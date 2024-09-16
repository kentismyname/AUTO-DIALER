import pyautogui as py
import pyperclip
import time
import keyboard
import re
import pymsgbox  # For pop-up messages

# Function to parse the data and extract rows
def parse_data(file_path):
    rows = []
    
    with open(file_path, 'r') as file:
        for line in file:
            # Split the line by tabs
            fields = line.strip().split('\t')
            rows.append(fields)
    
    return rows

# Function to capitalize the entire text
def capitalize_text(text):
    return text.upper()

# Function to find the first 10-digit number in a list of fields
def find_first_10_digit_number(fields):
    for field in fields:
        match = re.search(r'\b\d{10}\b', field)
        if match:
            return match.group()
    return None

def copy_phone_numbers(rows):
    for row in rows:
        # Find the first 10-digit number in the row
        phone_number = find_first_10_digit_number(row)
        if not phone_number:
            print("No 10-digit number found in this row. Skipping...")
            continue  # Skip rows without a 10-digit phone number

        # Wait for the Alt key to be pressed
        print("Press ALT to copy and paste the next phone number...")
        keyboard.wait('Alt')  # This will wait until the Alt key is pressed

        # Copy the phone number to clipboard
        pyperclip.copy(phone_number)

        # Move cursor to specific coordinates and click
        py.moveTo(348, 842, 1)
        py.click()
        py.moveTo(232, 219, 1)
        py.click()

        # Simulate paste (Ctrl+V)
        py.hotkey('ctrl', 'v')
        py.moveTo(385, 474, 1)
        py.click()

        # Wait for a short time to allow the paste operation
        time.sleep(3)

        # Copy the entire current row
        row_text = '\t'.join(row)
        capitalized_row_text = capitalize_text(row_text)
        pyperclip.copy(capitalized_row_text)

        py.moveTo(301, 438, .5)
        py.click()

        # Simulate paste (Ctrl+V) for the entire row
        py.hotkey('ctrl', 'v')

        # Wait for a short time to allow the paste operation
        time.sleep(3)

        # Move on to the next row
        print("Phone number and row pasted. Waiting for the next Alt press...")

    # When all rows are done, show a pop-up message
    pymsgbox.alert('Need to change leads', 'Process Completed')

if __name__ == "__main__":
    file_path = 'data.txt'  # Path to your data file
    rows = parse_data(file_path)
    copy_phone_numbers(rows)
