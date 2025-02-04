import vaihe1
import vaihe2
import vaihe3
import vaihe3b
import vaihe4
import vaihe5
import os
import re

def main(file_path, verbose=False):
    if not os.path.exists(file_path):
        print("File not found. Please check the path and try again.")
        return
    
    # Load words from the file
    words = vaihe1.load_words(file_path)
    
  
    print("\n\033[33mOriginal Words:\033[34m")
    for word in words:
        print(word)

    # Convert letters to numbers
    numerical_words = vaihe1.letters_to_numbers(words)
    # Save the numerical representation to a file
    output_file_path = 'vaihe1.txt'  # Output file name
    vaihe1.save_to_file(numerical_words, output_file_path)    
 
    print(f"\n\033[33mNumerical Representation:\033[34m ({output_file_path})")
    for num_word in numerical_words:
        print(num_word)  # Print numerical representation


    input_file_path = 'vaihe1.txt'
    output_file_path = 'vaihe2.txt'
    lines = vaihe2.read_data(input_file_path)
    transposed = vaihe2.transpose_data(lines)
    vaihe2.save_to_file(output_file_path, transposed)
    
    
    print(f"\033[33mTransposed data:\033[34m ({output_file_path}).")
    print("\n\033[34m".join(transposed))  # Print the transposed output

    input_file_path = 'vaihe2.txt'
    output_file_path = 'vaihe3.txt'
    lines = vaihe3.read_data(input_file_path)
    numbers = vaihe3.extract_numbers(lines)

    # Predict next numbers
    predictions = vaihe3.predict_next(numbers)
    # Format the predictions for output
    formatted_lines = vaihe3.format_predictions(lines, predictions)
    vaihe3.save_to_file(output_file_path, formatted_lines)
    
  
    print(f"\033[33mPredicted data:\033[34m ({output_file_path}).")
    print("\n\033[34m".join(formatted_lines))  # Print the predictions

    input_file = 'vaihe3.txt'
    output_file = 'modified_vaihe3.txt'
    vaihe3b.modify_numbers_in_parentheses(input_file, output_file)
    
    input_file_path = 'modified_vaihe3.txt'
    output_file_path = 'vaihe4.txt'
    lines = vaihe4.read_data(input_file)
    transposed = vaihe4.transpose_data(lines)
    vaihe4.save_to_file(output_file_path, transposed)

    
    print(f"\033[33mTransposed data:\033[34m ({output_file_path}).")
    print("\n\033[34m".join(transposed))  # Print the transposed output

    input_file_path = 'vaihe4.txt'
    output_file_path = 'vaihe5.txt'
    lines = vaihe5.read_data(input_file_path)
    converted_lines = vaihe5.convert_numbers_to_letters(lines)
    vaihe5.save_to_file(output_file_path, converted_lines)

 
   # print(f"\033[33mConverted data saved to:\033[34m {output_file_path}.")
   # print("\n\033[34m".join(converted_lines))  # Print the converted output
    
    # Print the contents of vaihe5.txt in blue, with the last line in light blue
    print("\033[34m" + "\n".join(converted_lines[:-1]) + "\033[0m")  # Blue font for all but last line
    print("\033[36m" + converted_lines[-1] + "\033[0m")  # Light blue for the last line

#if __name__ == "__main__":
#    main()
