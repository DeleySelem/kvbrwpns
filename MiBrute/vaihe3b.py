import re

def modify_numbers_in_parentheses(input_file, output_file):
    with open(input_file, 'r') as file:
        content = file.readlines()
    
    modified_content = []
    
    for line in content:
        # Use regex to find numbers in parentheses and replace 10 with 0
        modified_line = re.sub(r'\((10)\)', '(0)', line)
        modified_content.append(modified_line)
    
    with open(output_file, 'w') as file:
        file.writelines(modified_content)

    # Print the modified content
    print(f'\033[33mModified content:\033[34m ({output_file}):')
    for line in modified_content:
        print(line, end='')

if __name__ == "__main__":
    input_file = 'vaihe3.txt'
    output_file = 'modified_vaihe3.txt'
    modify_numbers_in_parentheses(input_file, output_file)
