# Entrenamiento del estilo

El dataset ya está preparado en `DATASET/` (59 imágenes con el papel blanqueado y su descripción).
En tu ordenador solo hay que instalar y entrenar.

## Antes de empezar (una sola vez)

1. **Git**: si no lo tienes, instálalo desde https://git-scm.com/download/win (todo por defecto).
2. **Descarga este repositorio** a tu ordenador, en un disco con unos **60 GB libres** (el C:, que es el rápido):
   abre una terminal en la carpeta donde lo quieras y ejecuta
   `git clone https://github.com/IkerEker/ESTILO.git`
   (si ya lo tenías clonado, basta con `git pull` dentro de la carpeta).
3. **Cuenta de Hugging Face** (gratis) y aceptar la licencia de FLUX.1-dev. El instalador te lo explica en pantalla cuando llega ese punto.

## Pasos

1. Doble clic en `ENTRENAMIENTO\1_INSTALAR.bat`. Tarda (descarga unos 10 GB). Al final te pide el token de Hugging Face.
2. Doble clic en `ENTRENAMIENTO\2_ENTRENAR.bat`. Se abren dos ventanas, una por cada 4090:
   - **A (rank 16)**: estilo más suave, mejor para temas que no aparecen en las imágenes.
   - **B (rank 32)**: trazo más fiel al original.
3. Cada 250 pasos se guardan imágenes de prueba en `SALIDAS\estilo_A_rank16\samples` y `SALIDAS\estilo_B_rank32\samples`
   (monja rezando, carnicero, carnicería, anciana con gato, perro, chico corriendo).
   Así vemos cómo va aprendiendo y elegimos el mejor punto: a veces el paso 1500 es mejor que el 3000.

## Cuando termine

Pásale a Claude una captura de las carpetas `samples` (o súbelas al repositorio, en `PRUEBAS/`).
Con eso elegimos la versión y el paso, y empezamos con el programa de generación.

Los modelos entrenados (`SALIDAS\...\*.safetensors`) **no se suben a GitHub**: pesan demasiado y se quedan en tu ordenador.

## Si algo falla

Copia el texto de la ventana y pásaselo a Claude.

## Archivos

| Archivo | Para qué |
|---|---|
| `descripciones.py` | Descripción de cada imagen y la palabra clave del estilo (`lpzsk`) |
| `preparar_dataset.py` | Rehace `DATASET/` desde `SELECCION/` (solo si cambias la selección o las descripciones) |
| `crear_configs.py` | Genera las dos configuraciones de entrenamiento |
