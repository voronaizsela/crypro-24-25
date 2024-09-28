#!/bin/python
from typing import Callable
from math import log2
from decimal import *

import pandas as pd
import argparse
import pprint
import os

getcontext().prec = 50

# 1 << 16 = 64KB
TEXT_BLOCK_SIZE = 1 << 16

STANDARD_ALPHABET = {
    "А": "а", "Б": "б", "В": "в", "Г": "г", "Д": "д", "Е": "е", "Ж": "ж", "З": "з", "И": "и", "Й": "й", "К": "к",
    "Л": "л", "М": "м", "Н": "н", "О": "о", "П": "п", "Р": "р", "С": "с", "Т": "т", "У": "у", "Ф": "ф", "Х": "х",
    "Ц": "ц", "Ч": "ч", "Ш": "ш", "Щ": "щ", "Ы": "ы", "Ь": "ь", "Э": "э", "Ю": "ю", "Я": "я"
}

STANDARD_ALPHABET_WHITESPACE = {
    "А": "а", "Б": "б", "В": "в", "Г": "г", "Д": "д", "Е": "е", "Ж": "ж", "З": "з", "И": "и", "Й": "й", "К": "к",
    "Л": "л", "М": "м", "Н": "н", "О": "о", "П": "п", "Р": "р", "С": "с", "Т": "т", "У": "у", "Ф": "ф", "Х": "х",
    "Ц": "ц", "Ч": "ч", "Ш": "ш", "Щ": "щ", "Ы": "ы", "Ь": "ь", "Э": "э", "Ю": "ю", "Я": "я", "\x00": " "
}

STATICTIC_OUTPUT_FILE = "statistic.xlsx"

