import os

def load_words(file_path):
    """Load words from a file, one word per line."""
    with open(file_path, 'r') as file:
        return [line.strip() for line in file]

def letters_to_numbers(words):
    """Convert letters to bracketed numbers and keep digits in parentheses."""
    mapping = {chr(i + 96): f'[{i}]' for i in range(1, 27)}  # Map letters to bracketed numbers
    numerical_words = []
    
    for word in words:
        numerical_word = ''.join(mapping.get(char, f'({char})') for char in word)  # Convert letters and keep digits in ()
        numerical_words.append(numerical_word)
    
    return numerical_words

def save_to_file(numerical_words, output_file_path):
    """Save numerical words to a file."""
    with open(output_file_path, 'w') as file:
        for num_word in numerical_words:
            file.write(f"{num_word}\n")

def main():
    # Prompt the user for the input file path
    file_path = input("Enter the path of the file with words (one word per line): ").strip()

    if not os.path.exists(file_path):
        print("File not found. Please check the path and try again.")
        return

    # Load words from the file
    words = load_words(file_path)
    print("\nOriginal Words:")
    for word in words:
        print(word)

    # Convert letters to numbers
    numerical_words = letters_to_numbers(words)
    print("\nNumerical Representation:")
    for num_word in numerical_words:
        print(num_word)  # Print numerical representation

    # Save the numerical representation to a file
    output_file_path = 'vaihe1.txt'  # Output file name
    save_to_file(numerical_words, output_file_path)
    print(f"\nSaved numerical representation to: {output_file_path}")

if __name__ == "__main__":
    main()
