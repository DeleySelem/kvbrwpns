import re
import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import datetime
import os
import subprocess  # Importing subprocess to run the external script
import vaiheet1233b5

# Global variable to control output verbosity
output_mode = 'default'
log_lines = []  # To store log lines for verbose output

def save_multifractal_results(log_file, q_values, tau_q, char_counts):
    """Save multifractal analysis results to a log file."""
    with open(log_file, 'w') as f:
        f.write("q values:\n")
        f.write(', '.join(map(str, q_values)) + '\n')
        f.write("tau(q) values:\n")
        f.write(', '.join(map(str, tau_q)) + '\n')
        f.write("Character Counts:\n")
        for char, count in char_counts.items():
            f.write(f"{char}: {count}\n")

def perform_multifractal_analysis_and_save(file_path, log_file):
    """Perform multifractal analysis and save results to a log file."""
    phrases = read_phrases(file_path)
    multifractal_results = multifractal_analysis(phrases)
    save_multifractal_results(log_file, *multifractal_results)

def read_phrases(file_path):
    """Read phrases from the specified file, handling potential errors."""
    try:
        with open(file_path, 'r') as file:
            phrases = [line.strip() for line in file if line.strip()]
        return phrases
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' was not found.")
        return []
    except Exception as e:
        print(f"An error occurred while reading the file: {e}")
        return []

def filter_phrases(phrases):
    """Filter out invalid phrases, allowing only alphanumeric characters."""
    filtered = []
    for phrase in phrases:
        if re.match(r'^[a-z0-9]+$', phrase):  # Match letters and numbers
            filtered.append(phrase)
    return filtered

def get_next_char(current_char, unique_chars):
    """Get the next character from unique characters list."""
    if current_char in unique_chars:
        current_index = unique_chars.index(current_char)
        return unique_chars[(current_index + 1) % len(unique_chars)]
    return current_char  # Fallback

def get_next_digit(current_digit, unique_digits):
    """Get the next digit from unique digits list."""
    if current_digit in unique_digits:
        current_index = unique_digits.index(current_digit)
        return unique_digits[(current_index + 1) % len(unique_digits)]
    return current_digit  # Fallback

def generate_next_phrase(phrases):
    """Generate the next phrase based on existing phrases."""
    base_phrase = phrases[0]  # Start with the first phrase
    next_phrase = []

    for i in range(len(base_phrase)):
        chars_at_index = [p[i] for p in phrases if len(p) > i]  # Get all chars at this index
        unique_chars = sorted(set(char for char in chars_at_index if char.isalpha()))
        unique_digits = sorted(set(char for char in chars_at_index if char.isdigit()))

        if base_phrase[i].isalpha():
            next_char = get_next_char(base_phrase[i], unique_chars)
            next_phrase.append(next_char)
        elif base_phrase[i].isdigit():
            next_digit = get_next_digit(base_phrase[i], unique_digits)
            next_phrase.append(next_digit)
        else:
            next_phrase.append(base_phrase[i])  # Keep other characters unchanged

    return ''.join(next_phrase)

def log_message(message):
    """Log a message with a timestamp."""
    if output_mode == 'verbose':
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        log_entry = f"{timestamp} - {message}\n"
        log_lines.append(log_entry)  # Store the log entry
        with open('console.log', 'a') as log_file:
            log_file.write(log_entry)

def print_log():
    """Print all new log lines to the console."""
    for line in log_lines:
        print(line, end='')  # Print each log line

def log_transformed_phrases(phrases):
    """Log transformed phrases where letters are replaced with '@' and digits with '%'."""
    transformed_phrases = []
    
    for phrase in phrases:
        transformed_phrase = ''.join(['@' if c.isalpha() else '%' for c in phrase])
        transformed_phrases.append(transformed_phrase)

    # Log the transformed phrases to console.log
    with open('console.log', 'a') as log_file:
        for tp in transformed_phrases:
            log_file.write(tp + '\n')
    
    return transformed_phrases

