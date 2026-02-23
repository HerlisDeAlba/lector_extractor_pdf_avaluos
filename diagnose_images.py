import os, io
import numpy as np
from PIL import Image

VALID = [
    'CONJ RES NARANJOS DEL CANEY VIS_APTO RPH_51m2_2hab_3.png',
    'N A_CASA NO RPH_0m2_7hab_2.jpeg',
    'N A_CASA NO RPH_0m2_7hab_4.png',
    'NO APLICA_CASA_171m2_4hab_1.png',
    'TURPIAL_CASA_91m2_3hab_2.jpeg',
    'TURPIAL_CASA_91m2_3hab_3.jpeg',
    'TURPIAL_CASA_91m2_3hab_3.png',
    'TURPIAL_CASA_91m2_3hab_3_1.png',
]

folder = 'Croquis_Extraidos'
files = sorted(os.listdir(folder))

def analyze(path):
    with open(path, 'rb') as f:
        data = f.read()
    img = Image.open(io.BytesIO(data)).convert('RGB')
    arr = np.array(img)
    gray = arr.mean(axis=2)
    w, h = img.size
    sz = len(data) / 1024
    aspect = w / h if h > 0 else 0
    # Local texture std (8x8 grid)
    ph, pw = max(1, gray.shape[0] // 8), max(1, gray.shape[1] // 8)
    stds = [gray[r*ph:(r+1)*ph, c*pw:(c+1)*pw].std()
            for r in range(8) for c in range(8)]
    texture = np.mean(stds)
    brightness = gray.mean()
    pixels = arr.reshape(-1, 3)
    quant = (pixels // 32) * 32
    _, counts = np.unique(quant, axis=0, return_counts=True)
    dom = counts.max() / len(pixels)
    unique_colors = len(counts)
    return sz, w, h, aspect, texture, brightness, dom, unique_colors

import csv
with open('diag_output.csv', 'w', newline='', encoding='utf-8') as csvf:
    w = csv.writer(csvf)
    w.writerow(['File', 'KB', 'W', 'H', 'AR', 'Texture', 'Brightness', 'DomColor', 'UniqueColors', 'Valid'])
    for fname in files:
        path = os.path.join(folder, fname)
        try:
            sz, wd, h, ar, texture, brightness, dom, uniq = analyze(path)
            ok = 'YES' if fname in VALID else 'NO'
            w.writerow([fname, round(sz,1), wd, h, round(ar,2), round(texture,2), round(brightness,2), round(dom,3), uniq, ok])
        except Exception as e:
            w.writerow([fname, '', '', '', '', '', '', '', '', 'ERROR'])
print('Written to diag_output.csv')
