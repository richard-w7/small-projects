import random

def load_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()

def save_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)

def generate_random_mapping():
    original_chars = list('abcdefghijklmnopqrstuvwxyz')
    used_chars = list('abcdefghijklmnopqrstuvwxyz')
    random_mapping = {}

    for char in original_chars:
        random_char = random.choice(used_chars)
        random_mapping[char] = random_char
        used_chars.remove(random_char)

    return random_mapping

def encrypt_text(text, mapping):
    result = ""
    for char in text:
        if char.isalpha():
            original_char = char.lower()
            if original_char in mapping:
                if char.isupper():
                    result += mapping[original_char].upper()
                else:
                    result += mapping[original_char]
            else:
                result += char
        else:
            result += char
    return result

def save_key(key_path, mapping):
    with open(key_path, 'w') as key_file:
        for original_char, new_char in mapping.items():
            key_file.write(f"{original_char}={new_char}\n")

def main():
    file_path = input("Enter the path to the input file: ")
    original_text = load_file(file_path)

    random_mapping = generate_random_mapping()

    encrypted_text = encrypt_text(original_text, random_mapping)
    print("Encrypted Text:")
    print(encrypted_text)

    output_path = input("Enter the path to save the encrypted text file: ")
    save_file(output_path, encrypted_text)

    key_path = output_path.rsplit('.', 1)[0] + '_key.txt'
    save_key(key_path, random_mapping)
    print(f"Key saved to {key_path}")

if __name__ == "__main__":
    main()