def detect_logic(phrases):
    """Detect the logic type of the given phrases."""
    if not phrases:
        return None, "Dynamic"

    # Log transformed phrases
    transformed_phrases = log_transformed_phrases(phrases)

    # Check if all transformed phrases are equal
    if all(tp == transformed_phrases[0] for tp in transformed_phrases):
        logic_type = "Static"
    else:
        logic_type = "Dynamic"

    # Create the logic string based on the first phrase
    detected_logic = ''.join(['@' if c.isalpha() else '%' for c in phrases[0]])
    
    return detected_logic, logic_type

def multifractal_analysis(phrases):
    """Perform multifractal analysis on the given phrases."""
    char_counts = Counter(''.join(phrases))
    frequencies = np.array(list(char_counts.values()))
    
    prob_dist = frequencies / frequencies.sum()
    
    q_values = np.linspace(-5, 5, 100)
    tau_q = np.zeros_like(q_values)
    
    for i, q in enumerate(q_values):
        tau_q[i] = np.sum(prob_dist ** q)
    
    print("\033[36m################ Multifractal Analysis Results ################\033[34m")
    print("\033[36m q values: \033[34m")
    print(q_values)
    print("\033[36mtau(q) values: \033[34m")
    print(tau_q)
    print("\033[36mCharacter Counts:\033[34m")  # Light gray font
    for char, count in char_counts.items():
        print(f"\033[34m{char}:\033[36m{count}", end="")
    
    return q_values, tau_q, char_counts

def transform_logic_representation(phrases):
    """Transform phrases into a logic representation using '@' and '%'. """
    return [''.join(['@' if c.isalpha() else '%' for c in phrase]) for phrase in phrases]

def perform_logic_analysis(phrases):
    """Analyze the logic of the phrases and perform multifractal analysis."""
    logic_representation = transform_logic_representation(phrases)

    # Perform multifractal analysis
    multifractal_results = multifractal_analysis(phrases)

    # Check if all logic representations are equal
    if all(lr == logic_representation[0] for lr in logic_representation):
        logic_type = "Static"
    else:
        logic_type = "\033[31mDynamic"

    # Output results
    print("")
    print("\033[36m################ Logic Analysis Results ################\033[0m")
    print("\033[36mLogic Representation: \033[0m", logic_representation[0])
    print("\033[36mLogic Type:           \033[0m", logic_type)

    return multifractal_results, logic_representation[0], logic_type

def calculate_matching_percentage(logic1, logic2):
    """Calculate the percentage of matching characters between two logic strings."""
    matches = sum(l1 == l2 for l1, l2 in zip(logic1, logic2))
    return (matches / len(logic1)) * 100 if logic1 else 0

