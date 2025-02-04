import re

def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def transpose_data(lines):
    # Split each line based on brackets and parentheses
    split_lines = [re.findall(r'(\[\d+\]|\(\d+\))', line) for line in lines]
    
    # Create a transposed structure
    max_length = max(len(line) for line in split_lines)
    transposed = []
    
    for col in range(max_length):
        transposed_row = []
        for line in split_lines:
            if col < len(line):
                transposed_row.append(line[col])
        transposed.append(''.join(transposed_row))  # Join components for each transposed row

    return transposed

def save_to_file(file_path, formatted_lines):
    with open(file_path, 'w') as file:
        for line in formatted_lines:
            file.write(line + '\n')

def main():
    input_file_path = 'vaihe3.txt'
    output_file_path = 'vaihe4.txt'
    
    lines = read_data(input_file_path)
    transposed = transpose_data(lines)
    
    save_to_file(output_file_path, transposed)

    print(f"Transposed data saved to {output_file_path}.")
    print("\n".join(transposed))  # Print the transposed output

if __name__ == "__main__":
    main()
