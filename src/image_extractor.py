import os
import re
import io
import fitz  # pymupdf
import pandas as pd
import numpy as np
import math
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
        page_str = page_str.strip()
        
        # Format: "Página 6" or "página 6" -> explicit page mention
        explicit_pages = re.findall(r'p[aá]gina\s*(\d+)', page_str, re.IGNORECASE)
        if explicit_pages:
            for p in explicit_pages: pages.add(int(p))
            return sorted(list(pages))
        
        # Format: "8 de 18" -> page 8 of 18, take only the first number
        de_match = re.match(r'^\s*(\d+)\s+de\s+\d+', page_str, re.IGNORECASE)
        if de_match:
            pages.add(int(de_match.group(1)))
            return sorted(list(pages))
        
        # Format: "9-10" -> range pages 9 and 10
        range_match = re.match(r'^\s*(\d+)\s*-\s*(\d+)\s*$', page_str)
        if range_match:
            start, end = int(range_match.group(1)), int(range_match.group(2))
            for p in range(start, end + 1): pages.add(p)
            return sorted(list(pages))
        
        # Format: "8, 9, 12" or "8 9 12" -> comma/space separated list
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
        """Check if page has enough drawing elements OR images to be a floor plan."""
        drawings = page.get_drawings()
        valid_elements = 0
        for d in drawings:
            r = d["rect"]
            if r.width > 10 and r.height > 10:  # Ignore tiny elements
                valid_elements += 1
        
        # Also count images as valid elements (for scanned croquis)
        images = page.get_images()
        valid_elements += len(images)
        
        return valid_elements >= config.MIN_DRAWING_ELEMENTS

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
            
            # Check 2: Aspect Ratio (Skip footers/headers)
            # Exception: panoramic maps can be wide but have many colors and significant size
            w, h = img.size
            aspect_ratio = w / h if h > 0 else 0
            if aspect_ratio > config.MAX_ASPECT_RATIO:
                unique_colors = len(unique)
                size_kb = len(img_data) / 1024 if hasattr(img_data, '__len__') else 0
                is_panoramic_map = unique_colors >= config.MIN_COLORS_FOR_WIDE_MAP
                if not is_panoramic_map:
                    return False, f"aspect ratio {aspect_ratio:.2f} > {config.MAX_ASPECT_RATIO} (only {unique_colors} colors, not a map)"
            
            # Check 3: Brightness (Skip dark images / black blocks)
            gray_img = img.convert("L")
            stat = np.array(gray_img)
            mean_brightness = stat.mean()
            if mean_brightness < config.MIN_BRIGHTNESS_MEAN:
                return False, f"too dark (mean brightness {mean_brightness:.1f} < {config.MIN_BRIGHTNESS_MEAN})"

            # Check 4: Unique colors (simple logos have few colors)
            unique_colors = len(unique)
            if unique_colors < config.MIN_UNIQUE_COLORS:
                return False, f"only {unique_colors} unique colors < {config.MIN_UNIQUE_COLORS}"
            
            # Check 5: Photo vs Croquis - Texture/Gradient detection
            # Natural photos have high LOCAL color variation (gradients, textures, shadows)
            # Floor plans, maps (even satellite) have flatter, more uniform color regions
            # Strategy: sample patches and measure local std deviation
            gray = np.array(img.convert("L"), dtype=float)
            # Sample a grid of 8x8 patches across the image
            ph, pw = max(1, gray.shape[0] // 8), max(1, gray.shape[1] // 8)
            local_stds = []
            for row in range(8):
                for col in range(8):
                    patch = gray[row*ph:(row+1)*ph, col*pw:(col+1)*pw]
                    if patch.size > 0:
                        local_stds.append(patch.std())
            if local_stds:
                mean_local_std = np.mean(local_stds)
                if mean_local_std > config.MAX_LOCAL_TEXTURE_STD:
                    return False, f"photo-like texture: local_std={mean_local_std:.1f} > {config.MAX_LOCAL_TEXTURE_STD}"
            
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

    def get_nearest_label(self, rect, page):
        """Finds the nearest text keyword to a given rectangle."""
        words = page.get_text("words")
        if not words: return None, 0
        
        # Center of the image
        cx, cy = rect.x0 + rect.width/2, rect.y0 + rect.height/2
        
        min_dist = float('inf')
        best_word = None
        
        for w in words:
            # Word center
            wx = (w[0] + w[2]) / 2
            wy = (w[1] + w[3]) / 2
            d = math.sqrt((cx - wx)**2 + (cy - wy)**2)
            if d < min_dist:
                min_dist = d
                best_word = w[4].lower()
                
        return best_word, min_dist

    def extract_candidates(self, doc, page):
        """Extracts ALL valid candidates (raw images and crop clusters) from a page."""
        candidates = [] # List of (img_data, ext, source_type)
        
        # 1. Extract Raw Images
        images = page.get_images()
        # Get spatial info for all images on page to filter by location
        img_info_list = page.get_image_info(xrefs=True)
        xref_to_bbox = {info['xref']: fitz.Rect(info['bbox']) for info in img_info_list if info.get('xref')}

        for item in images:
            xref = item[0]
            try:
                # Spatial Filtering: Skip images in header/footer zones
                if xref in xref_to_bbox:
                    bbox = xref_to_bbox[xref]
                    if not self.is_in_safe_zone(bbox, page.rect):
                        # print(f"    -> Skipping image xr {xref}: outside safe zone (header/footer)")
                        continue
                    
                    # Proximity Filtering: Skip images near photo-report keywords
                    nearest_text, _ = self.get_nearest_label(bbox, page)
                    if nearest_text:
                        is_photo = any(k in nearest_text for k in config.PHOTO_KEYWORDS)
                        is_croquis = any(k in nearest_text for k in config.CROQUIS_KEYWORDS)
                        
                        # If it's explicitly a photo label and NOT a croquis label, skip
                        if is_photo and not is_croquis:
                            # print(f"    -> Skipping image xr {xref}: near photo keyword '{nearest_text}'")
                            continue

                base_image = doc.extract_image(xref)
                w = base_image["width"]
                h = base_image["height"]
                size_kb = len(base_image["image"]) / 1024
                
                # Relaxed size check
                if w < config.MIN_IMG_WIDTH and h < config.MIN_IMG_HEIGHT: continue
                if size_kb < config.MIN_IMG_SIZE_KB: continue
                
                candidates.append((base_image["image"], base_image["ext"], "raw_image"))
            except: continue
            
        # 2. Extract Rendered Crop (Drawings)
        # Only if we find valid drawing clusters
        crop_rect = self.get_clustered_crop_box(page)
        if crop_rect:
            try:
                pix = page.get_pixmap(dpi=300, clip=crop_rect)
                img_data = pix.tobytes("png")
                candidates.append((img_data, "png", "crop_render"))
            except: pass
            
        return candidates

    def process_csv(self):
        print(f"Reading {config.OUTPUT_FILE} for image extraction...")
        try:
            df = pd.read_csv(config.OUTPUT_FILE, sep=';', encoding='utf-8-sig', dtype=str)
        except Exception as e:
            print(f"Pandas load failed: {e}")
            return

        df.columns = [c.strip() for c in df.columns]
        count = 0
        saved_hashes = set()  # Content-hash dedup: skip duplicate images across pages
        
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
                    # if self.is_page_text_heavy(page):
                        # print(f"  -> Skipping page {p_num}: too much text (not a croquis)")
                        # continue
                    
                    if not self.has_enough_drawings(page):
                        print(f"  -> Skipping page {p_num}: not enough drawing elements")
                        continue
                    
                    base_name = f"{conjunto}_{tipo}_{area_val}m2_{hab_val}hab"
                    
                    print(f"  -> Extracting from page {p_num}...")
                    
                    # New: Extract ALL candidates (images + crop clusters)
                    candidates = self.extract_candidates(doc, page)
                    
                    if not candidates:
                        print(f"  -> No candidates found on page {p_num}")
                        continue
                        
                    for i, (img_data, ext, source_type) in enumerate(candidates):
                        # POST-VALIDATION
                        is_valid, reason = self.is_image_valid_croquis(img_data)
                        if not is_valid:
                            print(f"    -> Candidate {i+1} ({source_type}) skipped: {reason}")
                            continue

                        # Content-hash dedup: skip if this exact image was already saved
                        import hashlib
                        img_hash = hashlib.md5(img_data).hexdigest()
                        if img_hash in saved_hashes:
                            print(f"    -> Candidate {i+1} ({source_type}) skipped: duplicate image")
                            continue
                        saved_hashes.add(img_hash)

                        # Construct filename
                        # If multiple candidates, we MUST append a suffix to distinguish them 
                        # (even for the first one if there are more coming, but logical simplicity: just append counter)
                        suffix = f"_{i+1}" if len(candidates) > 1 else ""
                        out_name = f"{base_name}{suffix}.{ext}" if ext else f"{base_name}{suffix}.png"
                        
                        # Save with duplicate checking (global file conflict)
                        out_path = os.path.join(self.output_folder, out_name)
                        counter = 1
                        base_name_no_ext = os.path.splitext(out_name)[0]
                        final_ext = os.path.splitext(out_name)[1]
                        
                        # Ensure we don't overwrite if file exists (e.g. from previous run or another page)
                        while os.path.exists(out_path):
                            out_name = f"{base_name_no_ext}_{counter}{final_ext}"
                            out_path = os.path.join(self.output_folder, out_name)
                            counter += 1
                            
                        with open(out_path, "wb") as f:
                            f.write(img_data)
                        print(f"    -> Saved: {out_name} ({source_type})")
                        count += 1
                doc.close()
            except Exception as e:
                print(f"Error processing {pdf_name}: {e}")
                
        print(f"Image Extraction Complete. {count} images saved to {self.output_folder}")