def plot_multifractal_spectrum(q_values1, tau_q1, q_values2, tau_q2, q_logic, tau_logic):
    fig = plt.figure(figsize=(12, 8))
    
    # Create a 1x2 subplot layout
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122)

    # Set the figure background color to black
    fig.patch.set_facecolor('black')
    ax1.set_facecolor('black')

    # Plot User Input File
    line1, = ax1.plot(q_values1, tau_q1, zs=0, zdir='y', label='User Input File', color='blue', linewidth=5, alpha=1)
    line2, = ax1.plot(q_values2, tau_q2, zs=1, zdir='y', label='Input+Generated', color='red', linewidth=5, alpha=1)
    line3, = ax1.plot(q_logic, tau_logic, zs=2, zdir='y', label='Logic Analysis', color='green', linewidth=5, alpha=1)

    # Set labels and title with light blue text
    ax1.set_xlabel('q', color='lightblue', fontsize=8)
    ax1.set_ylabel('Analysis Type', color='lightblue', fontsize=8)
    ax1.set_zlabel('τ(q)', color='lightblue', fontsize=8)
    ax1.set_title('3D Multifractal Spectrum Analysis', color='lightblue', fontsize=10)

    # Set y-ticks and labels
    ax1.set_yticks([0, 1, 2])
    ax1.set_yticklabels(['User Input File', 'Input+Generated', '@/% -Logic Analysis'], color='darkblue', fontsize=8)

    # Set grid color to light blue
    ax1.xaxis._axinfo['grid'].update(color='lightblue', linestyle='--', linewidth=0.5)
    ax1.yaxis._axinfo['grid'].update(color='lightblue', linestyle='--', linewidth=0.5)
    ax1.zaxis._axinfo['grid'].update(color='lightblue', linestyle='--', linewidth=0.5)

    # Show grid
    ax1.grid(True)

    # Create the legend and set the text color, positioned in the bottom right corner
    legend = ax1.legend(loc='lower right')
    for text in legend.get_texts():
        text.set_color('lightblue')
        text.set_backgroundcolor('black')
    # Display multifractal data on the left side, moved further left
    data_text = (
        f"Multifractal Data:\n"
        f"User Input File:\nq: {q_values1[:60]}...\ntau(q): {tau_q1[:60]}...\n\n"
        f"Input+Generated:\nq: {q_values2[:60]}...\ntau(q): {tau_q2[:60]}...\n\n"
        f"Logic Analysis:\nq: {q_logic[:60]}...\ntau(q): {tau_logic[:60]}..."
    )
    ax1.text2D(-0.35, 1.35, data_text, transform=ax1.transAxes, fontsize=5, verticalalignment='top', horizontalalignment='left', color='cyan')

    # Calculate differences for plotting
    diff_user_vaihe = tau_q1 - tau_q2
    diff_user_logic = tau_q1 - tau_logic
    diff_vaihe_logic = tau_q2 - tau_logic

    # Set the background color of the difference plot to black
    ax2.set_facecolor('black')

    # Plot differences
    ax2.plot(q_values1, diff_user_vaihe, label='User - Generated', color='blue')
    ax2.plot(q_values1, diff_user_logic, label='User - Logic', color='red')
    ax2.plot(q_values1, diff_vaihe_logic, label='Generated - Logic', color='green')

    ax2.set_xlabel('q', fontsize=5, color='white')
    ax2.set_ylabel('Differences', fontsize=5, color='white')
    ax2.set_title('Differences Between Multifractal Data', fontsize=10, color='lightblue')
    ax2.legend(fontsize=5, loc='upper right')
    ax2.grid(True, linewidth=0.5, 	color='lightblue')  # Optional: Set grid color for better visibility

    plt.tight_layout()
    plt.show()  # Ensure the plot is displayed  
	
def print_character_counts(char_counts):
    print("\033[37mCharacter Counts:\033[0m")  # Light gray font
    for char, count in char_counts.items():
        print(f"{char}: {count}")

def skip_characters(phrase, phrases):
    """Skip letters and increment numbers based on characters at the same index in the phrases."""
    next_phrase = []
    length = len(phrase)

    for i in range(length):
        chars_at_index = [p[i] for p in phrases if len(p) > i]  # Get all chars at this index
        unique_chars = sorted(set(char for char in chars_at_index if char.isalpha()))
        unique_digits = sorted(set(char for char in chars_at_index if char.isdigit()))

        if phrase[i].isalpha():
            next_char = get_next_char(phrase[i], unique_chars)
            next_phrase.append(next_char)
        elif phrase[i].isdigit():
            next_digit = get_next_digit(phrase[i], unique_digits)
            next_phrase.append(next_digit)
        else:
            next_phrase.append(phrase[i])  # Keep other characters unchanged

    return ''.join(next_phrase)

def generate_next_phrase(phrases, logic):
    """Generate the next phrase based on the current logic."""
    if not phrases:
        return ""
    
    base_phrase = phrases[0]
    next_phrase = []

    for i in range(len(base_phrase)):
        char = base_phrase[i]
        # Skip characters using the skip_characters function
        next_phrase.append(char)  # Placeholder, will be updated

    next_phrase_str = skip_characters(''.join(next_phrase), phrases)
    
    # Ensure the generated phrase doesn't already exist
    attempts = 0
    while next_phrase_str in phrases and attempts < 10:  # Limit attempts to avoid infinite loop
        next_phrase_str = skip_characters(''.join(next_phrase), phrases)
        attempts += 1
    
    return next_phrase_str

def print_algorithm(phrase, logic):
    print("\033[32mAlgorithm found:\033[0m")  # Green font
    print(f"Generated phrase: {phrase}")
    
    # Generate and print the Python code to produce the next phrase
    print("\n\033[33mPython Code to Generate Next Phrases:\033[0m")  # Yellow font
    print(f"""
def generate_next_phrase(phrase, logic):
    next_phrase = ""
    for i in range(len(phrase)):
        char = phrase[i]
        if char.isalpha() and logic[i] == '@':
            next_char = get_next_char(char, unique_chars)  # Skip one letter
            next_phrase += next_char
        elif char.isdigit() and logic[i] == '%':
            next_digit = get_next_digit(char, unique_digits)  # Increment digit
            next_phrase += next_digit
        else:
            next_phrase += char  # Keep other characters unchanged
    return next_phrase
""")

