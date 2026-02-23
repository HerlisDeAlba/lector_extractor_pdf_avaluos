import os
from PIL import Image

folder = "Croquis_Extraidos"
files = os.listdir(folder)

print(f"{'Filename':<50} | {'Size (KB)':<10} | {'Dimensions':<15} | {'Ratio':<5}")
print("-" * 90)

for f in files:
    try:
        path = os.path.join(folder, f)
        size_kb = os.path.getsize(path) / 1024
        with Image.open(path) as img:
            w, h = img.size
            ratio = w / h if h > 0 else 0
            print(f"{f[:47]:<50} | {size_kb:<10.2f} | {f'{w}x{h}':<15} | {ratio:<.2f}")
    except Exception as e:
        print(f"Error reading {f}: {e}")
