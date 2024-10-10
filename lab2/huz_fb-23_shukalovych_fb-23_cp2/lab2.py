import os
import re
from collections import Counter
import matplotlib.pyplot as plt

YELLOW = "\033[93m"
BLUE = "\033[94m"
RESET = "\033[0m"

#шифр Віженера
def vigenere(plaintext, key):
    cipher_text = []
    key_length = len(key)
    alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
    for i, char in enumerate(plaintext):
        if char.islower():
            key_char = key[i % key_length].lower()  
            shift = alphabet.index(key_char)  # Отримаємо зсув за ключем
            encrypted_char = alphabet[(alphabet.index(char) + shift) % 33]
            cipher_text.append(encrypted_char)
    return ''.join(cipher_text)

#зробили так, щоб текст був неперервним
def load_and_clean_text(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            text = file.read()
        text = text.lower()
        text = re.sub(r'[^а-яё]', '', text)
        return text
    except FileNotFoundError:
        print(f"Файл '{file_path}' не знайдено")
        return None

#функція для обрахунку індекса відповідності
def index_of_coincidence(text):
    letter_counts = Counter(text)
    n = sum(letter_counts.values())

    total_sum = sum(Nt * (Nt - 1) for Nt in letter_counts.values())
    index = total_sum / (n * (n - 1))

    return index

#функція для обрахунку індексів відп. для усіх значень ключа шифр.
def calculate_indexes_for_keys(*key_ranges):
    ic_dict = {}

    for key_range in key_ranges:
        for key_choice in key_range:
            try:
                with open(f"lab2/encrypted_{key_choice}.txt", 'r', encoding='utf-8') as file:
                    content = file.read()
                    ic_value = index_of_coincidence(content)
                    ic_dict[key_choice] = ic_value
            except FileNotFoundError:
                #print(f"Файл 'encrypted_{key_choice}.txt' не знайдено.")
                ic_dict[key_choice] = None

    return ic_dict

#побудова гістаграми
def plot_histogram(data):
    filtered_data = {k: v for k, v in data.items() if v is not None}

    if not filtered_data:
        print("Немає значень для побудови гістограми.")
        return
    #print(filtered_data)
    keys = list(filtered_data.keys())
    values = list(filtered_data.values())

    plt.figure(figsize=(10, 6))
    plt.bar(keys, values, color='pink')

    plt.title('Гістограма індексів відповідності')
    plt.xlabel('r')
    plt.ylabel('I')

    plt.tight_layout()
    plt.show()


def main(ic_results):
    while True:
        print(YELLOW + "\n♥Меню♥" + RESET)
        print("1. Вивести текст")
        print("2. Зашифрувати текст")
        print("3. Обчислити індекси відповідності")
        print("4. Розшифрувати текст")
        print("5. Діаграми")
        print("6. Вийти")
        
        user_choice = input("Виберіть опцію: ").strip()
        
        if user_choice == '6':
            print(BLUE + " /}___/}❀\n( • . •)\n/ >    > Byeee" + RESET)
            break
        
        if user_choice == '1':
            while True:
                print(YELLOW + "\n-♥-Меню виведення тексту-♥-" + RESET)
                print("0. Повернутись")
                print("1. Вивести текст")
                print("2. Вивести текст за варіантом")
                    
                text_choice = input("\nВиберіть опцію: ").strip()
                
                if text_choice == '1':
                    file_path = "lab2.1.txt"
                    text = load_and_clean_text(file_path)
                    if text:
                        print(f"\nОригінальний текст:\n{text}")
                
                elif text_choice == '2':
                    file_path = "lab2.2.txt"
                    text = load_and_clean_text(file_path)
                    if text:
                        print(f"\nОригінальний текст::\n{text}")
                
                elif text_choice == '0':
                    break  
                else:
                    print("Неправильний вибір. Спробуйте знову.")
        
        elif user_choice == '2':
            print(YELLOW + "\n-♥-Введіть довжину ключа для шифрування-♥-" + RESET + '\nМожливі довжини ключа: 2-5, 10-20')
            
            while True:
                key_choice = input("\nВведіть довжину ключа або '0' для повернення: ").strip()
                if key_choice == '0':
                    break
                
                # Ключі для шифрування
                encryption_keys = {'2': 'хи', '3': 'мяу', '4': 'сова', '5': 'осень',  
                                   '10': 'абитуриент', '11': 'бессмертный', '12': 'концентратор',
                                   '13': 'глазированный', '14': 'мультипликатив', '15': 'ухлёстывавшийся',
                                   '16': 'христадельфианин', '17': 'яфетидологический', 
                                   '18': 'задокументировавши', '19': 'жизнеобеспечивающий',  
                                   '20': 'евростандартизировав'}

                key = encryption_keys.get(key_choice)
                
                if not key:
                    print(f"Неправильний вибір '{key_choice}'. Спробуйте знову.")
                    continue  

                plaintext = load_and_clean_text("lab2.1.txt" )
                cipher_text = vigenere(plaintext, key)
                print(f"\nЗашифрований текст:\n{cipher_text}")

                directory = "lab2"
                if not os.path.exists(directory):
                    os.makedirs(directory)
                output_file = os.path.join(directory, f"encrypted_{key_choice}.txt")
                with open(output_file, 'w', encoding='utf-8') as file:
                    file.write(cipher_text)

                print(f"\nЗашифрований текст збережено у '{output_file}'")
                
        elif user_choice == '3':
            print(
                YELLOW + "\n-♥-Введіть довжину ключа для знаходження індексу відповідності-♥-" + RESET + '\nМожливі довжини ключа: 2-5, 10-20')

            while True:
                key_choice = int(input("\nВведіть довжину ключа або '0' для повернення: "))
                if key_choice == 0:
                    break

                if key_choice in ic_results and ic_results[key_choice] is not None:
                    print(f'\nІндекс відповідності для ключа :) {key_choice}: {ic_results[key_choice]}')
                else:
                    try:
                        with open(f"lab2/encrypted_{key_choice}.txt", 'r', encoding='utf-8') as file:
                            content = file.read()
                            ic_value = index_of_coincidence(content)
                            ic_results[key_choice] = ic_value
                            print(f'\nІндекс відповідності для ключа {key_choice}: {ic_value}')
                    except FileNotFoundError:
                        print(f"Файл 'encrypted_{key_choice}.txt' не знайдено. Зашифруйте спочатку текст з відповідним ключем.")

        elif user_choice == '4':
                print("\nФункція ще не реалізована.")

        elif user_choice == '5':
            while True:
                print(YELLOW + "\n-♥-Меню виведення діаграм-♥-" + RESET)
                print("0. Повернутись")
                print("1. Діаграма в1")
                print("2. Діаграма в2")

                dia_choice = input("\nВиберіть опцію: ").strip()

                if dia_choice == '1':
                    plot_histogram(ic_results)
                elif dia_choice == '2':
                    print("краказябра")
                elif dia_choice == '0':
                    break
                else:
                    print("Неправильний вибір. Спробуйте знову.")
        else:
                print("Неправильний вибір. Спробуйте знову.")

if __name__ == "__main__":
    ic_results = calculate_indexes_for_keys(range(2, 6), range(10, 21))
    main(ic_results)
