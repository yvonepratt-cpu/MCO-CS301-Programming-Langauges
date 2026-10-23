import tkinter as tk                                    # Import tkinter GUI module

window = tk.Tk()                                        # Initialize main application window
window.title("Python Calculator")                       # Set window title text
window.geometry("320x500")                              # Set fixed window dimensions
window.configure(bg="white")                            # Set window background color to white
window.resizable(True, True)                            # Allow window to be resizable

calculator = tk.Frame(                                  # Create main calculator container frame
    window,
    bg="white",
    bd=1,
    relief="solid",
    padx=20,
    pady=20
)
calculator.pack(pady=80)                                # Pack container frame with vertical padding

title = tk.Label(                                       # Create title label widget
    calculator,
    text="Calculator",
    font=("Arial", 20),
    bg="white"
)
title.grid(row=0, column=0, columnspan=4, pady=(0, 15))   # Position title spanning across 4 columns

display = tk.Entry(                                     # Create screen display input field
    calculator,
    font=("Arial", 24),
    justify="right",
    state="readonly",
    bd=1,
    relief="solid"
)
display.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 12))  # Position display across 4 columns

just_calculated = False                                 # Flag to track if '=' was just pressed

def get_display():                                      # Get current text from display screen
    return display.get()

def set_display(value):                                 # Set text value onto display screen
    display.config(state="normal")                      # Temporarily enable display for editing
    display.delete(0, tk.END)                           # Clear existing display text
    display.insert(0, value)                            # Insert new value string
    display.config(state="readonly")                    # Lock display back to readonly mode

def is_operator(value):                                 # Check if value is a math operator
    return value in ["+", "-", "*", "/"]

def add(value):                                         # Handle adding numbers and operators
    global just_calculated
    if just_calculated and not is_operator(value):      # If typing number after '=', clear screen
        set_display("")
    just_calculated = False                             # Reset calculation flag
    current = get_display()                             # Get current display text

    if is_operator(value):                              # Handle operator input
        if current == "":                               # If screen is empty
            if value == "-": set_display("-")           # Allow leading negative sign
            return
        last_character = current[-1]                    # Get last character on screen
        if is_operator(last_character):                 # If last char is also an operator
            current = current[:-1]                      # Remove previous operator
            set_display(current + value)                # Append new operator
            return

    if value == ".":                                    # Handle decimal input
        parts = []
        current_number = ""
        for character in current:                       # Split expression into separate numbers
            if character in "+-*/":
                if current_number != "": parts.append(current_number)
                current_number = ""
            else:
                current_number += character
        if current_number != "": parts.append(current_number)
        if "." in current_number: return                # Prevent multiple decimals in one number
        if current == "" or is_operator(current[-1]):   # Add '0' if decimal typed after operator
            current += "0"

    set_display(current + value)                        # Append value to display screen

def clear_display():                                    # Clear calculator display screen
    global just_calculated
    set_display("")                                     # Clear screen text
    just_calculated = False                             # Reset flag

def backspace():                                        # Remove last character from screen
    global just_calculated
    current = get_display()
    if current == "": return
    set_display(current[:-1])                           # Slice off final character
    just_calculated = False

def calculate():                                        # Compute final expression result
    global just_calculated
    expression = get_display()
    if expression == "" or is_operator(expression[-1]): return # Exit if empty or ends with operator

    try:
        answer = eval(expression)                       # Safely evaluate expression math
        if not isinstance(answer, (int, float)):        # Check if result is valid number type
            raise ValueError()
        set_display(str(answer))                        # Show answer on display screen
        just_calculated = True                          # Mark calculation as complete
    except Exception:
        set_display("Error")                            # Show error message on invalid math
        just_calculated = True

button_font = ("Arial", 18)                             # Define button font style and size
button_width = 5                                        # Define standard button width
button_height = 2                                       # Define standard button height

# List of vibrant rainbow colors for buttons
rainbow_colors = [
    "#FF6B6B", "#FF8E72", "#FFC75F", "#F9F871", 
    "#2EE8BB", "#4D96FF", "#6BCB77", "#9370DB",
    "#FF69B4", "#FF4500", "#FFD700", "#32CD32",
    "#00CED1", "#1E90FF", "#BA55D3", "#FF1493"
]

color_index = 0                                         # Index counter for rainbow colors

def create_button(text, command, row, column, columnspan=1):  # Helper function to create buttons
    global color_index
    bg_color = rainbow_colors[color_index % len(rainbow_colors)]  # Pick next rainbow color
    color_index += 1                                    # Increment color index pointer

    button = tk.Button(
        calculator,
        text=text,
        width=button_width,
        height=button_height,
        font=button_font,
        bg=bg_color,                                    # Apply rainbow background color
        activebackground="#FFFFFF",                     # Highlight color on button press
        bd=1,
        relief="solid",
        command=command
    )
    button.grid(row=row, column=column, columnspan=columnspan, padx=3, pady=3, sticky="nsew")

# ROW 1 BUTTONS
create_button("C", clear_display, 2, 0)
create_button("⌫", backspace, 2, 1)
create_button("÷", lambda: add("/"), 2, 2)
create_button("×", lambda: add("*"), 2, 3)

# ROW 2 BUTTONS
create_button("7", lambda: add("7"), 3, 0)
create_button("8", lambda: add("8"), 3, 1)
create_button("9", lambda: add("9"), 3, 2)
create_button("−", lambda: add("-"), 3, 3)

# ROW 3 BUTTONS
create_button("4", lambda: add("4"), 4, 0)
create_button("5", lambda: add("5"), 4, 1)
create_button("6", lambda: add("6"), 4, 2)
create_button("+", lambda: add("+"), 4, 3)

# ROW 4 BUTTONS
create_button("1", lambda: add("1"), 5, 0)
create_button("2", lambda: add("2"), 5, 1)
create_button("3", lambda: add("3"), 5, 2)
create_button("=", calculate, 5, 3)

# ROW 5 BUTTONS
create_button("0", lambda: add("0"), 6, 0, columnspan=2)  # 0 button spans two columns width
create_button(".", lambda: add("."), 6, 2)

for column in range(4):                                 # Make calculator grid columns expand evenly
    calculator.grid_columnconfigure(column, weight=1)

window.mainloop()                                       # Start main application event loop
