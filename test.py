import pyautogui as py
import pyperclip
import time
import keyboard
import re
import tkinter as tk
from tkinter import messagebox
import speech_recognition as sr

# Function to parse the data and extract rows
def parse_data(file_path):
    rows = []
    with open(file_path, 'r', encoding='utf-8', errors='replace') as file:
        for line in file:
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
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    custom_popup = tk.Toplevel(root)
    custom_popup.geometry("300x150")
    custom_popup.title("Process Completed")
    custom_popup.configure(bg='#ADD8E6')
    label = tk.Label(custom_popup, text="Need to change leads", font=("Arial", 16, "bold"), bg='#ADD8E6', fg='#333333')
    label.pack(pady=20)
    ok_button = tk.Button(custom_popup, text="OK", command=custom_popup.destroy, bg='#333333', fg='white', font=("Arial", 12, "bold"))
    ok_button.pack(pady=10)
    custom_popup.attributes('-topmost', True)
    root.mainloop()

def taking_note():
    # from sticky notes
    py.moveTo(1490, 335) 
    py.click()
    py.hotkey('ctrl', 'a')
    py.hotkey('ctrl', 'c')
    py.moveTo(587, 821, 0.5) 
    py.click()
    py.hotkey('ctrl', 'v')
    py.hotkey('enter')
    # from dr's link
    py.moveTo(565, 59, 0.5)
    py.click()
    py.hotkey('ctrl', 'c')
    py.moveTo(410, 1024, 0.5)
    py.click()
    py.moveTo(587, 821, 0.5) 
    py.click()
    py.typewrite('DR LINK:')
    py.hotkey('ctrl', 'v')
    py.hotkey('enter')
    # from vici dial
    py.moveTo(156, 21, 0.5) 
    py.click()
    py.moveTo(536, 840, 0.5) 
    py.click()
    py.moveTo(108, 774, 0.5) 
    py.tripleClick()
    py.hotkey('ctrl', 'c')
    py.moveTo(414, 1030, 0.5) 
    py.click()
    py.moveTo(587, 821, 0.5) 
    py.click()
    py.typewrite('1 VICI RECORDING      ')
    py.hotkey('ctrl', 'v')
    py.hotkey('enter')





# Define functions to handle different dispositions
def dnc():
    print("DNC OK")
    py.moveTo(409, 402)
    py.click()
    process_next_phone_number()
def handle_ctrl_alt_1():
    py.moveTo(83, 386)
    py.click()
    py.moveTo(440, 586, 0.5)
    py.click()
    py.moveTo(212, 256)
    py.doubleClick()
    process_next_phone_number()

def handle_ctrl_alt_2():
    py.moveTo(83, 386)
    py.click()
    py.moveTo(440, 586, 0.5)
    py.click()
    py.moveTo(448, 312)
    py.doubleClick()
    process_next_phone_number()

def handle_ctrl_alt_3():
    py.moveTo(83, 386)
    py.click()
    py.moveTo(440, 586, 0.5)
    py.click()
    py.moveTo(446, 282)
    py.doubleClick()
    process_next_phone_number()

def process_next_phone_number():
    global rows
    file_path = 'data.txt'
    if not rows:
        show_custom_popup()
        return
    row = rows.pop(0)
    phone_number = find_first_10_digit_number(row)
    if not phone_number:
        process_next_phone_number()
        return
    pyperclip.copy(phone_number)
    py.moveTo(348, 842)
    py.click()
    py.moveTo(232, 219, 0.5)
    py.click()
    py.hotkey('ctrl', 'v')
    py.moveTo(385, 474)
    py.click()
    row_text = '\t'.join(row)
    capitalized_row_text = capitalize_text(row_text)
    pyperclip.copy(capitalized_row_text)
    py.moveTo(301, 438)
    py.click()
    py.hotkey('ctrl', 'v')
    update_data_file(file_path, rows)

def update_data_file(file_path, remaining_rows):
    with open(file_path, 'w', encoding='utf-8', errors='replace') as file:
        for row in remaining_rows:
            file.write('\t'.join(row) + '\n')

# Voice recognition function
def listen_for_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio).lower()
            print(f"Recognized command: {command}") 
            return command
        except sr.UnknownValueError:
            print("Sorry, I could not understand the command.")
        except sr.RequestError as e:
            print(f"Error with the speech recognition service: {e}")
    return ""

def handle_voice_command(command):
    # Always log the recognized command
    print(f"Handling command: {command}")
    
    if "answering machine" in command:
        handle_ctrl_alt_1()
    elif "goodbye" in command  or "have a good day" in command:
        handle_ctrl_alt_2()
    elif "no answer" in command:
        handle_ctrl_alt_3()
    elif "next" in command:
        process_next_phone_number()   
    elif "dnc" in command:
        dnc() 
    elif "take note" in command:
        taking_note()        
    else:
        print("Command not recognized.")

if __name__ == "__main__":
    file_path = 'data.txt'
    rows = parse_data(file_path)
    
    # Set up voice commands loop
    while True:
        voice_command = listen_for_command()
        if voice_command:
            handle_voice_command(voice_command)
