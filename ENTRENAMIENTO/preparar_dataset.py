"""
Prepara el dataset de entrenamiento a partir de SELECCION/.

- Blanquea el papel: el modelo debe aprender que el fondo es blanco puro,
  para que luego se pueda volver transparente sin halos.
- En las FOTOGRAFIADAS corrige además la iluminación desigual (sombras, viñeteo).
- Guarda PNG + .txt con la descripción en DATASET/.

Uso:  python ENTRENAMIENTO/preparar_dataset.py
Necesita: pip install pillow numpy
"""
import os
import sys
import glob

import numpy as np
from PIL import Image, ImageFilter

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from descripciones import DESCRIPCIONES, ESCENAS, TRIGGER  # noqa: E402

ORIGEN = os.path.join(RAIZ, "SELECCION")
DESTINO = os.path.join(RAIZ, "DATASET")
LADO_MAX = 1536  # no hace falta más para entrenar


def color_papel(arr):
    """Color del papel = tono de los píxeles más claros."""
    lum = arr.mean(axis=2)
    claros = arr[lum >= np.percentile(lum, 85)]
    return np.median(claros, axis=0)


def mapa_iluminacion(img):
    """Estima el papel sin trazos: se borran las líneas (filtro máximo) y se difumina."""
    pequeno = img.convert("L").resize((max(1, img.width // 8), max(1, img.height // 8)), Image.BILINEAR)
    pequeno = pequeno.filter(ImageFilter.MaxFilter(9)).filter(ImageFilter.GaussianBlur(6))
    return np.asarray(pequeno.resize(img.size, Image.BICUBIC), dtype=np.float32)


def blanquear(img, fotografiada):
    arr = np.asarray(img.convert("RGB"), dtype=np.float32)
    if fotografiada:
        ilum = mapa_iluminacion(img)[..., None]
        arr = arr / np.maximum(ilum, 1.0) * 255.0
    papel = np.maximum(color_papel(arr), 1.0)
    arr = arr / papel * 255.0
    # punto blanco: lo casi blanco pasa a blanco puro, sin tocar los trazos suaves
    arr = np.clip((arr - 0.0) / 0.97, 0, 255)
    if fotografiada:
        # las fotos pierden contraste; un poco de curva para recuperar el negro del grafito
        arr = 255.0 * (arr / 255.0) ** 1.15
    return Image.fromarray(np.clip(arr, 0, 255).astype(np.uint8))


def main():
    os.makedirs(DESTINO, exist_ok=True)
    for f in glob.glob(os.path.join(DESTINO, "*")):
        os.remove(f)
    hechas = 0
    for sub, foto in (("NUCLEO", False), ("FOTOGRAFIADAS", True)):
        for ruta in sorted(glob.glob(os.path.join(ORIGEN, sub, "*"))):
            num = int(os.path.basename(ruta).split("_")[0])
            if num not in DESCRIPCIONES:
                print("Sin descripción, se salta:", ruta)
                continue
            img = Image.open(ruta)
            img.thumbnail((LADO_MAX, LADO_MAX), Image.LANCZOS)
            img = blanquear(img, foto)
            base = os.path.join(DESTINO, f"{num:03d}")
            img.save(base + ".png", optimize=True)
            with open(base + ".txt", "w", encoding="utf-8") as fh:
                final = "full scene drawn on paper" if num in ESCENAS else "isolated on plain white paper"
                fh.write(f"{TRIGGER} illustration, {DESCRIPCIONES[num]}, {final}")
            hechas += 1
    print(f"{hechas} imágenes preparadas en {DESTINO}")


if __name__ == "__main__":
    main()
