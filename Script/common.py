PADDING_ENCODING_SIZE = 3

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
    
def packBitsToBytes(encodedChain: str) -> bytes:

    padding = (8 - (len(encodedChain) + PADDING_ENCODING_SIZE) % 8) % 8
    encodedChain = format(padding, f'0{PADDING_ENCODING_SIZE}b') + encodedChain

    for i in range(0, padding):
        encodedChain += "0"

    encodedFile = []
    for i in range(0, len(encodedChain), 8):
        group = encodedChain[i:i+8]
        byte = int(group, 2)
        encodedFile.append(byte)

    return bytes(encodedFile)