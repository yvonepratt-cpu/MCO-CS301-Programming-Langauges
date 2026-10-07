import tkinter as tk


# ============================================================
# PYTHON CALCULATOR
# ============================================================


# ------------------------------------------------------------
# MAIN WINDOW
# ------------------------------------------------------------
window = tk.Tk()

window.title("Python Calculator")
window.geometry("320x500")
window.configure(bg="white")
window.resizable(True, True)


# ------------------------------------------------------------
# CALCULATOR CONTAINER
# ------------------------------------------------------------
calculator = tk.Frame(
    window,
    bg="white",
    bd=1,
    relief="solid",
    padx=20,
    pady=20
)

calculator.pack(pady=80)


# ------------------------------------------------------------
# TITLE
# ------------------------------------------------------------
title = tk.Label(
    calculator,
    text="Calculator",
    font=("Arial", 20),
    bg="white"
)

title.grid(
    row=0,
    column=0,
    columnspan=4,
    pady=(0, 15)
)


# ------------------------------------------------------------
# DISPLAY
# ------------------------------------------------------------
display = tk.Entry(
    calculator,
    font=("Arial", 24),
    justify="right",
    state="readonly",
    bd=1,
    relief="solid"
)

display.grid(
    row=1,
    column=0,
    columnspan=4,
    sticky="ew",
    pady=(0, 12)
)


# ------------------------------------------------------------
# CALCULATOR STATE
# ------------------------------------------------------------
just_calculated = False


# ============================================================
# DISPLAY FUNCTIONS
# ============================================================

def get_display():
    return display.get()


def set_display(value):

    display.config(state="normal")

    display.delete(0, tk.END)

    display.insert(0, value)

    display.config(state="readonly")


# ============================================================
# CHECK OPERATOR
# ============================================================

def is_operator(value):

    return value in ["+", "-", "*", "/"]


# ============================================================
# ADD NUMBER OR OPERATOR
# ============================================================

def add(value):

    global just_calculated

    # --------------------------------------------------------
    # If previous action was "=" and user enters a number,
    # start a new calculation.
    # --------------------------------------------------------
    if (
        just_calculated and
        not is_operator(value)
    ):

        set_display("")

    just_calculated = False

    current = get_display()


    # --------------------------------------------------------
    # OPERATOR CONTROL
    # --------------------------------------------------------
    if is_operator(value):

        # Allow negative number
        if current == "":

            if value == "-":
                set_display("-")

            return

        last_character = current[-1]

        # Replace previous operator
        if is_operator(last_character):

            current = current[:-1]

            set_display(
                current + value
            )

            return


    # --------------------------------------------------------
    # DECIMAL CONTROL
    # --------------------------------------------------------
    if value == ".":

        parts = []

        current_number = ""

        for character in current:

            if character in "+-*/":

                if current_number != "":
                    parts.append(current_number)

                current_number = ""

            else:

                current_number += character

        if current_number != "":
            parts.append(current_number)

        # Prevent multiple decimal points
        if "." in current_number:
            return

        # .5 becomes 0.5
        if (
            current == "" or
            is_operator(current[-1])
        ):

            current += "0"


    # --------------------------------------------------------
    # ADD VALUE
    # --------------------------------------------------------
    set_display(
        current + value
    )


# ============================================================
# CLEAR
# ============================================================

def clear_display():

    global just_calculated

    set_display("")

    just_calculated = False


# ============================================================
# BACKSPACE
# ============================================================

def backspace():

    global just_calculated

    current = get_display()

    if current == "":
        return

    # Remove last character
    current = current[:-1]

    set_display(current)

    just_calculated = False


# ============================================================
# CALCULATE
# ============================================================

def calculate():

    global just_calculated

    expression = get_display()

    if expression == "":
        return

    # Do not calculate unfinished expression
    if is_operator(expression[-1]):
        return

    try:

        answer = eval(expression)

        # Prevent invalid results
        if not isinstance(
            answer,
            (int, float)
        ):
            raise ValueError()

        set_display(
            str(answer)
        )

        just_calculated = True

    except Exception:

        set_display("Error")

        just_calculated = True


# ============================================================
# BUTTON SETTINGS
# ============================================================

button_font = (
    "Arial",
    18
)

button_width = 5
button_height = 2


# ============================================================
# CREATE BUTTON
# ============================================================

def create_button(
    text,
    command,
    row,
    column,
    columnspan=1
):

    button = tk.Button(
        calculator,
        text=text,
        width=button_width,
        height=button_height,
        font=button_font,
        bg="white",
        activebackground="#eeeeee",
        bd=1,
        relief="solid",
        command=command
    )

    button.grid(
        row=row,
        column=column,
        columnspan=columnspan,
        padx=3,
        pady=3,
        sticky="nsew"
    )


# ============================================================
# BUTTON LAYOUT
#
# [ C ] [ ⌫ ] [ ÷ ] [ × ]
# [ 7 ] [ 8 ] [ 9 ] [ − ]
# [ 4 ] [ 5 ] [ 6 ] [ + ]
# [ 1 ] [ 2 ] [ 3 ] [ = ]
# [       0       ] [ . ]
#
# ============================================================


# ------------------------------------------------------------
# ROW 1
# ------------------------------------------------------------
create_button(
    "C",
    clear_display,
    2,
    0
)

create_button(
    "⌫",
    backspace,
    2,
    1
)

create_button(
    "÷",
    lambda: add("/"),
    2,
    2
)

create_button(
    "×",
    lambda: add("*"),
    2,
    3
)


# ------------------------------------------------------------
# ROW 2
# ------------------------------------------------------------
create_button(
    "7",
    lambda: add("7"),
    3,
    0
)

create_button(
    "8",
    lambda: add("8"),
    3,
    1
)

create_button(
    "9",
    lambda: add("9"),
    3,
    2
)

create_button(
    "−",
    lambda: add("-"),
    3,
    3
)


# ------------------------------------------------------------
# ROW 3
# ------------------------------------------------------------
create_button(
    "4",
    lambda: add("4"),
    4,
    0
)

create_button(
    "5",
    lambda: add("5"),
    4,
    1
)

create_button(
    "6",
    lambda: add("6"),
    4,
    2
)

create_button(
    "+",
    lambda: add("+"),
    4,
    3
)


# ------------------------------------------------------------
# ROW 4
# ------------------------------------------------------------
create_button(
    "1",
    lambda: add("1"),
    5,
    0
)

create_button(
    "2",
    lambda: add("2"),
    5,
    1
)

create_button(
    "3",
    lambda: add("3"),
    5,
    2
)

create_button(
    "=",
    calculate,
    5,
    3
)


# ------------------------------------------------------------
# ROW 5
# ------------------------------------------------------------
# 0 takes the width of TWO buttons
create_button(
    "0",
    lambda: add("0"),
    6,
    0,
    columnspan=2
)

create_button(
    ".",
    lambda: add("."),
    6,
    2
)


# ============================================================
# MAKE GRID COLUMNS EXPAND EVENLY
# ============================================================

for column in range(4):

    calculator.grid_columnconfigure(
        column,
        weight=1
    )


# ============================================================
# START APPLICATION
# ============================================================

window.mainloop()