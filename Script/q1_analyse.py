#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import math
from collections import Counter
import re
import csv
from common import openFileByte, openFileChar, FILE_PATHS

METRICS = [
    'Taille du fichier [octets]',
    'Nombre de symboles [caractères]',
    'Taille de l’alphabet [octets]',
    'Taille de l’alphabet [caractères]',
    'Entropie $H(X)$ [bits/octet]',
    'Entropie $H(X)$ [bits/caractère]',
    'Taille théorique minimale [octets]',
    'Ratio mots uniques / mots totaux [%]'
]

OUTPUT_PATH = './Resultats/q1_metriques.csv'

def getFileData(fileByte: bytes, fileChar: str):
        
    fileSizeByte = len(fileByte)
    fileLength = len(fileChar)

    alphByte = set(fileByte)
    alphByteLength = len(alphByte)

    alphChar = set(fileChar)
    alphCharLength = len(alphChar)
    
    entropyByte = calcEntropy(fileByte)
    entropyChar = calcEntropy(fileChar)

    minSize = (entropyByte * fileSizeByte) / 8

    tokens = tokenize(fileChar)
    uniqueWordsRatio = int(len(set(tokens)) / len(tokens) *100)

    return fileSizeByte, fileLength, alphByteLength, alphCharLength, entropyByte, entropyChar, minSize, uniqueWordsRatio

def calcEntropy(file) -> float:

    n = len(file)
    frequencies = Counter(file)

    entropy = 0.0
    for count in frequencies.values():
        p = count / n
        entropy -= p * math.log2(p)

    return entropy

def tokenize(fileChar: str):

    splitters = r"[ \n;,.']+"
    tokens = re.split(splitters, fileChar)
    tokens = [t for t in tokens if t]
    return tokens

def main() -> None:

    data = []
    for path in FILE_PATHS:
        fileByte = openFileByte(path)
        fileChar = openFileChar(path)
        fileData = getFileData(fileByte, fileChar)
        data.append(fileData)

    transposedData = list(zip(*data))

    with open(OUTPUT_PATH, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(['Métrique', 'Littéraire (fr)', 'Structuré (CSV)', 'Code (Python)'])
        
        for index, metric in enumerate(METRICS):
            line = [metric]
            for value in transposedData[index]:
                if isinstance(value, float):
                    line.append(f"{value:.2f}")
                else:
                    line.append(value)
            writer.writerow(line)
        

if __name__ == "__main__":
    main()