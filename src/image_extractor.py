import os
import re
import io
import fitz  # pymupdf
import pandas as pd
import numpy as np
from PIL import Image
from . import config

class ImageExtractor:
    def __init__(self):
        self.output_folder = config.IMAGE_OUTPUT_FOLDER
        if not os.path.exists(self.output_folder):
            os.makedirs(self.output_folder)
            
    def clean_filename_segment(self, text):
        if not isinstance(text, str): return "NA"
        text = text.replace('-', ' ').replace('_', ' ').replace('.', ' ')
        cleaned = re.sub(r'[^A-Z0-9\s]', '', text.upper())
        cleaned = re.sub(r'\s+', ' ', cleaned).strip()
        return cleaned if cleaned else "NA"

    def clean_number(self, text):
        if not isinstance(text, str): return "0"
        match = re.search(r'(\d+)', text)
        return match.group(1) if match else "0"

    def parse_pages(self, page_str):
        if not isinstance(page_str, str) or not page_str.strip(): return []
        pages = set()
        explicit_pages = re.findall(r'Página (\d+)', page_str, re.IGNORECASE)
        if explicit_pages:
            for p in explicit_pages: pages.add(int(p))
        else:
            nums = re.findall(r'\d+', page_str)
            for n in nums: pages.add(int(n))
        return sorted(list(pages))

    def rect_distance(self, r1, r2):
        if r1.intersects(r2): return 0
        dx = max(0, r1.x0 - r2.x1, r2.x0 - r1.x1)
        dy = max(0, r1.y0 - r2.y1, r2.y0 - r1.y1)
        return max(dx, dy)

    def is_in_safe_zone(self, rect, page_rect):
        safe_y_min = page_rect.height * config.EXCLUDE_TOP_PCT
        safe_y_max = page_rect.height * (1.0 - config.EXCLUDE_BOTTOM_PCT)
        center_y = rect.y0 + rect.height/2
        return safe_y_min <= center_y <= safe_y_max

    def is_page_text_heavy(self, page):
        """Check if page has too much text (not a croquis page)."""
        text = page.get_text("text")
        words = text.split()
        return len(words) > config.MAX_TEXT_WORDS_ON_PAGE

    def has_enough_drawings(self, page):
        """Check if page has enough drawing elements to be a floor plan."""
        drawings = page.get_drawings()
        valid_drawings = 0
        for d in drawings:
            r = d["rect"]
            if r.width > 10 and r.height > 10:  # Ignore tiny elements
                valid_drawings += 1
        return valid_drawings >= config.MIN_DRAWING_ELEMENTS

    def is_image_valid_croquis(self, img_data):
        """Analyze image to determine if it looks like a croquis."""
        try:
            img = Image.open(io.BytesIO(img_data)).convert("RGB")
            img_array = np.array(img)
            
            # Check 1: Dominant color ratio (detect mostly black/white/single color pages)
            pixels = img_array.reshape(-1, 3)
            total_pixels = len(pixels)
            
            # Quantize to reduce noise
            quantized = (pixels // 32) * 32
            unique, counts = np.unique(quantized, axis=0, return_counts=True)
            max_count = counts.max()
            dominant_ratio = max_count / total_pixels
            
            if dominant_ratio > config.MAX_DOMINANT_COLOR_RATIO:
                return False, f"dominant color covers {dominant_ratio:.1%}"
            
            # Check 2: Unique colors (simple logos have few colors)
            unique_colors = len(unique)
            if unique_colors < config.MIN_UNIQUE_COLORS:
                return False, f"only {unique_colors} unique colors"
            
            return True, "valid"
        except Exception as e:
            return True, f"validation error: {e}"  # Allow on error

    def get_clustered_crop_box(self, page):
        elements = []
        
        # Collect & Filter
        for p in page.get_drawings():
            r = p["rect"]
            if r.width < 5 and r.height < 5: continue
            if r.width > page.rect.width * 0.95 and r.height > page.rect.height * 0.95: continue
            if self.is_in_safe_zone(r, page.rect):
                elements.append(r)
            
        for img in page.get_images():
            try:
                r = page.get_image_bbox(img)
                if r.width > page.rect.width * 0.98 and r.height > page.rect.height * 0.98: continue
                if self.is_in_safe_zone(r, page.rect):
                    elements.append(r)
            except: pass
            
        if not elements: return None

        # Cluster
        clusters = []
        assigned = [False] * len(elements)
        
        for i in range(len(elements)):
            if assigned[i]: continue
            current_cluster = elements[i]
            assigned[i] = True
            
            changed = True
            while changed:
                changed = False
                for j in range(len(elements)):
                    if not assigned[j]:
                        if self.rect_distance(current_cluster, elements[j]) <= config.IMG_CLUSTER_DISTANCE:
                            current_cluster |= elements[j]
                            assigned[j] = True
                            changed = True
            clusters.append(current_cluster)
            
        if not clusters: return None
        
        best_cluster = max(clusters, key=lambda r: r.width * r.height)
        best_cluster += (-config.IMG_PADDING_PX, -config.IMG_PADDING_PX, config.IMG_PADDING_PX, config.IMG_PADDING_PX)
        best_cluster &= page.rect
        return best_cluster

    def extract_primary_image(self, doc, page):
        """Extracts raw image ONLY if it meets size thresholds."""
        images = page.get_images()
        if not images: return None, None
            
        best_image = None
        max_area = 0
        
        for item in images:
            xref = item[0]
            try:
                base_image = doc.extract_image(xref)
                w = base_image["width"]
                h = base_image["height"]
                size_kb = len(base_image["image"]) / 1024
                
                if w < config.MIN_IMG_WIDTH or h < config.MIN_IMG_HEIGHT: continue
                if size_kb < config.MIN_IMG_SIZE_KB: continue
                
                area = w * h
                if area > max_area:
                    max_area = area
                    best_image = base_image
            except: continue
                
        if best_image:
            return best_image["image"], best_image["ext"]
        return None, None

    def process_csv(self):
        print(f"Reading {config.OUTPUT_FILE} for image extraction...")
        try:
            df = pd.read_csv(config.OUTPUT_FILE, sep=';', encoding='utf-8-sig', dtype=str)
        except Exception as e:
            print(f"Pandas load failed: {e}")
            return

        df.columns = [c.strip() for c in df.columns]
        count = 0
        
        for index, row in df.iterrows():
            is_included = str(row['CROQUIS_INCLUIDO_SN']).strip().lower()
            if is_included not in ['si', 'sí', 's', 'yes', 'true', '1']: continue
                
            pdf_name = str(row['ARCHIVO']).strip()
            pdf_path = os.path.join(config.PDF_FOLDER, pdf_name)
            if not os.path.exists(pdf_path): continue
                
            conjunto = self.clean_filename_segment(row.get('CONJUNTO_URB', ''))
            tipo = self.clean_filename_segment(row.get('TIPO_BIEN', ''))
            area_val = self.clean_number(row.get('AREA_PRIVADA', '') if row.get('AREA_PRIVADA') != 'nan' else row.get('AREA_CONSTRUIDA', ''))
            hab_str = row.get('NUM_ALCOBAS', '')
            hab_val = self.clean_number(hab_str)
            
            target_pages = self.parse_pages(str(row['PAG_CROQUIS']))
            if not target_pages: continue
                
            print(f"Processing Images for {pdf_name} -> Page(s) {target_pages}")
            
            try:
                doc = fitz.open(pdf_path)
                for p_num in target_pages:
                    idx = p_num - 1
                    if idx < 0 or idx >= len(doc): continue
                    page = doc.load_page(idx)
                    
                    # PRE-VALIDATION: Check if page looks like a croquis page
                    if self.is_page_text_heavy(page):
                        print(f"  -> Skipping page {p_num}: too much text (not a croquis)")
                        continue
                    
                    if not self.has_enough_drawings(page):
                        print(f"  -> Skipping page {p_num}: not enough drawing elements")
                        continue
                    
                    base_name = f"{conjunto}_{tipo}_{area_val}m2_{hab_val}hab"
                    
                    # 1. Try Extract Raw
                    img_data, ext = self.extract_primary_image(doc, page)
                    
                    if img_data:
                        out_name = f"{base_name}.{ext}" if ext else f"{base_name}.png"
                    else:
                        # 2. Fallback Render
                        crop_rect = self.get_clustered_crop_box(page)
                        if not crop_rect: continue
                        pix = page.get_pixmap(dpi=300, clip=crop_rect)
                        img_data = pix.tobytes("png")
                        out_name = f"{base_name}.png"

                    # POST-VALIDATION: Check if extracted image looks like a croquis
                    is_valid, reason = self.is_image_valid_croquis(img_data)
                    if not is_valid:
                        print(f"  -> Skipping page {p_num}: {reason}")
                        continue

                    # Save with duplicate checking
                    out_path = os.path.join(self.output_folder, out_name)
                    counter = 1
                    base_name_no_ext = os.path.splitext(out_name)[0]
                    final_ext = os.path.splitext(out_name)[1]
                    while os.path.exists(out_path):
                        out_name = f"{base_name_no_ext}_{counter}{final_ext}"
                        out_path = os.path.join(self.output_folder, out_name)
                        counter += 1
                        
                    with open(out_path, "wb") as f:
                        f.write(img_data)
                    count += 1
                doc.close()
            except Exception as e:
                print(f"Error processing {pdf_name}: {e}")
                
        print(f"Image Extraction Complete. {count} images saved to {self.output_folder}")
