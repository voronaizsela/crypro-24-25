import math

FILENAME_WITH_WHITESPACES = "./seneka.txt"
FILENAME_WITHOUT_WHITESPACES = "./seneka_no_whitespace.txt"
ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def prepare_text(text):
    text_filtered = ''.join([char.lower() for char in text if char.lower() in ALPHABET])
    text_filtered = ' '.join(text_filtered.split())
    return text_filtered

def calculate_monogram_frequencies(text_filtered):
    mono_freq_percentage = {}
    mono_freq_counter = {}
    mono_counter = 0
    for i in range(0, len(text_filtered), 1):
        monogram = text_filtered[i:i+1]
        mono_counter += 1
        if monogram in mono_freq_counter:
            mono_freq_counter[monogram] += 1
        else:
            mono_freq_counter[monogram] = 1

    for monogram, freq in mono_freq_counter.items():
        mono_freq_percentage[monogram] = freq/mono_counter

    return mono_freq_percentage

def calculate_monogram_entropy(mono_freq_percentage):
    mono_entropy = None
    for freq in mono_freq_percentage.values():
        if not freq:
            continue
        mono_entropy += (math.log2(freq))*freq
    mono_entropy = (-1) * mono_entropy
    return mono_entropy

def calculate_monogram_redundancy(mono_entropy):
    mono_redundancy = 1-(mono_entropy / math.log2(len(ALPHABET)))
    return mono_redundancy

def calculate_bigram_frequencies(text_filtered, step):
    bi_freq_percentage = {}
    bi_freq_counter = {}
    bi_counter = 0
    for i in range(0, len(text_filtered)-1, step):
        bigram = text_filtered[i:i+2]
        bi_counter += 1
        if bigram in bi_freq_counter:
            bi_freq_counter[monogram] += 1
        else:
            bi_freq_counter[monogram] = 1

    for monogram, freq in bi_freq_counter.items():
        bi_freq_percentage[monogram] = freq/bi_counter

    return bi_freq_percentage

def calculate_bigram_entropy(bi_freq_percentage):
    bi_entropy = None
    for freq in bi_freq_percentage.values():
        if not freq:
            continue
        bi_entropy += (math.log2(freq))*freq
    bi_entropy = ((-1) * bi_entropy)/2
    return bi_entropy

def calculate_bigram_redundancy(bi_entropy):
    bi_redundancy = 1-(bi_entropy / math.log2(len(ALPHABET)))
    return bi_redundancy

def main():

    with open(FILENAME_WITH_WHITESPACES, 'r', encoding='utf-8') as file:
        text_with_whitespaces = file.read()
    
    text_filtered = prepare_text(text_with_whitespaces)
    

if __name__ == "__main__":
    main()