FILE_PATHS = [
    './Donnees/litteraire_fr.txt',
    './Donnees/structure_meteo.csv', 
    './Donnees/code_source_python.py'
    ]

def openFileByte(path: str) -> bytes:

    with open(path, 'rb') as f:
        return f.read()
    
def openFileChar(path: str) -> str:

    with open(path, 'r', encoding='utf-8') as f:
        return f.read()