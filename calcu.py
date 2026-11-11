import tkinter as tk                                    # Import the Tkinter library to create the GUI window and widgets

window = tk.Tk()                                        # Create the main application window
window.title("Python Calculator")                       # Set the text that appears in the window's title bar
window.geometry("320x500")                              # Set the initial size of the window to 320 pixels wide by 500 pixels high
window.configure(bg="white")                            # Set the background color of the main window to white
window.resizable(True, True)                            # Allow the user to resize the window both horizontally and vertically

calculator = tk.Frame(                                  # Create a box container (frame) to hold all calculator widgets
    window,                                             # Place this frame inside the main window
    bg="white",                                         # Set the background color of the frame to white
    bd=1,                                               # Set border thickness to 1 pixel
    relief="solid",                                     # Draw a solid border line around the frame
    padx=20,                                            # Add 20 pixels of inner padding on the left and right sides
    pady=20                                             # Add 20 pixels of inner padding on the top and bottom sides
)
calculator.pack(pady=80)                                # Add the frame into the main window with 80 pixels of vertical margin

title = tk.Label(                                       # Create a text header widget
    calculator,                                         # Place the label inside the calculator frame
    text="Calculator",                                  # Display the text "Calculator"
    font=("Arial", 20),                                 # Set font style to Arial and size to 20 points
    bg="white"                                          # Set background color of the label to white
)
title.grid(row=0, column=0, columnspan=4, pady=(0, 15))   # Put title in row 0, span across 4 columns, and add 15px space below it

display = tk.Entry(                                     # Create a single-line text input field for the screen
    calculator,                                         # Place the display inside the calculator frame
    font=("Arial", 24),                                 # Set large Arial text size (24 points) for numbers
    justify="right",                                    # Align numbers to the right side of the screen like a real calculator
    state="readonly",                                   # Prevent users from typing directly using their physical keyboard
    bd=1,                                               # Set border thickness to 1 pixel
    relief="solid"                                      # Give the display box a solid border line
)
display.grid(row=1, column=0, columnspan=4, sticky="ew", pady=(0, 12))  # Place display in row 1 spanning 4 columns stretching horizontally

just_calculated = False                                 # True/False flag to track if the '=' button was just clicked

def get_display():                                      # Function to read whatever text is currently shown on screen
    return display.get()                                # Return the current text string from the display field

def set_display(value):                                 # Function to overwrite the text shown on screen with a new value
    display.config(state="normal")                      # Temporarily unlock display editing mode
    display.delete(0, tk.END)                            # Erase all existing text from index 0 to the end
    display.insert(0, value)                            # Insert the new text value into the display field
    display.config(state="readonly")                    # Relock display to read-only mode so user cannot type directly

def is_operator(value):                                 # Function to check if a symbol is a basic math operator
    return value in ["+", "-", "*", "/"]                # Return True if value is '+', '-', '*', or '/', otherwise False

def add(value):                                         # Function to append numbers or operators to the screen
    global just_calculated                              # Access the global flag variable tracking recent calculation
    if just_calculated and not is_operator(value):      # If user types a number right after getting an answer:
        set_display("")                                 # Clear screen to start a brand new calculation
    just_calculated = False                             # Reset flag back to False once typing resumes
    current = get_display()                             # Store the currently displayed text in a local variable

    if is_operator(value):                              # If the pressed button is a math operator (+, -, *, /):
        if current == "":                               # Check if the screen is currently completely empty
            if value == "-": set_display("-")           # Allow '-' at the start so user can enter negative numbers
            return                                      # Stop function early to prevent starting with +, *, or /
        last_character = current[-1]                    # Look at the very last character typed on the screen
        if is_operator(last_character):                 # If the last character was already an operator:
            current = current[:-1]                      # Delete the old operator to replace it
            set_display(current + value)                # Attach the new operator symbol and update screen
            return                                      # Exit function

    if value == ".":                                    # If the pressed button is a decimal point:
        parts = []                                      # Create an empty list to hold individual numbers from expression
        current_number = ""                             # Variable to accumulate characters for the current number being typed
        for character in current:                       # Loop through every character on the screen from left to right
            if character in "+-*/":                     # If character is an operator (+, -, *, /):
                if current_number != "": parts.append(current_number) # Add completed number to parts list
                current_number = ""                     # Reset current number accumulator for next set of digits
            else:
                current_number += character             # Append digit or existing decimal to current number string
        if current_number != "": parts.append(current_number) # Add final number to parts list after loop finishes
        if "." in current_number: return                # Stop if current number already has a decimal point (prevents invalid numbers like 5.2.3)
        if current == "" or is_operator(current[-1]):   # Check if decimal is typed at start or right after an operator
            current += "0"                              # Automatically add leading zero (e.g., converts '.' to '0.')

    set_display(current + value)                        # Append new character to existing text and refresh screen

def clear_display():                                    # Function for the 'C' (Clear) button
    global just_calculated                              # Access global calculation status flag
    set_display("")                                     # Erase all contents from the screen
    just_calculated = False                             # Reset calculation flag back to False

def backspace():                                        # Function for the '⌫' (Delete) button
    global just_calculated                              # Access global calculation status flag
    current = get_display()                             # Get current text string on screen
    if current == "": return                            # Do nothing if the screen is already empty
    set_display(current[:-1])                           # Remove the single last character using string slicing
    just_calculated = False                             # Reset calculation flag back to False