def show_help():
    help_text = """
Available Commands:
- help: Display this help screen.
- show options: Show file info, detected logic, and current logic.
- show logic: Current logic to be used.
- set logic <logic>: Set the logic for phrase generation (e.g., '@@@@%%%%').
- set number <number>: Set the number of phrases to generate.
- set output <verbose/quiet>: Verbose output (logs all/minimal actions).
- use file <filename>: Set the file to be analyzed.
- perform logic analysis: Analyze logic to find the right logic for phrase generation.
- run / execute / start: Perform the analysis and display the results.
- exit: Exit the program.
"""
    print(help_text)

def show_options(file_path, phrases, logic, logic_type, detected_logic, num_phrases):
    print("\033[33m########################### Options ###########################\033[0m")
    print(f"File imported:      {file_path}   Change with [use file <file>]\0")
    print(f"Number of phrases:  {len(phrases)}                Amount of phrases in <file>")
    print(f"Logic type:         {logic_type}           @/% -logic can be Dynamic/Static")
    print(f"Detected logic:     {detected_logic if detected_logic else 'None'}          Logic in file.")
    print(f"Number:             {num_phrases}                Amount of phrases to predict.")
    print(f"Logic to be used:   {''.join(logic)}         Generation logic @:letter %:number.")
    print("\033[33m######################## End of Options ########################\033[0m")  # Added end marker for clarity

def run_vaiheet_program(file_path):
    """Run the vaiheet1233b5.py program with the provided file path."""
    # Call the vaiheet1233b5 main function with the file_path argument
    vaiheet1233b5.main(file_path)

