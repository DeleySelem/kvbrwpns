import re

def read_data(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return [line.strip() for line in lines]

def extract_numbers(lines):
    numbers = []
    for line in lines:
        # Use regex to find all numbers in brackets and parentheses
        matches = re.findall(r'\[(\d+)\]|\((\d+)\)', line)
        # Flatten the matches and convert to integers
        num_list = []
        for match in matches:
            num_list.extend(int(num) for num in match if num)  # Add non-empty matches
        numbers.append(num_list)
    return numbers

def predict_next(numbers):
    predictions = []
    for num_list in numbers:
        if len(num_list) < 2:
            predictions.append(num_list)  # Not enough data to predict
            continue
        
        # Determine if the list is in parentheses or brackets
        if '(' in str(num_list[0]):  # Check for parentheses
            next_value = (num_list[-1] + 1) % 10  # Wrap around for parentheses (0-9)
        else:  # Assume brackets
            next_value = (num_list[-1] + 1) % 27  # Wrap around for brackets (1-26)
            if next_value == 0:
                next_value = 1  # Ensure that 0 wraps to 1

        predictions.append(num_list + [next_value])  # Append the new number to the list
    return predictions
def format_predictions(lines, predictions):
    formatted_lines = []
    for line, pred in zip(lines, predictions):
        # Determine the format based on the original line
        if '[' in line:
            formatted_lines.append(''.join(f'[{num}]' for num in pred))
        if '(' in line:
            # Use the same prediction logic for parentheses
            formatted_lines.append(''.join(f'({num})' for num in pred))
    return formatted_lines

def save_to_file(file_path, formatted_lines):
    with open(file_path, 'w') as file:
        for line in formatted_lines:
            file.write(line + '\n')

def main():
    input_file_path = 'vaihe2.txt'
    output_file_path = 'vaihe3.txt'
    
    lines = read_data(input_file_path)
    numbers = extract_numbers(lines)
    
    # Predict next numbers
    predictions = predict_next(numbers)
    
    # Format the predictions for output
    formatted_lines = format_predictions(lines, predictions)
    
    save_to_file(output_file_path, formatted_lines)

    print(f"Predicted data saved to {output_file_path}.")
    print("\n".join(formatted_lines))  # Print the predictions

if __name__ == "__main__":
    main()
