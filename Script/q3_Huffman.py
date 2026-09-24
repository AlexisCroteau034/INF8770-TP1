import sys
from common import openFileByte, FILE_PATHS, PADDING_ENCODING_SIZE, packBitsToBytes
from collections import Counter
import heapq

DICT_LEN_ENCODING_SIZE = 16
SYMBOL_LEN_ENCODING_SIZE = 8
SYMBOL_ENCODING_SIZE = 8

class Node:
    def __init__(self, freq, symbol = None, left = None, right = None):
        self.freq = freq
        self.symbol = symbol
        self.left = left
        self.right = right

    def __lt__(self, other):
        return self.freq < other.freq
    
def buildTree(file: bytes) -> Node:
    
    frequencies = Counter(file)
    
    heap = []
    for symbol, freq in frequencies.items():
       heap.append(Node(freq, symbol))
    
    heapq.heapify(heap)

    while len(heap) > 1:
        leftChild = heapq.heappop(heap)
        rightChild = heapq.heappop(heap)
        freqSum = leftChild.freq + rightChild.freq
        heapq.heappush(heap, Node(freqSum, None, leftChild, rightChild))

    return heapq.heappop(heap)
    
def buildDictionary(node: Node, prefix: str = "", dictionary: dict = None) -> dict:

    if dictionary is None:
        dictionary = {}
    
    if node.symbol is not None:
        dictionary[node.symbol] = prefix
        return dictionary
    
    buildDictionary(node.left, prefix + "0", dictionary)
    buildDictionary(node.right, prefix + "1", dictionary)
    
    return dictionary

def encodeDictionary(dictionary: dict) -> str:
    
    encodedDictionary = ""
    for symbol, code in dictionary.items():
        encodedDictionary += format(len(code), f'0{SYMBOL_LEN_ENCODING_SIZE}b') + code + format(symbol, f'0{SYMBOL_ENCODING_SIZE}b')

    return encodedDictionary

def encodeContent(file: bytes, dictionnary: dict) -> str:

    encodedList = []
    for byte in file:
        encodedList.append(dictionnary[byte])

    encodedChain = ''.join(encodedList)

    return encodedChain

def huffmanEncoder(file: bytes) -> bytes:
    
    treeRoot = buildTree(file)
    dictionary = buildDictionary(treeRoot)

    encodedDictionary = encodeDictionary(dictionary)
    encodedContent = encodeContent(file, dictionary)

    encodedChain = format(len(encodedDictionary), f'0{DICT_LEN_ENCODING_SIZE}b') + encodedDictionary + encodedContent

    return packBitsToBytes(encodedChain)

def decodeDictionary(encodedDictionary: str) -> dict:

    dictionary = {}
    position = 0
    
    while position < len(encodedDictionary):
        
        length = int(encodedDictionary[position:position + SYMBOL_LEN_ENCODING_SIZE], 2)
        position += SYMBOL_LEN_ENCODING_SIZE
        
        code = encodedDictionary[position: position + length]
        position += length
        
        dictionary[code] = int(encodedDictionary[position: position + SYMBOL_ENCODING_SIZE], 2)
        position += SYMBOL_ENCODING_SIZE

    return dictionary

def huffmanDecoder(file: bytes) -> bytes:

    encodedChain = ''.join(format(byte, '08b') for byte in file)

    padding = int(encodedChain[0:PADDING_ENCODING_SIZE], 2)
    dictStart = PADDING_ENCODING_SIZE+DICT_LEN_ENCODING_SIZE
    dictSize = int(encodedChain[PADDING_ENCODING_SIZE:dictStart], 2)
    dictionary = decodeDictionary(encodedChain[dictStart:dictStart + dictSize])
    encodedContent = encodedChain[dictStart + dictSize:]

    if padding != 0:
        encodedContent = encodedContent[:-padding]
    
    decodedFile = []

    buffer = ""
    for bit in encodedContent:
        buffer += bit
        
        if buffer in dictionary:
            decodedFile.append(dictionary[buffer])
            buffer = ""

    return bytes(decodedFile)

def processFile(path: str) -> bool:
 
    original = openFileByte(path)
 
    encoded = huffmanEncoder(original)
    decoded = huffmanDecoder(encoded)
 
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