def main(file_path):
    global output_mode
    phrases = read_phrases(file_path)
    filtered_phrases = filter_phrases(phrases)
    
    if not filtered_phrases:
        print("No valid phrases found in the user input file.")
        return
    
    detected_logic, logic_type = detect_logic(filtered_phrases)
    logic = list(detected_logic) if detected_logic else ['@', '%'] * (len(filtered_phrases[0]) // 2)
    
    num_phrases = 1  # Default number of phrases
    infinite_mode = False  # Flag for infinite mode
    plot_enabled = True  # Default plot setting
    multifractal_results = None  # Initialize variable
    generated_phrases = []  # List to keep track of generated phrases

    while True:
        command = input("\033[34m[\033[32m>\033[34m]\033[0m ").strip().lower()
        
        log_message(f"Command received: {command}")
        
        if command == "help":
            show_help()
            log_message("Displayed help.")

        elif command == "show logic":
            print(f"Current logic: {''.join(logic)}")
            log_message(f"Displayed logic: {logic}")
        elif command == "show options":
            show_options(file_path, filtered_phrases, logic, logic_type, detected_logic, num_phrases)
       
            log_message("Displayed options.")
        elif command.startswith("set logic "):
            new_logic = command.split(" ", 2)[-1]
            if re.match(r'^[%@]+$', new_logic):
                logic = list(new_logic)
                logic_type = "Static"
                print(f"Logic set to: {''.join(logic)}")
                log_message(f"Set logic to: {logic}")
            else:
                print("Invalid logic format. Use '@' for letters and '%' for numbers.")
                log_message("Attempted to set invalid logic.")
        elif command == "set logic auto":
            detected_logic, logic_type = detect_logic(filtered_phrases)
            if logic_type == "Static":
                logic = list(detected_logic)
                print(f"Logic set to detected logic: {''.join(logic)}")
                log_message(f"Set logic to detected: {logic}")
            else:
                print("\033[31mLogic type of the phrases in imported file is dynamic. Perform logic type analysis before doing phrase analysis.\033[0m")
                log_message("Attempted to auto-set logic but it was dynamic.")
        elif command.startswith("set number "):
            parts = command.split(" ")
            if len(parts) == 3 and parts[2] == "0":
                infinite_mode = True
                print("Generating phrases infinitely...")
                log_message("Set to infinite mode for phrase generation.")
                
                # Infinite generation mode
                while infinite_mode:
                    next_phrase_detected = generate_next_phrase(filtered_phrases + generated_phrases, logic)
                    next_phrase_skipped = skip_characters(next_phrase_detected, filtered_phrases + generated_phrases)
                    print(f"Next most probable phrase: {next_phrase_skipped}")

                    generated_phrases.append(next_phrase_skipped)

                    with open('temporary_phrases.txt', 'a') as temp_file:
                        temp_file.write(next_phrase_skipped + '\n')

                    multifractal_results = multifractal_analysis([next_phrase_skipped])
                    log_message(f"Saved generated phrase: {next_phrase_skipped}")

            else:
                try:
                    num_phrases = int(parts[-1])
                    infinite_mode = False
                    print(f"Number of phrases to generate set to: {num_phrases}")
                    log_message(f"Set number of phrases to generate: {num_phrases}")
                except ValueError:
                    print("Invalid number format.")
                    log_message("Attempted to set invalid number format.")
        elif command.startswith("set output "):
            setting = command.split(" ", 2)[-1]
            if setting in ["verbose", "quiet"]:
                output_mode = setting
                print(f"Output set to: {output_mode}")
                log_message(f"Output mode changed to: {output_mode}")
                if output_mode == 'verbose':
                    print_log()
            else:
                print("Invalid output setting. Use 'verbose' or 'quiet'.")
        elif command.startswith("use file "):
            file_path = command.split(" ", 2)[-1]
            phrases = read_phrases(file_path)
            filtered_phrases = filter_phrases(phrases)
            detected_logic, logic_type = detect_logic(filtered_phrases)
            print(f"File set to: {file_path}")
            log_message(f"Set input file to: {file_path}")
        elif command == "perform logic analysis":
            multifractal_results, detected_logic, logic_type = perform_logic_analysis(filtered_phrases)
            logic = list(detected_logic)
        elif command in ["run", "execute", "start"]:
            if multifractal_results is None:
                print("\033[31mPlease perform logic analysis first.\033[0m")
                log_message("Attempted to run analysis without performing logic analysis.")
            else:
                run_vaiheet_program(file_path)  # Call the function to run the vaiheet program with the file path
        elif command == "show plot": 
            # Perform multifractal analysis on user input file
            detected_logic, logic_type = detect_logic(filtered_phrases)
            logic = list(detected_logic) if detected_logic else ['@', '%'] * (len(filtered_phrases[0]) // 2)
            multifractal_results_user = multifractal_analysis(filtered_phrases)
    
            # Perform multifractal analysis on vaihe5.txt
            vaiheet_file_path = "vaihe5.txt"
            vaiheet_phrases = read_phrases(vaiheet_file_path)
            filtered_vaiheet_phrases = filter_phrases(vaiheet_phrases)
    
            if not filtered_vaiheet_phrases:
                print("No valid phrases found in vaihe5.txt.")
                return

            multifractal_results_vaiheet = multifractal_analysis(filtered_vaiheet_phrases)

            # Perform logic analysis
            multifractal_results_logic, detected_logic, logic_type = perform_logic_analysis(filtered_phrases)
            q_logic, tau_logic, _ = multifractal_results_logic  # Unpack logic analysis results

            # Plot both results and logic analysis
            q_values_user, tau_q_user, _ = multifractal_results_user
            q_values_vaiheet, tau_q_vaiheet, _ = multifractal_results_vaiheet
            plot_multifractal_spectrum(q_values_user, tau_q_user, q_values_vaiheet, tau_q_vaiheet, q_logic, tau_logic)

        elif command == "exit":
            print("Exiting program.")
            log_message("Program exited.")
            break
        else:
            print("\033[31mUnknown command. Type 'help' for a list of commands.\033[0m")
            log_message("Received unknown command.")

if __name__ == "__main__":
    input_file = "testpasses.txt"  # Replace with your file path
    os.system('clear')
    print("------------------------<𝕸𝖎𝕭𝖗𝖚𝖙𝖊 v1.3.4>------------------------")
    print()
    print("Passphrase Algorithm Multi Fractal Analysis Console")
    print("'Et tu mi Brute' -Julius Caesar")
    print()
    print("By: Deley Selem")
    print()
    main(input_file)
