import re

def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def number_to_letter(num):
    # Convert number to letter (1=a, 2=b, ..., 26=z, 27=a, ...)
    return chr(((num - 1) % 26) + ord('a'))

def loop_number(num):
    # Loop the number in the range of 0-9
    return num % 10

def convert_numbers_to_letters(lines):
    converted_lines = []
    for line in lines:
        # Replace numbers in brackets with letters
        line = re.sub(r'\[(\d+)\]', lambda m: number_to_letter(int(m.group(1))), line)
        # Replace looped numbers in parentheses
        line = re.sub(r'\((\d+)\)', lambda m: str(loop_number(int(m.group(1)))), line)
        converted_lines.append(line)
    return converted_lines

def save_to_file(file_path, converted_lines):
    with open(file_path, 'w') as file:
        for line in converted_lines:
            file.write(line + '\n')

def main():
    input_file_path = 'vaihe4.txt'
    output_file_path = 'vaihe5.txt'
    
    lines = read_data(input_file_path)
    converted_lines = convert_numbers_to_letters(lines)
    
    save_to_file(output_file_path, converted_lines)

    print(f"Converted data saved to {output_file_path}.")
    print("\n".join(converted_lines))  # Print the converted output

if __name__ == "__main__":
    main()

