import os, json

DEBUG = True

ADDIN_NAME = os.path.basename(os.path.dirname(__file__))
COMPANY_NAME = 'v-whitetail'
LOCAL_CONFIG = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'filepath.json')
MATERIAL_SYNC_FILE: str = 'None Selected'

with open(LOCAL_CONFIG, 'rt+') as local_config:
    file_contents: dict[str, str] = json.load(local_config)
    MATERIAL_SYNC_FILE: str = file_contents['filepath']

sample_palette_id = f'{COMPANY_NAME}_{ADDIN_NAME}_palette_id'