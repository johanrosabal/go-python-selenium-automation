import tkinter as tk
from tkinter import ttk


def ask_for_mfa_code(default_code: str = "") -> str:
    """
    Displays an interactive OS-level modal using Tkinter to ask the user
    for the Okta MFA code. Blocks execution until a choice is made.

    Args:
        default_code (str): An optional default code to pre-fill the input field.

    Returns:
        str: The entered MFA code, or None if the user chose to skip.
    """
    root = tk.Tk()
    root.title("Manual Intervention: Okta MFA")

    # Make the window pop up in front of everything
    root.attributes("-topmost", True)
    root.focus_force()

    # Center the window
    window_width = 350
    window_height = 150
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x_cordinate = int((screen_width / 2) - (window_width / 2))
    y_cordinate = int((screen_height / 2) - (window_height / 2))
    root.geometry(f"{window_width}x{window_height}+{x_cordinate}+{y_cordinate}")

    # UI Elements
    result = {"code": None, "skipped": False}

    ttk.Label(root, text="Enter the Okta code:", font=("Arial", 11)).pack(pady=10)

    code_entry = ttk.Entry(root, font=("Arial", 12), width=20)
    if default_code:
        code_entry.insert(0, default_code)
    code_entry.pack(pady=5)
    code_entry.focus()

    def on_submit(event=None):
        result["code"] = code_entry.get().strip()
        root.destroy()

    def on_skip():
        result["skipped"] = True
        root.destroy()

    root.bind("<Return>", on_submit)

    btn_frame = ttk.Frame(root)
    btn_frame.pack(pady=15)

    submit_btn = ttk.Button(btn_frame, text="Send Code", command=on_submit)
    submit_btn.grid(row=0, column=0, padx=5)

    skip_btn = ttk.Button(btn_frame, text="Skip (Okta not required)", command=on_skip)
    skip_btn.grid(row=0, column=1, padx=5)

    # Block execution until window is closed
    root.mainloop()

    if result["skipped"]:
        return None
    return result["code"] if result["code"] else None
