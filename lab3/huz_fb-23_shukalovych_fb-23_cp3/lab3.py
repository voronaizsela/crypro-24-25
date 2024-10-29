from collections import Counter
import re
from math_operations import *

YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

# Завантаження та очищення тексту
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

# Підрахунок біграм без перетинання
def count_bigrams_no_overlap(text):
    bigrams = [text[i:i + 2] for i in range(0, len(text) - 1, 2)]  
    bigram_counts = Counter(bigrams)
    return bigram_counts

# Загальна кількість біграм
def count_total_bigrams(bigram_counts):
    return sum(bigram_counts.values())

# Частота біграм
def bigram_frequencies(bigram_counts, total_bigrams):
    frequencies = {bigram: count / total_bigrams for bigram, count in bigram_counts.items()}
    return frequencies

# Виведення топ-5 біграм
def print_top_5_bigrams(bigram_frequencies, i=False):
    top_5_bigrams = dict(sorted(bigram_frequencies.items(), key=lambda x: x[1], reverse=True)[:5])
    if i:
        print("Найчастіші біграми та їх частоти:")
        for bigram, frequency in top_5_bigrams.items():
            print(f"{bigram}: {frequency:.5f}")
    else:
        return top_5_bigrams

# Знаходження кандидатів для ключів
def keys_find(cipher_bigrams, plain_bigrams):
    m = 31
    keys = []
    for i in range(len(cipher_bigrams) - 1):
        for j in range(i + 1, len(cipher_bigrams)):
            y1 = cipher_bigrams[i]
            y2 = cipher_bigrams[j]
            x1 = plain_bigrams[i]
            x2 = plain_bigrams[j]
            diff_y = (y1 - y2) % (m ** 2)
            diff_x = (x1 - x2) % (m ** 2)
            a_candidates = solve_linear_congruence(diff_x, diff_y, m ** 2)
            for a in a_candidates:
                b = (y1 - a * x1) % (m ** 2)
                keys.append((a, b))
    return keys

alphabet = 'абвгдежзийклмнопрстуфхцчшщыьэюя'


def main(bigram_freq, content, unreal_bigrams):
    candidates = [] 
    ciphertext = content  
    forbidden_bigrams = ['аь', 'оь', 'еь', 'иь'] 
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
            cipher_top_bigrams = list(print_top_5_bigrams(bigram_freq).keys())
            plain_top_bigrams = ['ст', 'но', 'то', 'на', 'ен']
            cipher_bigrams = [31 * alphabet.index(bigram[0]) + alphabet.index(bigram[1]) for bigram in cipher_top_bigrams]
            plain_bigrams = [31 * alphabet.index(bigram[0]) + alphabet.index(bigram[1]) for bigram in plain_top_bigrams]
            candidates = keys_find(cipher_bigrams, plain_bigrams)  # Зберігаємо кандидатів
            for candidate in candidates:
                print(candidate)

        elif user_choice == '4':
            if candidates:
                pass
            else:
                print("Кандидати для ключів не знайдені.")
        else:
            print("Неправильний вибір. Спробуйте знову.")

if __name__ == "__main__":
    content = load_and_clean_text('04.txt')
    bigram_counts = count_bigrams_no_overlap(content)
    total_bigrams = count_total_bigrams(bigram_counts)
    bigram_freq = bigram_frequencies(bigram_counts, total_bigrams)
    main(bigram_freq, content, [])
