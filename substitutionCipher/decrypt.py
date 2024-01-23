import os

def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def print_frequency(text):
    standard = {'e':12.7, 't':9.1, 'a':8.2, 'o':7.5, 'i':7.0, 'n':6.7, 's':6.3, 'h':6.1, 'r':6.0, 'd':4.3, 'l':4.0,
                'c':2.8, 'u':2.8, 'm':2.4, 'w':2.4, 'f':2.2, 'g':2.0, 'y':2.0, 'p':1.9, 'b':1.5, 'v':0.98, 'k':0.77,
                'j':0.15, 'x':0.15, 'q':0.095, 'z':0.074}
    frequency = {}
    for char in text:
        if char.isalpha():
            char = char.lower()
            frequency[char] = frequency.get(char, 0) + 1
    print("\nLetter Frequencies:\tStandard Frequencies:")
    total_chat = sum(frequency.values())
    sorted_frequency = dict(sorted(frequency.items(), key=lambda x: x[1], reverse=True))

    missing_letters = set(list(standard.keys())) - set(list(sorted_frequency.keys()))
    missing_letters_list = list(missing_letters)

    for letters in missing_letters_list:
            sorted_frequency[letters] = 0
    i = 0
    for char, count in sorted_frequency.items():
        curr = list(standard.keys())[i]
        print(f"{char}: {count} ({round(count/total_chat*100, 2)}%)\t\t{curr}: {standard.get(curr)}%")
        i += 1
    return list(map(str.lower,sorted_frequency.keys())), list(map(str.lower, standard.keys()))

def substitution_cipher(text, swap_table):
    result = ""
    for char in text:
        if char.isalpha():
            original_char = char.lower()
            if original_char in swap_table:
                if char.isupper():
                    result += swap_table[original_char].upper()
                else:
                    result += swap_table[original_char]
            else:
                result += char
        else:
            result += char
    return result

def main():
    file_path = input("Enter the path to the encrypted text file: ")
    
    key_option = input("Do you have a key for decryption? (yes/no): ").lower()

    if key_option == 'yes':
        key_path = input("Enter the path to the key file: ")
        key_content = load_file(key_path)
        key_lines = key_content.strip().split('\n')

        swap_table = {}
        for line in key_lines:
            original_char, new_char = line.split('=')
            swap_table[new_char.lower()] = original_char.lower()

        encrypted_text = load_file(file_path)
        decrypted_text = substitution_cipher(encrypted_text, swap_table)

        output_path = input("Enter the path to save the decrypted text file: ")
        with open(output_path, 'w') as output_file:
            output_file.write(decrypted_text)

        print("Decrypted text saved successfully.")
        exit()
    else:
        original_text = load_file(file_path)
        
        exp, sta = print_frequency(original_text)

        auto_fill = input("Do you want to auto-swap based on letter frequencies? (yes/no): ").lower()

        if auto_fill == 'yes':
            original_text = substitution_cipher(original_text, dict(zip(exp, sta)))
            print(f"\nAuto-swapped text:")
            print(original_text)
        else:
            print("\nOriginal Text:")
            print(original_text)
            
        swap_table = {}
        while True:
            swap_input = input("Enter a substitution (e.g., 'y=a'), type 'done' to finish: ")
            
            if swap_input.lower() == 'done':
                break

            if '=' not in swap_input:
                print("Invalid input. Please use the format 'y=a'")
                continue

            original_char, new_char = swap_input.split('=')

            if len(original_char) != 1 or len(new_char) != 1:
                print("Invalid input. Please use the format 'y=a'")
                continue

            swap_table[original_char.lower()] = new_char.lower()

            updated_text = substitution_cipher(original_text, swap_table)
            print(f"\nUpdated Text: (Swapped {original_char} with {new_char})")
            print(updated_text)
            print()

        output_path = input("Enter the path to save the updated text file: ")
        with open(output_path, 'w') as output_file:
            output_file.write(substitution_cipher(original_text, swap_table))

        print("Updated text saved successfully.")

if __name__ == "__main__":
    main()
