"""
Genera las dos configuraciones de entrenamiento (una por cada RTX 4090).

  Versión A: rank 16  -> estilo más suave, generaliza mejor a temas nuevos.
  Versión B: rank 32  -> copia el trazo con más fidelidad, riesgo de "calcar".

Se entrenan a la vez y luego se elige la que salga mejor (y en qué paso).
Solo usa la librería estándar de Python. Lo llama 2_ENTRENAR.bat.
"""
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.dirname(AQUI)
sys.path.insert(0, AQUI)
from descripciones import TRIGGER  # noqa: E402

DATASET = os.path.join(RAIZ, "DATASET").replace("\\", "/")
SALIDAS = os.path.join(RAIZ, "SALIDAS").replace("\\", "/")

PRUEBAS = [
    "[trigger] illustration, a nun praying with her hands together, full body, graphite and grey wash, isolated on plain white paper",
    "[trigger] illustration, a butcher in a white apron holding a big knife, full body, colored pencil, isolated on plain white paper",
    "[trigger] illustration, the inside of an old butcher shop with hanging meat and a counter, full scene drawn on paper",
    "[trigger] illustration, an old woman sitting on a chair with a cat on her lap, red and blue colored pencil, isolated on plain white paper",
    "[trigger] illustration, a dog sitting and looking up, graphite, isolated on plain white paper",
    "[trigger] illustration, a young man running, full body, colored pencil and watercolor, isolated on plain white paper",
]

PLANTILLA = """---
job: extension
config:
  name: "{nombre}"
  process:
    - type: 'sd_trainer'
      training_folder: "{salidas}"
      device: cuda:0
      trigger_word: "{trigger}"
      network:
        type: "lora"
        linear: {rank}
        linear_alpha: {rank}
      save:
        dtype: float16
        save_every: 250
        max_step_saves_to_keep: 12
        push_to_hub: false
      datasets:
        - folder_path: "{dataset}"
          caption_ext: "txt"
          caption_dropout_rate: 0.05
          shuffle_tokens: false
          cache_latents_to_disk: true
          resolution: [ 512, 768, 1024 ]
      train:
        batch_size: 1
        steps: {pasos}
        gradient_accumulation_steps: 1
        train_unet: true
        train_text_encoder: false
        gradient_checkpointing: true
        noise_scheduler: "flowmatch"
        optimizer: "adamw8bit"
        lr: {lr}
        ema_config:
          use_ema: true
          ema_decay: 0.99
        dtype: bf16
      model:
        name_or_path: "black-forest-labs/FLUX.1-dev"
        is_flux: true
        quantize: true
      sample:
        sampler: "flowmatch"
        sample_every: 250
        width: 1024
        height: 1024
        prompts:
{pruebas}
        neg: ""
        seed: 42
        walk_seed: true
        guidance_scale: 4
        sample_steps: 20
meta:
  name: "[name]"
  version: '1.0'
"""

VERSIONES = {
    "estilo_A_rank16": dict(rank=16, lr="1e-4", pasos=3000),
    "estilo_B_rank32": dict(rank=32, lr="1e-4", pasos=3000),
}


def main():
    os.makedirs(SALIDAS, exist_ok=True)
    pruebas = "\n".join(f'          - "{p}"' for p in PRUEBAS)
    for nombre, v in VERSIONES.items():
        ruta = os.path.join(AQUI, f"{nombre}.yaml")
        with open(ruta, "w", encoding="utf-8") as fh:
            fh.write(PLANTILLA.format(nombre=nombre, salidas=SALIDAS, dataset=DATASET,
                                      trigger=TRIGGER, pruebas=pruebas, **v))
        print("Configuración creada:", ruta)


if __name__ == "__main__":
    main()
