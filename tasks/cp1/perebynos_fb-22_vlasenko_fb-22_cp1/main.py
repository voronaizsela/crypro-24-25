from typing import Callable
import pandas as pd
from math import log2

# 1 << 16 = 64KB
TEXT_BLOCK_SIZE = 1 << 16
FILE_NAME = ""
STATICTIC_OUTPUT_FILE = "mono.xlsx"

class EntropyCalculator:
    alphabet: set
    up2low: dict[str, str]

    monogramCount: dict[str, int]
    totalMonograms: int

    distinctBigramCount: dict[str, int]
    totalDisctinctBigrams: int

    overlappedBigramCount: dict[str, int]
    totalOverlappedBigrams: int

    # Alphabet is dictionary uppercase -> lowercase
    # \x00 in uppercase mean that character which not included in alphabet
    # can be interpreted as \x00 lowercase. Sequences of \x00 counts as 1 symbol
    def __init__(self, _alphabet: dict[str, str]):
        self.alphabet = set(_alphabet.values())
        self.up2low = _alphabet

    def handleText(self, text: str):
        pass

    # Create a DataFrame for monogram frequencies.
    def formMonogramDF(self) -> pd.DataFrame:
        monoDF = pd.DataFrame()
        monoFreq = calculateFrequency(self.monogramCount, self.totalMonograms)

        monogramCol: list[str] = []
        freqCol: list[int] = []

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
        biFreq: dict[str, int] = {}
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
def fillEmpty(columns: int, rows: int) -> list[list[int]]:
    matrix: list[list[int]] = []
    for i in range(columns):
        matrix.append([])
        for _ in range(rows):
            matrix[i].append(0)
    return matrix

# Remove duplicates in a list.
def removeDuplicates(lst: list) -> list:
    return list(dict.fromkeys(lst))

# Calculate frequency of each Ngram in text by dividing its occurences on total Ngram quantity.
def calculateFrequency(NgramCount: dict[str, int], totalNgrams: int) -> dict[str, int]:
    frequencies: dict[str, int] = {}
    for ngram, count in NgramCount.items():
        frequencies[ngram] = count / totalNgrams
    return dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))


def calculateEntropy(frequencies: dict[str, int]) -> int:
    entropy: int = 0
    for freq in frequencies.values():
        entropy -= freq * log2(freq)
    return entropy


# Read text from file by blocks and process by handler.
# Handler should be object method.
def readTextWithHandler(_fileName: str, _handler: Callable[[str]]):
    with open(_fileName, "r") as f:
        textBlock = f.read(TEXT_BLOCK_SIZE)
        _handler(textBlock)


def main():
    standardAlphabet = {
        "А": "а", "Б": "б", "В": "в", "Г": "г", "Д": "д", "Е": "е", "Ж": "ж", "З": "з", "И": "и", "Й": "й", "К": "к",
        "Л": "л", "М": "м", "Н": "н", "О": "о", "П": "п", "Р": "р", "С": "с", "Т": "т", "У": "у", "Ф": "ф", "Х": "х",
        "Ц": "ц", "Ч": "ч", "Ш": "ш", "Щ": "щ", "Ы": "ы", "Ь": "ь", "Э": "э", "Ю": "ю", "Я": "я"
    }

    standardAlphabetWhitespace = {
        "А": "а", "Б": "б", "В": "в", "Г": "г", "Д": "д", "Е": "е", "Ж": "ж", "З": "з", "И": "и", "Й": "й", "К": "к",
        "Л": "л", "М": "м", "Н": "н", "О": "о", "П": "п", "Р": "р", "С": "с", "Т": "т", "У": "у", "Ф": "ф", "Х": "х",
        "Ц": "ц", "Ч": "ч", "Ш": "ш", "Щ": "щ", "Ы": "ы", "Ь": "ь", "Э": "э", "Ю": "ю", "Я": "я", "\x00": " "
    }

    whitespacedCalc = EntropyCalculator(standardAlphabetWhitespace)
    readTextWithHandler(FILE_NAME, whitespacedCalc.handleText)


if __name__ == "__main__":
    main()
