from typing import Callable

# 1 << 16 = 64KB
TEXT_BLOCK_SIZE = 1 << 16
FILE_NAME = ""

class EntropyCalculator:
    alphabet: set
    up2low: dict[str, str]

    monogramCount: dict[str, int]
    totalMonograms: int

    notOverlappedBigramCount: dict[str, int]
    totalNotOverlappedBigrams: int

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
