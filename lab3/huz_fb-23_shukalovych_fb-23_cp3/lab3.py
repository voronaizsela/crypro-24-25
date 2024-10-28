from math_operations import *
from collections import Counter
import re

YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

def load_and_clean_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        text = text.lower()
        text = re.sub(r'[^абвгдеежзийклмнопрстуфхцчшщыьэюя]', '', text)
        return text
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено")
        return None 
    
def count_bigrams_no_overlap(text):
    bigrams = [text[i:i + 2] for i in range(0, len(text) - 1, 2)]  
    bigram_counts = Counter(bigrams)
    return bigram_counts

# Загальна кількість біграм
def count_total_bigrams(bigram_counts):
    total_bigrams = sum(bigram_counts.values())
    return total_bigrams

# Частота біграм
def bigram_frequencies(bigram_counts, total_bigrams):
    frequencies = {}
    for bigram, count in bigram_counts.items():
        frequencies[bigram] = count / total_bigrams
    return frequencies

def print_top_5_bigrams(bigram_frequencies, i=False):
    top_5_bigrams = dict(sorted(bigram_frequencies.items(), key=lambda x: x[1], reverse=True)[:5])

    if i is True:
        print("Найчастіші біграми та їх частоти:")
        for bigram, frequency in top_5_bigrams.items():
            print(f"{bigram}: {frequency:.5f}")
    else:
        return top_5_bigrams

def find_top_5_bigrams(text):
    bigram_counts = count_bigrams_no_overlap(text)
    total_bigrams = count_total_bigrams(bigram_counts)
    frequencies = bigram_frequencies(bigram_counts, total_bigrams)
    return print_top_5_bigrams(frequencies, i=False)


def affine_decrypt(ciphertext, candidates):
    decrypted_texts = []
    m = 31  
    for a, b in candidates:
        decrypted_text = []       
        
        a_inverse = pow(a, -1, m)

        for char in ciphertext:
            if char.isalpha():
                
                y = (a_inverse * (ord(char) - ord('а') - b)) % m
                decrypted_text.append(chr(y + ord('а')))
            else:
                decrypted_text.append(char)

        decrypted_texts.append((a, b, ''.join(decrypted_text)))

    return decrypted_texts


def contains_unreal_bigrams(text, unreal_bigrams):
    for i in range(len(text) - 1):
        bigram = text[i:i + 2]
        if bigram in unreal_bigrams:
            return True
    return False


def frequency_check(text, frequent_letters, rare_letters):
    text = text.lower()
    total_count = len(text)

    if total_count == 0:
        return False

    frequent_count = sum(text.count(letter) for letter in frequent_letters)
    frequent_check = frequent_count / total_count >= 0.1

    rare_count = sum(text.count(letter) for letter in rare_letters)
    rare_check = rare_count / total_count <= 0.05

    return frequent_check and rare_check


def decrypt_affine_candidates(ciphertext, candidates, unreal_bigrams):
    frequent_letters = ['о', 'а', 'е']
    rare_letters = ['ф', 'щ', 'ь']
    valid_keys = []  
    
    decrypted_results = affine_decrypt(ciphertext, candidates)

    for a, b, decrypted_text in decrypted_results:
        
        if not contains_unreal_bigrams(decrypted_text, unreal_bigrams) and frequency_check(decrypted_text, frequent_letters, rare_letters):
            valid_keys.append((a, b, decrypted_text))  
    if valid_keys:  
        for a, b, text in valid_keys:
            print(f"Змістовний текст з ключем (a={a}, b={b}): {text}")
    else:
        print("Не знайдено жодного змістовного тексту.")




def main(bigram_freq, candidates, content, unreal_bigrams):
    while True:
        print(YELLOW + "\n♥Меню♥" + RESET)
        print("1. Математичні операції")
        print("2. П'ять найчастіших біграм")
        print("3. Співставлення частот біграм") 
        print("4. Дешифрування тексту")
        print("5. Вийти")

        user_choice = input("Виберіть опцію: ").strip()

        if user_choice == '5':
            print(BLUE + " /}___/}❀\n( • . •)\n/ >    > Byeee" + RESET)
            break

        if user_choice == '1':
            while True:
                print(YELLOW + "\n-♥-Меню математичних операцій-♥-" + RESET)
                print("0. Повернутись")
                print("1. Обчислити обернений елемент(розш. алг. Евкліда)")
                print("2. Розв'язування лінійних порівнянь")

                text_choice = input("Виберіть опцію: ").strip()

                if text_choice == '1':
                    try:
                        print("\nВведіть натуральне значення для знаходження оберненого b ≡ a (mod n):")
                        a = int(input("Введіть число a: "))
                        n = int(input("Введіть модуль n: "))

                        if a <= 0 or n <= 0:
                            raise ValueError("Числа мають бути натуральними (додатними).")

                        b = extended_euclidean(a, n)
                        if b:
                            print(f"Обернений елемент числа {a} за модулем {n} дорівнює {b}")
                        else:
                            print(f"Оберненого елементу числа {a} за модулем {n} не існує.")

                    except ValueError as e:
                        print(e)

                elif text_choice == '2':
                    try:
                        print("\nВведіть значення для лінійного порівняння ax ≡ b (mod n):")
                        a = int(input("Введіть a: "))
                        b = int(input("Введіть b: "))
                        n = int(input("Введіть модуль n: "))

                        if a <= 0 or n <= 0 or b <= 0:
                            raise ValueError("Числа мають бути натуральними (додатними).")

                        solutions = solve_linear_congruence(a, b, n)
                        if solutions:
                            print("Розв'язки лінійного порівняння:", solutions)
                        else:
                            print("Порівняння не має розв'язків.")

                    except ValueError as e:
                        print(e)

                elif text_choice == '0':
                    break
                else:
                    print("Неправильний вибір. Спробуйте знову.")
        elif user_choice == '2':
            print_top_5_bigrams(bigram_freq, i=True)
        elif user_choice == '3':
            print("Можливі кандидати на ключі (a, b):")
            for candidate in candidates:
                print(candidate)

        elif user_choice == '4':
           decrypt_affine_candidates(content, candidates, unreal_bigrams)

        else:
            print("Неправильний вибір. Спробуйте знову.")

if __name__ == "__main__":
    content = load_and_clean_text('04.txt')
    bigram_counts = count_bigrams_no_overlap(content)
    total_bigrams = count_total_bigrams(bigram_counts)
    bigram_freq = bigram_frequencies(bigram_counts, total_bigrams)
    cipher_top_bigrams = list(print_top_5_bigrams(bigram_freq).keys())
    plain_top_bigrams = ['ст', 'но', 'то', 'на', 'ен']
    candidates = find_key_candidates(plain_top_bigrams, cipher_top_bigrams)
    unreal_bigrams = ['аь', 'уь', 'яь', 'юь', 'еь', 'оь', 'йь', 'ыь', 'иь', 'эь', 'ъд']
    main(bigram_freq, candidates, content, unreal_bigrams)