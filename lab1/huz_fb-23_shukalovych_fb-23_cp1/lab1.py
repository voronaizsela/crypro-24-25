import re
from collections import Counter
import math

YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"


def clean_text():
    with open('lab1.txt', 'r', encoding='utf-8') as file:
        content = file.read()
    content = content.lower()
    cleaned = re.sub(r'[^а-я\s]+', '', content)
    cleaned = re.sub(r'\s+', ' ', cleaned)
    cleaned = cleaned.strip()
    return cleaned


def count_letters(text):
    letter_counts = Counter(re.findall(r'[а-я]', text))
    return letter_counts


def total_letter_count(letter_counts):
    return sum(letter_counts.values())


def letter_frequencies(letter_counts, total_count):
    frequencies = {}
    for letter, count in letter_counts.items():
        frequencies[letter] = count / total_count
    sorted_frequencies = dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))
    return sorted_frequencies


def count_letters_with_spaces(text):
    letter_counts_with_spaces = Counter(text)
    return letter_counts_with_spaces


def total_letter_count_with_spaces(letter_counts_with_spaces):
    return sum(letter_counts_with_spaces.values())


def letter_frequencies_with_spaces(letter_counts_with_spaces, total_count_with_spaces):
    frequencies = {}
    for letter, count in letter_counts_with_spaces.items():
        frequencies[letter] = count / total_count_with_spaces
    sorted_frequencies_with_spaces = dict(sorted(frequencies.items(), key=lambda item: item[1], reverse=True))
    return sorted_frequencies_with_spaces


def remove_spaces(text):
    return text.replace(" ", "")


def count_bigrams(text):
    bigrams = [text[i:i + 2] for i in range(len(text) - 1)]
    bigram_counts = Counter(bigrams)
    return bigram_counts


def bigram_frequencies(bigram_counts, total_bigrams):
    frequencies = {}
    for bigram, count in bigram_counts.items():
        frequencies[bigram] = count / total_bigrams
    return frequencies


def print_bigram_table(bigram_counts):
    formatted_bigrams = []
    for bigram, count in bigram_counts.items():
        formatted_bigrams.append(f'"{bigram}" - {count}')
    print("\nКількість біграм:")
    for i in range(0, len(formatted_bigrams), 8):
        print("  ".join(formatted_bigrams[i:i + 8]))


def print_bigram_frequencies(bigram_frequencies):
    formatted_frequencies = []
    for bigram, frequency in bigram_frequencies.items():
        formatted_frequencies.append(f'"{bigram}" - {frequency:.5f}')
    print("\nЧастота біграм:")
    for i in range(0, len(formatted_frequencies), 8):
        print("  ".join(formatted_frequencies[i:i + 8]))


def entropy_H1(letter_frequencies):
    entropy_value = 0
    for p_i in letter_frequencies.values():
        if p_i > 0:
            entropy_value -= p_i * math.log2(p_i)

    return entropy_value


def text_processing_menu(cleaned):
    while True:
        print(YELLOW + "\n-♥- Обробка тексту -♥-" + RESET)
        print("1. Вивести текст з пробілами")
        print("2. Вивести текст без пробілів")
        print("3. Повернутись до головного меню")

        choice = input("Введіть номер опції: ")

        if choice == '1':
            print("\nТекст з пробілами:")
            print(cleaned)
        elif choice == '2':
            print("\nТекст без пробілів:")
            print(remove_spaces(cleaned))
        elif choice == '3':
            break
        else:
            print("Неправильний вибір, будь ласка, спробуйте ще раз.")


def letter_processing_menu(letter_counts, total_count, letter_counts_with_spaces, total_count_with_spaces):
    while True:
        print(YELLOW + "\n-♥- Аналіз літер -♥-" + RESET)
        print("1. Вивести кількість літер без пробілів")
        print("2. Вивести частоту літер без пробілів")
        print("3. Вивести кількість літер з пробілами")
        print("4. Вивести частоту літер з пробілами")
        print("5. Повернутись до головного меню")

        choice = input("Введіть номер опції: ")

        if choice == '1':
            print("\nКількість літер:")
            for letter, count in letter_counts.items():
                print(f"{letter}: {count}")
            print(f"Загальна кількість літер: {total_count}")
        elif choice == '2':
            frequencies = letter_frequencies(letter_counts, total_count)
            print("\nЧастота літер:")
            for letter, frequency in frequencies.items():
                print(f"Частота літери '{letter}': {frequency}")
        elif choice == '3':
            print("\nКількість літер:")
            for letter, count in letter_counts_with_spaces.items():
                print(f"{letter}: {count}")
            print(f"Загальна кількість символів: {total_count_with_spaces}")
        elif choice == '4':
            frequencies_with_spaces = letter_frequencies_with_spaces(letter_counts_with_spaces, total_count_with_spaces)
            print("\nЧастота літер:")
            for letter, frequency in frequencies_with_spaces.items():
                print(f"Частота символу '{letter}': {frequency}")
        elif choice == '5':
            break
        else:
            print("Неправильний вибір, будь ласка, спробуйте ще раз.")


