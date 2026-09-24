import math
from common import packBitsToBytes, unpackBytesToBits, openFileByte,  FILE_PATHS

SYMBOL_ENCODING_SIZE = 8

def initDictionary() -> dict:
    
    dictionary = {}
    for i in range(2 ** SYMBOL_ENCODING_SIZE):
        symbol = bytes([i])
        dictionary[symbol] = i
    
    return dictionary
        
def requiredBits(n: int) -> int:
    return math.ceil(math.log2(n))

def encodeData(dictionary: dict, symbol: bytes):
    encodingSize = requiredBits(len(dictionary))
    return format(dictionary[symbol], f'0{encodingSize}b')

def lzwEncoder(file: bytes) -> bytes:
    
    dictionary = initDictionary()
    counter = len(dictionary)

    encodedList = []

    buffer = bytes()
    for byte in file:
        extended = buffer + bytes([byte])
        
        if extended in dictionary:
            buffer = extended
        else:            
            code = encodeData(dictionary, buffer)
            encodedList.append(code)
            
            dictionary[extended] = counter
            counter += 1
            buffer = bytes([byte])
    
    if buffer != bytes():
        code = encodeData(dictionary, buffer)
        encodedList.append(code)
    
    encodedChain = ''.join(encodedList)

    return packBitsToBytes(encodedChain)

def lzwDecoder(file: bytes) -> bytes:
    encodedChain = unpackBytesToBits(file)

    dictionary = [bytes([i]) for i in range(2 ** SYMBOL_ENCODING_SIZE)]
    initialSize = len(dictionary)

    decoded = bytearray()
    previous = None
    position = 0
    index = 0

    while position < len(encodedChain):
        width = requiredBits(initialSize + index)
        code = int(encodedChain[position:position + width], 2)
        position += width

        if code < len(dictionary):
            entry = dictionary[code]
        elif code == len(dictionary) and previous is not None:
            entry = previous + previous[:1]
        else:
            raise ValueError(f"Invalid LZW code {code} at position {position - width}")

        if previous is not None:
            dictionary.append(previous + entry[:1])

        decoded.extend(entry)
        previous = entry
        index += 1

    return bytes(decoded)

def processFile(path: str) -> bool:
    original = openFileByte(path)
 
    encoded = lzwEncoder(original)
    decoded = lzwDecoder(encoded)
 
    ratio = len(encoded) / len(original)

    ok = False
    if decoded == original:
        ok = True
 
    print(f"{path}")
    print(f"  original : {len(original)} bytes")
    print(f"  encoded  : {len(encoded)} bytes ({ratio:.1%} of original)")
    print(f"  roundtrip: {'OK' if ok else 'MISMATCH'}")
 
    return ok
 
def main() -> None:
    paths = FILE_PATHS
 
    for path in paths:
        try:
            processFile(path)
        except FileNotFoundError:
            print(f"{path}\n  file not found")
 
if __name__ == "__main__":
    main()
