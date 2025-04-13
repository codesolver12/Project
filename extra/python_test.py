from collections import defaultdict

# Define the cipher dictionary
cipher = {'A': 'Z', 'B': 'Y', 'C': 'X', 'D': 'W', 'E': 'V', 'F': 'U', 'G': 'T', 'H': 'S', 'I': 'R', 'J': 'Q',
          'K': 'P', 'L': 'O', 'M': 'N', 'N': 'M', 'O': 'L', 'P': 'K', 'Q': 'J', 'R': 'I', 'S': 'H', 'T': 'G',
          'U': 'F', 'V': 'E', 'W': 'D', 'X': 'C', 'Y': 'B', 'Z': 'A'}

def encrypt_word(word, key, math_operation):
    # Check if the word is in capitals
    if word.islower():
        print("Word should be in capitals")
        return

    # Check if the key is a valid number
    try:
        key = int(key)
    except ValueError:
        print("Enter valid key")
        return

    # Check if the math operation is valid
    if math_operation not in ['addition', 'subtraction']:
        print("Invalid Operation")
        return

    encrypted_word = ""
    ascii_values = []

    for char in word:
        # Check if the character is a valid letter
        if char.isalpha() and char.isupper():
            # Check if the character is in the cipher dictionary
            if char in cipher:
                encrypted_char = cipher[char]
                encrypted_word += encrypted_char
                ascii_value = ord(encrypted_char)

                # Apply the math operation based on user input
                if math_operation == 'addition':
                    new_ascii = ascii_value + key
                elif math_operation == 'subtraction':
                    new_ascii = ascii_value - key

                ascii_values.append(new_ascii)
            else:
                print("Enter valid key")
                return
        else:
            encrypted_word += char

    print("".join(chr(value) for value in ascii_values))


key = input()
math_operation = input()
word_to_encrypt = input()



encrypt_word(word_to_encrypt, key, math_operation)
