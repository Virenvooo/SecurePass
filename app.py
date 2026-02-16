import customtkinter as ctk
import random
import string
import webbrowser

__version__ = "1.2.0"

# ───────────────────────────────────────────────
# Theme & Window Setup
# ───────────────────────────────────────────────
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title(f"SecurePass - Password Generator v{__version__}")
root.geometry("1300x800")
root.minsize(1300, 800)
root.resizable(False, False)

# Center window on screen
root.update_idletasks()
width = root.winfo_width()
height = root.winfo_height()
x = (root.winfo_screenwidth() // 2) - (width // 2)
y = (root.winfo_screenheight() // 2) - (height // 2)
root.geometry(f"{width}x{height}+{x}+{y}")

# ───────────────────────────────────────────────
# Fonts
# ───────────────────────────────────────────────
TITLE_FONT = ("Helvetica", 32, "bold")
LABEL_FONT = ("Helvetica", 15)
BUTTON_FONT = ("Helvetica", 14, "bold")
PASSWORD_FONT = ("Courier New", 22, "bold")

# ───────────────────────────────────────────────
# UI Elements
# ───────────────────────────────────────────────
ctk.CTkLabel(root, text="SecurePass", font=TITLE_FONT, text_color="#bb86fc").pack(pady=(50, 10))
ctk.CTkLabel(root, text="Modern Password Generator", font=("Helvetica", 16), text_color="#a0a0cc").pack(pady=(0, 30))

# Password output
output_frame = ctk.CTkFrame(root, fg_color="transparent")
output_frame.pack(pady=10, padx=60, fill="x")

password_var = ctk.StringVar()

password_entry = ctk.CTkEntry(
    output_frame,
    textvariable=password_var,
    font=PASSWORD_FONT,
    height=60,
    corner_radius=12,
    fg_color="#1e1633",
    text_color="white",
    justify="center",
    state="readonly"
)
password_entry.pack(side="left", fill="x", expand=True, padx=(0, 15))

def copy_password():
    root.clipboard_clear()
    root.clipboard_append(password_var.get())
    copy_btn.configure(text="Copied ✓")
    root.after(2000, lambda: copy_btn.configure(text="Copy"))

copy_btn = ctk.CTkButton(
    output_frame,
    text="Copy",
    font=BUTTON_FONT,
    width=120,
    height=60,
    corner_radius=12,
    fg_color="#2a1b4d",
    hover_color="#bb86fc",
    command=copy_password
)
copy_btn.pack(side="left")

# Strength
strength_frame = ctk.CTkFrame(root, fg_color="transparent")
strength_frame.pack(pady=15)

ctk.CTkLabel(strength_frame, text="Strength:", font=LABEL_FONT, text_color="#b0a0ff").pack(side="left")
strength_label = ctk.CTkLabel(strength_frame, text="—", font=("Helvetica", 17, "bold"), text_color="#666")
strength_label.pack(side="left", padx=15)

def update_strength():
    pw = password_var.get()
    if len(pw) < 10:
        strength_label.configure(text="Weak", text_color="#ff6b6b")
        return
    variety = sum([any(c.islower() for c in pw), any(c.isupper() for c in pw),
                   any(c.isdigit() for c in pw), any(not c.isalnum() for c in pw)])
    score = len(pw) * 4 + variety * 25
    if score < 70:   col, txt = "#ff6b6b", "Weak"
    elif score < 100: col, txt = "#ffd166", "Medium"
    else:            col, txt = "#06d6a0", "Strong"
    strength_label.configure(text=txt, text_color=col)

# Options
opts = ctk.CTkFrame(root, fg_color="transparent")
opts.pack(pady=20, padx=100, fill="x")

ctk.CTkLabel(opts, text="Password Length", font=LABEL_FONT, text_color="#e0d4ff").pack(anchor="w", pady=(20,5))

value_label = ctk.CTkLabel(opts, text="16", font=("Helvetica", 20, "bold"), text_color="#bb86fc")
value_label.pack(anchor="w")

length_var = ctk.IntVar(value=16)
slider = ctk.CTkSlider(opts, from_=8, to=40, variable=length_var, height=28, button_length=32,
                       progress_color="#bb86fc", fg_color="#2a1b4d")
slider.pack(fill="x", pady=10)

# Checkboxes
check_frame = ctk.CTkFrame(opts, fg_color="transparent")
check_frame.pack(pady=25, anchor="w")

lower_var = ctk.BooleanVar(value=True)
upper_var = ctk.BooleanVar(value=True)
num_var   = ctk.BooleanVar(value=True)
sym_var   = ctk.BooleanVar(value=True)

for text, var in [
    ("Lowercase (a-z)", lower_var),
    ("Uppercase (A-Z)", upper_var),
    ("Numbers (0-9)", num_var),
    ("Symbols (!@#$...)", sym_var)
]:
    ctk.CTkCheckBox(check_frame, text=text, variable=var, font=LABEL_FONT).pack(anchor="w", pady=9)

# Generate button
def generate():
    chars = ""
    if lower_var.get(): chars += string.ascii_lowercase
    if upper_var.get(): chars += string.ascii_uppercase
    if num_var.get():   chars += string.digits
    if sym_var.get():   chars += string.punctuation

    if not chars:
        password_var.set("Select at least one option")
        return

    pwd = "".join(random.choice(chars) for _ in range(length_var.get()))
    password_var.set(pwd)
    update_strength()

generate_btn = ctk.CTkButton(
    root,
    text="Generate New Password",
    font=BUTTON_FONT,
    width=320,
    height=62,
    corner_radius=20,
    fg_color="#2a1b4d",
    hover_color="#bb86fc",
    text_color="white",
    command=generate
)
generate_btn.pack(pady=40)

# Live updates
length_var.trace_add("write", lambda *a: (value_label.configure(text=str(length_var.get())), generate()))
for v in (lower_var, upper_var, num_var, sym_var):
    v.trace_add("write", lambda *a: generate())

# Footer
footer = ctk.CTkLabel(
    root,
    text="Made with ♥ by Vir • v" + __version__,
    font=("Helvetica", 14, "italic"),
    text_color="#bb86fc",
    cursor="hand2"
)
footer.place(relx=1.0, rely=1.0, anchor="se", x=-30, y=-25)
footer.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/YOURUSERNAME/SecurePass"))

# Start
generate()
root.mainloop()