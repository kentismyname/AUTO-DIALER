import pyautogui as py
import pyperclip
import time
import keyboard
import re
import tkinter as tk
from tkinter import messagebox

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

def show_custom_popup():
    # Create a custom Tkinter window
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    
    # Customize the message box style
    custom_popup = tk.Toplevel(root)
    custom_popup.geometry("300x150")
    custom_popup.title("Process Completed")
    
    # Set background color and other styles
    custom_popup.configure(bg='#ADD8E6')  # Light blue background
    
    # Label with custom font and text
    label = tk.Label(custom_popup, text="Need to change leads", font=("Arial", 16, "bold"), bg='#ADD8E6', fg='#333333')
    label.pack(pady=20)
    
    # Ok button to close the popup
    ok_button = tk.Button(custom_popup, text="OK", command=custom_popup.destroy, bg='#333333', fg='white', font=("Arial", 12, "bold"))
    ok_button.pack(pady=10)

    # Make sure the pop-up window stays on top of all other windows
    custom_popup.attributes('-topmost', True)

    # Run the Tkinter loop
    root.mainloop()

# Function to simulate hotkey process and move to coordinates for "Answering Machine"
def handle_ctrl_alt_1():
    print("Ctrl+Alt+1 pressed. Moving to coordinates for answering machine...")
    py.moveTo(83, 386)
    py.click()
    py.moveTo(440, 586, 1)
    py.click()
    py.moveTo(212, 256, 0.5)
    py.doubleClick()
    print("Dispo: Answering Machine")
    # Simulate Alt key functionality
    process_next_phone_number()

# Function to simulate hotkey process and move to coordinates for "Not Interested"
def handle_ctrl_alt_2():
    print("Ctrl+Alt+2 pressed. Moving to coordinates for not interested...")
    py.moveTo(83, 386)
    py.click()
    py.moveTo(440, 586, 1)
    py.click()
    py.moveTo(448, 312, 0.5)
    py.doubleClick()
    print("Dispo: Not Interested")
    # Simulate Alt key functionality
    process_next_phone_number()

# Function to simulate hotkey process and move to coordinates for "No Answer"
def handle_ctrl_alt_3():
    print("Ctrl+Alt+3 pressed. Moving to coordinates for no answer...")
    py.moveTo(83, 386)
    py.click()
    py.moveTo(440, 586, 1)
    py.click()
    py.moveTo(446, 282, 0.5)
    py.doubleClick()
    print("Dispo: No Answer")
    # Simulate Alt key functionality
    process_next_phone_number()

# New function for Ctrl + 1 functionality
def handle_ctrl_1():
    print("Ctrl+1 pressed. Moving to coordinates (348, 842)...")
    
    # Move cursor to specific coordinates and click
    py.moveTo(621, 819, 0.5)
    py.click()
    py.moveTo(586, 180, 0.5)
    py.click()
    
    # Add any additional actions you want to perform after clicking
    print("PAUSED AS NOTES.")


def process_next_phone_number1():
    global rows
    file_path = 'data.txt'  # Path to your data file
    
    if not rows:
        print("No more rows to process.")
        show_custom_popup()
        return
    
    # Process the next row
    row = rows.pop(0)  # Get the first row and remove it from the list
    
    # Find the first 10-digit number in the row
    phone_number = find_first_10_digit_number(row)
    if not phone_number:
        print("No 10-digit number found in this row. Skipping...")
        process_next_phone_number()  # Skip this row and move to the next
        return

    # Copy the phone number to clipboard
    pyperclip.copy(phone_number)

    # Move cursor to specific coordinates and click
    py.moveTo(348, 842)
    py.click()
    py.moveTo(232, 219)
    py.click()

    # Simulate paste (Ctrl+V)
    py.hotkey('ctrl', 'v')
    py.moveTo(385, 474, 0.5)
    py.click()

    # Wait for a short time to allow the paste operation
    time.sleep(1)

    # Copy the entire current row
    row_text = '\t'.join(row)
    capitalized_row_text = capitalize_text(row_text)
    pyperclip.copy(capitalized_row_text)

    py.moveTo(301, 438)
    py.click()

    # Simulate paste (Ctrl+V) for the entire row
    py.hotkey('ctrl', 'v')

    # Wait for a short time to allow the paste operation
    time.sleep(1)

    # After processing, update the data.txt file by removing the processed row
    update_data_file(file_path, rows)

    print("Phone number and row pasted, and row removed from data.txt.")

# Setting up the Ctrl+Alt+1, 2, 3 hotkey functionalities
keyboard.add_hotkey('ctrl+alt+1', handle_ctrl_alt_1)
keyboard.add_hotkey('ctrl+alt+2', handle_ctrl_alt_2)
keyboard.add_hotkey('ctrl+alt+3', handle_ctrl_alt_3)
keyboard.add_hotkey('ctrl+1', handle_ctrl_1)
keyboard.add_hotkey('up', process_next_phone_number1)

def update_data_file(file_path, remaining_rows):
    """Rewrite data.txt with the remaining rows"""
    with open(file_path, 'w') as file:
        for row in remaining_rows:
            file.write('\t'.join(row) + '\n')

def process_next_phone_number():
    global rows
    file_path = 'data.txt'  # Path to your data file
    
    if not rows:
        print("No more rows to process.")
        show_custom_popup()
        return
    
    # Process the next row
    row = rows.pop(0)  # Get the first row and remove it from the list
    
    # Find the first 10-digit number in the row
    phone_number = find_first_10_digit_number(row)
    if not phone_number:
        print("No 10-digit number found in this row. Skipping...")
        process_next_phone_number()  # Skip this row and move to the next
        return

    # Copy the phone number to clipboard
    pyperclip.copy(phone_number)

    # Move cursor to specific coordinates and click
    py.moveTo(348, 842)
    py.click()
    py.moveTo(232, 219)
    py.click()

    # Simulate paste (Ctrl+V)
    py.hotkey('ctrl', 'v')
    py.moveTo(385, 474, 0.5)
    py.click()

    # Wait for a short time to allow the paste operation
    time.sleep(1)

    # Copy the entire current row
    row_text = '\t'.join(row)
    capitalized_row_text = capitalize_text(row_text)
    pyperclip.copy(capitalized_row_text)

    py.moveTo(301, 438)
    py.click()

    # Simulate paste (Ctrl+V) for the entire row
    py.hotkey('ctrl', 'v')

    # Wait for a short time to allow the paste operation
    time.sleep(1)

    # After processing, update the data.txt file by removing the processed row
    update_data_file(file_path, rows)

    print("Phone number and row pasted, and row removed from data.txt.")

    # Switch to the 7th tab (Ctrl + 7 to switch to tab number 7)
    py.hotkey('ctrl', '7')
    time.sleep(0.5)  # Small delay to ensure the tab is switched
    
    # Close the 7th tab (Ctrl + W to close)
    py.hotkey('ctrl', 'w')
    print("7th tab closed.")


if __name__ == "__main__":
    file_path = 'data.txt'  # Path to your data file
    rows = parse_data(file_path)
    print("Press Ctrl+Alt+1, 2, or 3 to process phone numbers with dispositions.")
    keyboard.wait()  # Keep the script running until a hotkey is pressed
