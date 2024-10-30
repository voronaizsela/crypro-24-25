import random
import pandas as pd
import seaborn as sns
from collections import Counter
import matplotlib.pyplot as plt

class CryptoConstants:
    def __init__(self):
        self.alphabet = 'абвгдежзийклмнопрстуфхцчшщъыьэюя'
        self.letter_frequencies = {
            'о': 0.1106464800, 'а': 0.0863823704, 'е': 0.0812994808, 'и': 0.0684,
            'т': 0.0602991214, 'л': 0.0525426988, 'с': 0.0506917913, 'р': 0.0474,
            'к': 0.0365767408, 'у': 0.0300542565, 'м': 0.0300107844, 'п': 0.0284,
            'г': 0.0191527960, 'я': 0.0190691959, 'з': 0.0177767374, 'ь': 0.0177,
            'ч': 0.0159024219, 'б': 0.0154860931, 'й': 0.0117224140, 'ж': 0.0090,
            'х': 0.0082279275, 'ю': 0.0052801859, 'щ': 0.0035379587, 'ц': 0.0033,
            'ф': 0.0021602281, 'ъ': 0.0003210246
        }

class TextProcessor:
    def __init__(self):
        self.constants = CryptoConstants()
        
    def read_text(self, filename):
        try:
            with open(filename, 'r', encoding='utf-8') as file:
                return file.read().lower()
        except FileNotFoundError:
            raise FileNotFoundError(f"Файл {filename} не знайдено")

    def generate_random_text(self, original_text, size, min_length=20, max_length=50):
        if not original_text:
            raise ValueError("Вхідний текст порожній")
            
        fragments = [
            original_text[i:i+length]
            for length in range(min_length, max_length + 1)
            for i in range(len(original_text) - length + 1)
        ]
        
        if not fragments:
            return ""
            
        num_fragments = size // min_length
        random_text = ''.join(random.choice(fragments) for _ in range(num_fragments))
        return random_text[:size]

    def generate_keys(self, lengths):
        return [''.join(random.choice(self.constants.alphabet)
                for _ in range(length)) for length in lengths]