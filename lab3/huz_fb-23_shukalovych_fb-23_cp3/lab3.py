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

def print_top_5_bigrams(bigram_frequencies):
    top_5_bigrams = dict(sorted(bigram_frequencies.items(), key=lambda x: x[1], reverse=True)[:5])

    print("Найчастіші біграми та їх частоти:")
    for bigram, frequency in top_5_bigrams.items():
        print(f"{bigram}: {frequency:.5f}")

    return top_5_bigrams

def main():
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
            with open('04.txt', 'r', encoding='utf-8') as file:
                content = file.read()
            bigram_counts = count_bigrams_no_overlap(content)
            total_bigrams = count_total_bigrams(bigram_counts)
            bigram_freq = bigram_frequencies(bigram_counts, total_bigrams)
            #print(bigram_freq)
            print_top_5_bigrams(bigram_freq)
        elif user_choice == '3':
            print("краказябра")
        elif user_choice == '4':
            print("краказябра")
        else:
            print("Неправильний вибір. Спробуйте знову.")

if __name__ == "__main__":
    main()