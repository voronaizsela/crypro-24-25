import os
import re

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


def main():
    while True:
        print(YELLOW + "\n♥Меню♥" + RESET)
        print("1. Вивести текст")
        print("2. Зашифрувати текст")
        print("3. Обчислити індекси відповідності")
        print("4. Розшифрувати текст")
        print("5. Вийти")
        
        user_choice = input("Виберіть опцію: ").strip()
        
        if user_choice == '5':
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
            print("\nФункція ще не реалізована.")
        
        elif user_choice == '4':
            print("\nФункція ще не реалізована.")
        
        else:
            print("Неправильний вибір. Спробуйте знову.")

if __name__ == "__main__":
    main()
