import sys
from common import openFileByte, FILE_PATHS
from collections import Counter
import heapq

PADDING_ENCODING_SIZE = 3
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

    padding = (8 - (len(encodedChain)+ PADDING_ENCODING_SIZE) % 8) % 8 

    encodedChain = format(padding, f'0{PADDING_ENCODING_SIZE}b') + encodedChain
    
    for i in range(0, padding):
        encodedChain += "0"

    encodedFile = []
    for i in range(0, len(encodedChain), 8):
        group = encodedChain[i:i+8]
        byte = int(group, 2)
        encodedFile.append(byte)

    return bytes(encodedFile)

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


def main() -> None:
    
    texte_test = "ABCAABBAACAABAABA"
    fileByte_test = texte_test.encode('utf-8')  # convertit la chaîne en bytes

    encodedText = huffmanEncoder(fileByte_test)
    decodedText = huffmanDecoder(encodedText)

    print(fileByte_test == decodedText)

if __name__ == "__main__":
    main()