def bigram_processing_menu(cleaned):
    while True:
        print(YELLOW + "\n-♥- Аналіз біграм -♥-" + RESET)
        print("1. Вивести кількість біграм з перетином")
        print("2. Вивести кількість біграм без перетину")
        print("3. Вивести частоту біграм з перетином")
        print("4. Вивести частоту біграм без перетину")
        print("5. Повернутись до головного меню")

        choice = input("Введіть номер опції: ")

        if choice == '1':
            bigram_counts = count_bigrams(cleaned)
            print_bigram_table(bigram_counts)
            print(f"Загальна кількість біграм: {sum(bigram_counts.values())}")
        elif choice == '2':
            print('xi')
        elif choice == '3':
            bigram_counts = count_bigrams(cleaned)
            total_bigrams = sum(bigram_counts.values())
            bigram_frequencies_table = bigram_frequencies(bigram_counts, total_bigrams)
            print_bigram_frequencies(bigram_frequencies_table)
        elif choice == '4':
            print('xi')
        elif choice == '5':
            break
        else:
            print("Неправильний вибір, будь ласка, спробуйте ще раз.")


def entropy_menu(letter_frequencies, letter_frequencies_with_spaces):
    while True:
        print(YELLOW + "\n-♥- Ентропія -♥-" + RESET)
        print("1. H1 з пробілами")
        print("2. H1 без пробілів")
        print("3. H2 з пробілами, з перетинами")
        print("4. H2 без пробілів, з перетинами")
        print("5. H2 з проблілами, без перетинів")
        print("6. H2 без проблілами, без перетинів")
        print("7. Повернутись до головного меню")

        choice = input("Введіть номер опції: ")

        if choice == '1':
            h1_with_spaces = entropy_H1(letter_frequencies_with_spaces)
            print(f"\nЕнтропія H1 (з пробілами): {h1_with_spaces:.5f}")
        elif choice == '2':
            h1_without_spaces = entropy_H1(letter_frequencies)
            print(f"\nЕнтропія H1 (без пробілів): {h1_without_spaces:.5f}")
        elif choice == '3':
            print('xi')
        elif choice == '4':
            print('xi')
        elif choice == '5':
            print('xi')
        elif choice == '6':
            print('xi')
        elif choice == '7':
            break
        else:
            print("Неправильний вибір, будь ласка, спробуйте ще раз.")


def main():
    cleaned = clean_text()
    letter_counts = count_letters(cleaned)
    total_count = total_letter_count(letter_counts)

    letter_frequencies_dict = letter_frequencies(letter_counts, total_count)

    # Нові обчислення для тексту з пробілами
    letter_counts_with_spaces = count_letters_with_spaces(cleaned)
    total_count_with_spaces = total_letter_count_with_spaces(letter_counts_with_spaces)

    letter_frequencies_with_spaces_dict = letter_frequencies_with_spaces(letter_counts_with_spaces,
                                                                         total_count_with_spaces)

    while True:
        print(YELLOW + "\n♥Меню♥" + RESET)
        print("1. Обробка тексту")
        print("2. Аналіз літер")
        print("3. Аналіз біграм")
        print("4. Ентропія")
        print("7. Вийти")

        choice = input("Введіть номер опції: ")

        if choice == '1':
            text_processing_menu(cleaned)
        elif choice == '2':
            letter_processing_menu(letter_counts, total_count, letter_counts_with_spaces, total_count_with_spaces)
        elif choice == '3':
            bigram_processing_menu(cleaned)
        elif choice == '4':
            entropy_menu(letter_frequencies_dict, letter_frequencies_with_spaces_dict)
        elif choice == '7':
            print(BLUE + " /}___/}❀\n( • . •)\n/ >    > Byeee" + RESET)
            break
        else:
            print("Неправильний вибір, будь ласка, спробуйте ще раз.")


if __name__ == "__main__":
    main()
