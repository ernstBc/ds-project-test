import os
from pathlib import Path
import logging


logging.basicConfig(level=logging.INFO)

PROJECT_ID = "ds_project"

list_of_files = [
    "main.py",
    'app.py',
    'Dockerfile',
    'requirements.txt',
    '.github/workflows/.gitkeep',
    'config/config.yaml',
    'parameters.yaml',
    'schema.yaml',
    'setup.py',
    'notebooks/notebook.ipynb',
    f'src/{PROJECT_ID}/__init__.py',
    f'src/{PROJECT_ID}/components/__init__.py',
    f'src/{PROJECT_ID}/utils/__init__.py',
    f'src/{PROJECT_ID}/utils/utils.py',
    f'src/{PROJECT_ID}/config/__init__.py',
    f'src/{PROJECT_ID}/config/config.py',
    f'src/{PROJECT_ID}/pipeline/__init__.py',
    f'src/{PROJECT_ID}/entity/__init__.py',
    f'src/{PROJECT_ID}/entity/entity_config.py',
    f'src/{PROJECT_ID}/constants/__init__.py',
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)

    if filedir!= "":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Directory {filedir} created.")
    
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, 'w') as f:
            pass
            logging.info(f"File {filepath} created.")
    else:
        logging.info(f"File {filepath} already exists.")