import math

FILENAME_WITH_WHITESPACES = "./seneka.txt"
FILENAME_WITHOUT_WHITESPACES = "./seneka_no_whitespace.txt"
ALPHABET = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'

def prepare_text(text, with_space=False):
    if with_space==True:
        text_filtered = ''.join([char.lower() for char in text if char.lower() in (ALPHABET+' ')])
        text_filtered = ' '.join(text_filtered.split())
    else:
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
    mono_entropy = 0
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
            bi_freq_counter[bigram] += 1
        else:
            bi_freq_counter[bigram] = 1

    for bigram, freq in bi_freq_counter.items():
        bi_freq_percentage[bigram] = freq/bi_counter

    return bi_freq_percentage

def calculate_bigram_entropy(bi_freq_percentage):
    bi_entropy = 0
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

    # working with file with whitespaces
    with open(FILENAME_WITH_WHITESPACES, 'r', encoding='utf-8') as file:
        text_with_whitespaces = file.read()
    
        # working with monograms
        text_with_whitespaces_filtered = prepare_text(text_with_whitespaces, with_space=True)
        mono_freq_percentage = calculate_monogram_frequencies(text_with_whitespaces_filtered)
        H1_mono_entropy = calculate_monogram_entropy(mono_freq_percentage)
        R1_mono_redundancy = calculate_monogram_redundancy(H1_mono_entropy)

        # working with bigrams with step 1
        bi_freq_percentage = calculate_bigram_frequencies(text_with_whitespaces_filtered, 1)
        H2_bi_entropy_step1 = calculate_bigram_entropy(bi_freq_percentage)
        R2_bi_redundancy_step1 = calculate_bigram_redundancy(H2_bi_entropy_step1)

        # working with bigrams with step 2
        bi_freq_percentage = calculate_bigram_frequencies(text_with_whitespaces_filtered, 2)
        H2_bi_entropy_step2 = calculate_bigram_entropy(bi_freq_percentage)
        R2_bi_redundancy_step2 = calculate_bigram_redundancy(H2_bi_entropy_step2)

        # printing required info
        print("\n^^^^ WORKING WITH FILE THAT HAS WHITESPACES ^^^^\n\n")

        # Printing monogram frequencies line by line
        print("Monogram frequencies:")
        for monogram, frequency in mono_freq_percentage.items():
            print(f"{monogram}: {frequency}")

        print(f"\nMonogram's entropy: {H1_mono_entropy}\n")

        # Printing bigram frequencies line by line (step 1)
        print("Bigram frequencies (step 1, with whitespaces):")
        for bigram, frequency in bi_freq_percentage.items():
            print(f"{bigram}: {frequency}")

        print(f"\nSTEP ONE Bigram's entropy: {H2_bi_entropy_step1}\n")
        print(f"STEP ONE Bigram's redundancy: {R2_bi_redundancy_step1}\n")

        # Printing bigram frequencies line by line (step 2)
        print("Bigram frequencies (step 2, with whitespaces):")
        for bigram, frequency in bi_freq_percentage.items():
            print(f"{bigram}: {frequency}")

        print(f"\nSTEP TWO Bigram's entropy: {H2_bi_entropy_step2}\n")
        print(f"STEP TWO Bigram's redundancy: {R2_bi_redundancy_step2}\n")
        print("-"*60)

    # working with file withOUT whitespaces
    with open(FILENAME_WITHOUT_WHITESPACES, 'r', encoding='utf-8') as file:
        text_without_whitespaces = file.read()
    
        # working with monograms
        text_without_whitespaces_filtered = prepare_text(text_without_whitespaces)
        mono_freq_percentage = calculate_monogram_frequencies(text_without_whitespaces_filtered)
        H1_mono_entropy = calculate_monogram_entropy(mono_freq_percentage)
        R1_mono_redundancy = calculate_monogram_redundancy(H1_mono_entropy)

        # working with bigrams with step 1
        bi_freq_percentage = calculate_bigram_frequencies(text_without_whitespaces_filtered, 1)
        H2_bi_entropy_step1 = calculate_bigram_entropy(bi_freq_percentage)
        R2_bi_redundancy_step1 = calculate_bigram_redundancy(H2_bi_entropy_step1)

        # working with bigrams with step 2
        bi_freq_percentage = calculate_bigram_frequencies(text_without_whitespaces_filtered, 2)
        H2_bi_entropy_step2 = calculate_bigram_entropy(bi_freq_percentage)
        R2_bi_redundancy_step2 = calculate_bigram_redundancy(H2_bi_entropy_step2)

        # printing required info
        print("\n^^^^ WORKING WITH FILE THAT HAS >NOT< WHITESPACES ^^^^\n\n")

        # Printing monogram frequencies line by line
        print("Monogram frequencies (without whitespaces):")
        for monogram, frequency in mono_freq_percentage.items():
            print(f"{monogram}: {frequency}")

        print(f"\nMonogram's entropy: {H1_mono_entropy}\n")

        # Printing bigram frequencies line by line (step 1)
        print("Bigram frequencies (step 1, without whitespaces):")
        for bigram, frequency in bi_freq_percentage.items():
            print(f"{bigram}: {frequency}")

        print(f"\nSTEP ONE Bigram's entropy: {H2_bi_entropy_step1}\n")
        print(f"STEP ONE Bigram's redundancy: {R2_bi_redundancy_step1}\n")

        # Printing bigram frequencies line by line (step 2)
        print("Bigram frequencies (step 2, without whitespaces):")
        for bigram, frequency in bi_freq_percentage.items():
            print(f"{bigram}: {frequency}")

        print(f"\nSTEP TWO Bigram's entropy: {H2_bi_entropy_step2}\n")
        print(f"STEP TWO Bigram's redundancy: {R2_bi_redundancy_step2}\n")

    return

if __name__ == "__main__":
    main()