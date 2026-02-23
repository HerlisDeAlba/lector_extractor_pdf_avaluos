import fitz, hashlib, io, os
from PIL import Image
import numpy as np

doc = fitz.open('Avaluos_PDF/AvaluUo.pdf')
page = doc.load_page(11) # Page 12
imgs = page.get_images()
print(f"Total images on Page 12: {len(imgs)}")

for i, info in enumerate(imgs):
    xref = info[0]
    bi = doc.extract_image(xref)
    data = bi['image']
    h = hashlib.md5(data).hexdigest()
    
    img = Image.open(io.BytesIO(data)).convert('RGB')
    w, h_img = img.size
    arr = np.array(img)
    gray = arr.mean(axis=2)
    bri = gray.mean()
    
    ph, pw = max(1, arr.shape[0]//8), max(1, arr.shape[1]//8)
    stds = [gray[r*ph:(r+1)*ph, c*pw:(c+1)*pw].std() for r in range(8) for c in range(8)]
    tex = np.mean(stds)
    
    unique_colors = len(np.unique(arr.reshape(-1, 3), axis=0))
    ar = w/h_img if h_img > 0 else 0
    
    # Quantitative diagnostic
    pixels = arr.reshape(-1, 3)
    quantized = (pixels // 32) * 32
    _, counts = np.unique(quantized, axis=0, return_counts=True)
    dom = counts.max() / len(pixels)
    
    print(f"Index {i}: xref={xref} hash={h[:8]} {w}x{h_img} bri={bri:.1f} tex={tex:.1f} uniq={unique_colors} ar={ar:.2f} dom={dom:.3f}")
    
    # Save for manual verification (I will check properties later)
    out_path = f"debug_p12_img_{i}_{xref}.jpg"
    with open(out_path, "wb") as f:
        f.write(data)

doc.close()