class EntropyCalculator:
    alphabet: set
    up2low: dict[str, str]

    monogramCount: dict[str, int]
    totalMonograms: int = 0

    distinctBigramCount: dict[str, int]
    totalDistinctBigrams: int = 0

    overlappedBigramCount: dict[str, int]
    totalOverlappedBigrams: int = 0

    whitespace: str | None
    isWhitespace: bool = False
    previousSymbol: str | None = None

    # Alphabet is dictionary uppercase -> lowercase
    # \x00 in uppercase mean that character which not included in alphabet
    # can be interpreted as \x00 lowercase. Sequences of \x00 counts as 1 symbol
    def __init__(self, alphabet: dict[str, str]):
        self.alphabet = set(alphabet.values())
        self.up2low = alphabet

        # Init dictionaries
        self.monogramCount = {c: 0 for c in self.alphabet}
        self.overlappedBigramCount = {c1 + c2: 0 for c1 in self.alphabet for c2 in self.alphabet}
        self.whitespace = alphabet["\x00"] if "\x00" in alphabet else None
        if not self.whitespace is None:
            # There cannot be two whitespace bigram
            del self.overlappedBigramCount[self.whitespace*2]

        self.distinctBigramCount = self.overlappedBigramCount.copy()

    def updateNgramDicts(self, currentSymbol: str):
        self.monogramCount[currentSymbol] += 1
        self.totalMonograms += 1
        
        # previousSymbol absent for the first letter
        if not self.previousSymbol is None:
            # Total overlapped bigrams count is one less than monograms count
            self.overlappedBigramCount[self.previousSymbol + currentSymbol] += 1
            self.totalOverlappedBigrams += 1

            # Total distinct bigrams count is half monograms count
            if self.totalMonograms % 2 == 0:
                self.distinctBigramCount[self.previousSymbol + currentSymbol] += 1
                self.totalDistinctBigrams += 1

    def handleText(self, text: str):
        for c in text:
            # All characters not included in the alphabet are considered whitespace
            if c not in self.alphabet or (not self.whitespace is None and c == self.whitespace):
                # If whitespace not provided in alphabet just skip it.
                if self.whitespace is None:
                    continue

                # We need to skip, when two or more whitespaces in row,
                # since there can be only one whitespace
                if self.isWhitespace:
                    continue
                
                self.updateNgramDicts(self.whitespace)
                self.isWhitespace = True
                self.previousSymbol = self.whitespace
                continue

            self.isWhitespace = False
            self.updateNgramDicts(c)
            self.previousSymbol = c

    # Create a DataFrame for monogram frequencies.
    def formMonogramDF(self) -> pd.DataFrame:
        monoDF = pd.DataFrame()
        monoFreq = calculateFrequency(self.monogramCount, self.totalMonograms)

        monogramCol: list[str] = []
        freqCol: list[Decimal] = []

        # Split frequencies dictionary into two columns (monograms with corresponding frequencies by index).
        for monogram, freq in monoFreq.items():
            monogramCol.append(monogram)
            freqCol.append(freq)
        
        monoDF.insert(0, "Monogram", monogramCol, allow_duplicates=True)
        monoDF.insert(1, "Frequency", freqCol, allow_duplicates=True)
        return monoDF
    
    # Create a DataFrame for bigram frequencies.
    def formBigramDF(self, overlapped: bool = True) -> pd.DataFrame:
        biDF = pd.DataFrame()

        # Calculate frequencies depending on whether the bigrams can ovelap.
        biFreq: dict[str, Decimal] = {}
        if overlapped:
            biFreq = calculateFrequency(self.overlappedBigramCount, self.totalOverlappedBigrams)
        else:
            biFreq = calculateFrequency(self.distinctBigramCount, self.totalDisctinctBigrams)

        bigramCol: list[str] = []
        bigramRow: list[str] = []

        # Split bigrams into headers: column (1st letter) and a row (2nd letter).
        for bigram in biFreq.keys():
            bigramRow.append(bigram[0])
            bigramCol.append(bigram[1])

        # Remove duplicates.
        bigramCol = removeDuplicates(bigramCol)
        bigramRow = removeDuplicates(bigramRow)

        # Pre-fill frequencies matrix with 0s.
        freqMatrix = fillEmpty(len(bigramCol), len(bigramRow))

        # Set the frequencies in corresponding cells. 
        for bigram, freq in biFreq.items():
            col = bigramRow.index(bigram[1])
            row = bigramCol.index(bigram[0])
            freqMatrix[col][row] = freq

        # Add row headers (column) to the sheet and the correspondig frequencies along with a column header.
        biDF.insert(0, "Bigram Letters", bigramCol, allow_duplicates=True)
        for i in range(len(bigramRow)):
            biDF.insert(i + 1, bigramRow[i], freqMatrix[i], allow_duplicates=True)

        return biDF

    # Create an Excel file with aggregated statistics.
    def statisticsToExcel(self) -> None:
        # MONOGRAMS : Form columns monogram -> frequency.
        monoDF = self.formMonogramDF()

        # OVERLAPPED BIGRAMS : Form matrix for overlapped bigrams -> frequencies.
        oBiDF = self.formBigramDF(overlapped=True)

        # DISTINCT BIGRAMS : Form matrix for distinct bigrams -> frequencies.
        dBiDF = self.formBigramDF(overlapped=False)

        # CONVERSION TO EXCEL
        with pd.ExcelWriter(STATICTIC_OUTPUT_FILE) as writer:
            monoDF.to_excel(writer, sheet_name="Monogram Statictic", index=False)
            oBiDF.to_excel(writer, sheet_name="Overlapped Bigram Statistic", index=False)
            dBiDF.to_excel(writer, sheet_name="Distinct Bigram Statistic", index=False)


# Fill NxM matrix (2D list) with 0s.
def fillEmpty(columns: int, rows: int) -> list[list[Decimal]]:
    matrix: list[list[Decimal]] = []
    for i in range(columns):
        matrix.append([])
        for _ in range(rows):
            matrix[i].append(Decimal(0))
    return matrix


# Remove duplicates in a list.
def removeDuplicates(lst: list) -> list:
    return list(dict.fromkeys(lst))


