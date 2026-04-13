import PyInstaller.__main__
import os
import shutil
from pathlib import Path

def build():
    # Nombre del ejecutable
    app_name = "AnonymizerPro"
    
    # 1. Limpiar carpetas previas
    for folder in ['build', 'dist']:
        if os.path.exists(folder):
            shutil.rmtree(folder)

    # 2. Configurar argumentos de PyInstaller
    # Importante: Las rutas son relativas al lugar desde donde se corre el script
    # (asumimos que se corre desde el raíz del proyecto)
    args = [
        'anonymizer/gui.py',              # Script principal
        '--name=%s' % app_name,           # Nombre del exe
        '--onefile',                      # Generar un único archivo .exe
        '--windowed',                     # No abrir consola al ejecutar
        '--noconfirm',                    # No pedir confirmación
        '--clean',                        # Limpiar cache
        '--icon=docs/assets/logo.ico',    # Icono del ejecutable
        
        # Incluir archivos adicionales (formato: origen;destino)
        '--add-data=docs/mini_manual.html;.',  # Incluimos el manual
        '--add-data=docs/assets/logo.png;.',   # Incluimos el logo
        
        # Importante para librerías de IA y Spacy
        '--collect-all=spacy',
        '--collect-all=xx_ent_wiki_sm',   # Si usas este modelo (o el que tengas)
        '--collect-all=customtkinter',
    ]

    print(f"Iniciando construcción de {app_name}.exe...")
    PyInstaller.__main__.run(args)
    print("\n¡Construcción finalizada!")
    print(f"El ejecutable se encuentra en la carpeta 'dist/{app_name}.exe'")

if __name__ == "__main__":
    build()