def calculate():                                        # Function for the '=' button to run math evaluation
    global just_calculated                              # Access global calculation status flag
    expression = get_display()                          # Grab full math expression string from screen
    if expression == "" or is_operator(expression[-1]): return # Exit if screen is empty or expression ends in unfinished operator

    try:
        answer = eval(expression)                       # Evaluate string expression as standard Python math code
        if not isinstance(answer, (int, float)):        # Confirm result is a valid number (integer or float decimal)
            raise ValueError()                          # Raise an error if evaluation returns invalid object type
        set_display(str(answer))                        # Convert numerical answer to string and display on screen
        just_calculated = True                          # Set flag to True so next digit clear-starts calculation
    except Exception:
        set_display("Error")                            # Display "Error" text if math is invalid (e.g., dividing by zero)
        just_calculated = True                          # Set flag to True so user typing clears the error message

button_font = ("Arial", 18)                             # Set font family to Arial and font size to 18 for all buttons
button_width = 5                                        # Set standard button width (character width units)
button_height = 2                                       # Set standard button height (line height units)

# List of color hex codes used to give each button a unique rainbow color
rainbow_colors = [
    "#FF6B6B", "#FF8E72", "#FFC75F", "#F9F871", 
    "#2EE8BB", "#4D96FF", "#6BCB77", "#9370DB",
    "#FF69B4", "#FF4500", "#FFD700", "#32CD32",
    "#00CED1", "#1E90FF", "#BA55D3", "#FF1493"
]

color_index = 0                                         # Counter index to cycle through the color list sequentially

def create_button(text, command, row, column, columnspan=1):  # Helper function to generate and position buttons easily
    global color_index                                  # Access global index pointer for rainbow color array
    bg_color = rainbow_colors[color_index % len(rainbow_colors)] # Pick next color using modulo to loop back if buttons > colors
    color_index += 1                                    # Advance index count by 1 for next button creation

    button = tk.Button(                                 # Create standard Tkinter Button widget
        calculator,                                     # Place button inside calculator frame container
        text=text,                                      # Text string printed on the button face
        width=button_width,                             # Apply width parameter
        height=button_height,                           # Apply height parameter
        font=button_font,                               # Set button text font style
        bg=bg_color,                                    # Assign current rainbow color as background
        activebackground="#FFFFFF",                     # Change button background to pure white while being clicked
        bd=1,                                           # Set button border thickness to 1 pixel
        relief="solid",                                 # Draw solid border line around button box
        command=command                                 # Assign callback function triggered when user clicks button
    )
    button.grid(row=row, column=column, columnspan=columnspan, padx=3, pady=3, sticky="nsew") # Grid-position button with spacing

# ROW 1 BUTTONS (Clear, Backspace, Divide, Multiply)
create_button("C", clear_display, 2, 0)                # Place Clear button at row 2, column 0
create_button("⌫", backspace, 2, 1)                    # Place Backspace button at row 2, column 1
create_button("÷", lambda: add("/"), 2, 2)             # Place Divide button at row 2, column 2 (inputs '/')
create_button("×", lambda: add("*"), 2, 3)             # Place Multiply button at row 2, column 3 (inputs '*')

# ROW 2 BUTTONS (7, 8, 9, Subtract)
create_button("7", lambda: add("7"), 3, 0)             # Place number 7 button at row 3, column 0
create_button("8", lambda: add("8"), 3, 1)             # Place number 8 button at row 3, column 1
create_button("9", lambda: add("9"), 3, 2)             # Place number 9 button at row 3, column 2
create_button("−", lambda: add("-"), 3, 3)             # Place Subtract button at row 3, column 3 (inputs '-')

# ROW 3 BUTTONS (4, 5, 6, Add)
create_button("4", lambda: add("4"), 4, 0)             # Place number 4 button at row 4, column 0
create_button("5", lambda: add("5"), 4, 1)             # Place number 5 button at row 4, column 1
create_button("6", lambda: add("6"), 4, 2)             # Place number 6 button at row 4, column 2
create_button("+", lambda: add("+"), 4, 3)             # Place Add button at row 4, column 3 (inputs '+')

# ROW 4 BUTTONS (1, 2, 3, Equals)
create_button("1", lambda: add("1"), 5, 0)             # Place number 1 button at row 5, column 0
create_button("2", lambda: add("2"), 5, 1)             # Place number 2 button at row 5, column 1
create_button("3", lambda: add("3"), 5, 2)             # Place number 3 button at row 5, column 2
create_button("=", calculate, 5, 3)                    # Place Equals button at row 5, column 3 (triggers calculation)

# ROW 5 BUTTONS (0, Decimal)
create_button("0", lambda: add("0"), 6, 0, columnspan=2)  # Place number 0 button at row 6 spanning 2 columns wide
create_button(".", lambda: add("."), 6, 2)             # Place Decimal point button at row 6, column 2

for column in range(4):                                 # Loop through all 4 grid columns (0, 1, 2, 3)
    calculator.grid_columnconfigure(column, weight=1)   # Configure each column to expand proportionally when resizing window

window.mainloop()                                       # Run main Tkinter event loop continuously listening for user mouse clicks