# Calculate frequency of each Ngram in text by dividing its occurences on total Ngram quantity.
def calculateFrequency(ngramCount: dict[str, int], totalNgrams: int) -> dict[str, Decimal]:
    # Since log(0) is undefined, we add one to the amount of each ngram
    return {ngram: Decimal(count + 1) / Decimal(totalNgrams + len(ngramCount)) for ngram, count in ngramCount.items()}


def calculateEntropy(frequencies: dict[str, Decimal]) -> Decimal:
    entropy = Decimal(0)
    for freq in frequencies.values():
        entropy -= freq * Decimal(log2(freq))
    return entropy / Decimal(len(list(frequencies.keys())[0]))


def sourceRedundancy(entropy: Decimal, symbolsCount: int) -> Decimal:
    return Decimal(1) - (entropy / Decimal(log2(symbolsCount)))


# Read text from file by blocks and process by handler.
# Handler should be object method.
def readTextWithHandler(fileName: str, handler: Callable[[str], None]):
    with open(fileName, "r") as f:
        textBlock = f.read(TEXT_BLOCK_SIZE)
        handler(textBlock)


def main():
    # CLI
    argparser = argparse.ArgumentParser(prog="Entropy calculator", 
                                    description="This script calculates the specific entropy for monograms and bigrams of the given text.",
                                    usage="main.py pathToFile")
    argparser.add_argument('path', nargs='?', help='path to text file')
    args = argparser.parse_args()
    if not args.path:
        argparser.print_help()
        exit(0)
    if not os.path.isfile(args.path):
        argparser.print_help()
        exit(0)
    fileName: str = args.path

    generalCalc = EntropyCalculator(STANDARD_ALPHABET)
    whitespacedCalc = EntropyCalculator(STANDARD_ALPHABET_WHITESPACE)

    readTextWithHandler(fileName, generalCalc.handleText)
    readTextWithHandler(fileName, whitespacedCalc.handleText)

    freqs = calculateFrequency(generalCalc.monogramCount, generalCalc.totalMonograms)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on monogram (without spaces):", entropy)
    print("Source redundancy monogram (without spaces):", sourceRedundancy(entropy, len(generalCalc.alphabet)))
    print("Monogram (without spaces) frequencys:")
    pprint.pp(sorted(freqs.items(), key=lambda item: item[1], reverse=True))

    print()

    freqs = calculateFrequency(generalCalc.overlappedBigramCount, generalCalc.totalOverlappedBigrams)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on bigram (overlapped) (without spaces):", entropy)
    print("Source redundancy bigram (overlapped) (without spaces):", sourceRedundancy(entropy, len(generalCalc.alphabet)))

    print()

    freqs = calculateFrequency(generalCalc.distinctBigramCount, generalCalc.totalDistinctBigrams)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on bigram (not overlapped) (without spaces):", entropy)
    print("Source redundancy bigram (not overlapped) (without spaces):", sourceRedundancy(entropy, len(generalCalc.alphabet)))

    print()

    freqs = calculateFrequency(whitespacedCalc.monogramCount, whitespacedCalc.totalMonograms)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on monogram character (with spaces):", entropy)
    print("Source redundancy monogram character (with spaces):", sourceRedundancy(entropy, len(whitespacedCalc.alphabet)))
    print("Monogram (with spaces) frequencys:")
    pprint.pp(sorted(freqs.items(), key=lambda item: item[1], reverse=True))

    print()

    freqs = calculateFrequency(whitespacedCalc.overlappedBigramCount, whitespacedCalc.totalOverlappedBigrams)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on monogram character (overlapped) (with spaces):", entropy)
    print("Source redundancy monogram character (overlapped) (with spaces):", sourceRedundancy(entropy, len(whitespacedCalc.alphabet)))

    print()

    freqs = calculateFrequency(whitespacedCalc.distinctBigramCount, whitespacedCalc.totalDistinctBigrams)
    entropy = calculateEntropy(freqs)
    print("Specific entropy on monogram character (not overlapped) (with spaces):", entropy)
    print("Source redundancy monogram character (not overlapped) (with spaces):", sourceRedundancy(entropy, len(whitespacedCalc.alphabet)))



if __name__ == "__main__":
    main()
