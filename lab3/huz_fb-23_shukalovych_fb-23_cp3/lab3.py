from math_operations import *
from collections import Counter

YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

#кількість біграм без перетину
def count_bigrams_no_overlap(text):
    bigrams = [text[i:i + 2] for i in range(0, len(text) - 1, 2)]
    bigram_counts = Counter(bigrams)
    return bigram_counts

#загальна кількість біграм
def count_total_bigrams(bigram_counts):
    total_bigrams = sum(bigram_counts.values())
    return total_bigrams

#частота біграм
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
def find_key_candidates(plain_bigrams, cipher_bigrams):
    m_squared = 31 * 31  # 961
    alphabet = "абвгдеежзийклмнопрстуфхцчшщыьэюя"
    letter_to_index = {letter: idx for idx, letter in enumerate(alphabet)}
    candidates = []

    def bigram_to_index(bigram):
        return letter_to_index[bigram[0]] * 31 + letter_to_index[bigram[1]]

    plain_positions = [bigram_to_index(bigram) for bigram in plain_bigrams]
    cipher_positions = [bigram_to_index(bigram) for bigram in cipher_bigrams]

    for X1 in plain_positions:
        for X2 in plain_positions:
            if X1 == X2:
                continue

            for Y1 in cipher_positions:
                for Y2 in cipher_positions:
                    if Y1 == Y2:
                        continue

                    delta_x = (X1 - X2) % m_squared
                    delta_y = (Y1 - Y2) % m_squared

                    a_solutions = solve_linear_congruence(delta_x, delta_y, m_squared)
                    if a_solutions:
                        for a in a_solutions:
                            b = (Y1 - a * X1) % m_squared
                            candidates.append((a, b))

    return candidates

def main(bigram_freq):
    while True:
        print(YELLOW + "\n♥Меню♥" + RESET)
        print("1. Математичні операції")
        print("2. П'ять найчастіших біграм")
        print("3. Співставлення частот біграм") #реалізувати меню для цього
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
            cipher_top_bigrams = list(print_top_5_bigrams(bigram_freq).keys())
            plain_top_bigrams = ["ст", "но", "то", "на", "ен"]

            candidates = find_key_candidates(plain_top_bigrams, cipher_top_bigrams)
            print("Можливі кандидати на ключі (a, b):")
            for candidate in candidates:
                print(candidate)

        elif user_choice == '4':
            print("краказябра")
        else:
            print("Неправильний вибір. Спробуйте знову.")

if __name__ == "__main__":
    with open('04.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    bigram_counts = count_bigrams_no_overlap(content)
    total_bigrams = count_total_bigrams(bigram_counts)
    bigram_freq = bigram_frequencies(bigram_counts, total_bigrams)
    main(bigram_freq)