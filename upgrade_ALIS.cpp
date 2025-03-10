#!/bin/bash

# Disclaimer message
echo "[ This is a Cybersecurity test run performed by: Deley Selem ]"
echo "Logging actions to upgrade_log.txt..."

# Log file for recording actions and timestamps
LOG_FILE="upgrade_log.txt"

# Function to log messages with timestamps
log_message() {
    echo "$(date '+%Y-%m-%d %H:%M:%S') - $1" >> "$LOG_FILE"
}

# Function to remove comments from files
remove_comments() {
    local file="$1"
    log_message "Processing file: $file"

    # Remove single-line and multi-line comments
    sed -i.bak '/^\s*\/\//d; :a; N; /\*\n.*\*\//! ba; s/\/\*.*\*\///g; P; D' "$file"
    rm "${file}.bak"

    log_message "Comments removed from: $file"
}

# Create a backup for the upgrade file
UPGRADE_FILE="upgrade_file.sh"
cp /dev/null "$UPGRADE_FILE"  # Clear the file if it exists

# Loop through all relevant files in the current directory
for file in *.cpp *.c *.sh; do
    if [[ -f "$file" ]]; then
        remove_comments "$file"
        # Make the file executable
        chmod +x "$file"

        # Append execution command to upgrade file
        echo "./$file" >> "$UPGRADE_FILE"
    fi
done

log_message "All comments removed and files made executable."

# Create an xterm window to display the log
sudo xterm -e "tail -f $LOG_FILE" &

# Run protocols by executing the upgrade file
log_message "Running protocols..."
bash "$UPGRADE_FILE" 2>> "$LOG_FILE"  # Log any errors

log_message "Protocols executed. Upgrade file created: $UPGRADE_FILE"
echo "All actions logged in $LOG_FILE."
