import tkinter as tk
from tkinter import filedialog, simpledialog, scrolledtext, messagebox
from ttkthemes import ThemedStyle

# Define theme colors
theme_colors = {
    "light": {
        "bg": "#FFFFFF",  # Sky blue background
        "text_bg": "#87CEEB",
        "text_fg": "#000000",
        "menu_bg": "#EEEEEE",
        "highlight_thickness": 0,
        "highlight_color": "#000000",
    },
    "dark": {
        "bg": "#000000",  # Black background
        "text_bg": "#000000",
        "text_fg": "#00FF00",  # Green text color
        "menu_bg": "#333333",
        "highlight_thickness": 0,
        "highlight_color": "#FFFFFF",  # White for better contrast
    },
}

root = tk.Tk()
root.title("Text Editor")

current_theme = "dark"

style = ThemedStyle(root)
style.set_theme("equilux")  # Change theme to 'equilux'

def apply_theme(theme_name):
    global current_theme
    current_theme = theme_name

    for widget in root.winfo_children():
        if isinstance(widget, tk.Menu):
            widget.configure(bg=theme_colors[theme_name]["menu_bg"], fg=theme_colors[theme_name]["text_fg"], activebackground="#555555", activeforeground="#FFFFFF")
        elif isinstance(widget, scrolledtext.ScrolledText):
            widget.configure(bg=theme_colors[theme_name]["text_bg"], fg=theme_colors[theme_name]["text_fg"], font=("Helvetica", 12))
        elif isinstance(widget, tk.Label):
            widget.configure(bg=theme_colors[theme_name]["bg"], fg=theme_colors[theme_name]["text_fg"])

    status_bar.configure(bg=theme_colors[theme_name]["menu_bg"], fg="#d4d4d4", font=("Helvetica", 10))

    text_area.config(
        insertbackground=theme_colors[theme_name]["text_fg"],
        highlightcolor=theme_colors[theme_name]["highlight_color"],
        selectbackground=theme_colors[theme_name]["highlight_color"],
        selectforeground=theme_colors[theme_name]["text_bg"],
        font=("Helvetica", 12),
        bg=theme_colors[theme_name]["text_bg"],  # Set background color
        fg=theme_colors[theme_name]["text_fg"]   # Set text color
    )

def toggle_theme():
    if current_theme == "dark":
        apply_theme("light")
    else:
        apply_theme("dark")

def save_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text files", "*.txt")]
    )
    if file_path:
        with open(file_path, "w") as file:
            file.write(text_area.get(1.0, tk.END))
        root.title(f"Text Editor - {file_path}")

def find_text():
    target = simpledialog.askstring("Find", "Enter text to find:")
    if target:
        start_index = text_area.search(target, "1.0", stopindex=tk.END)
        if start_index:
            end_index = f"{start_index}+{len(target)}c"
            text_area.tag_add("search", start_index, end_index)
            text_area.tag_configure("search", background="yellow")

def replace_text():
    target = simpledialog.askstring("Replace", "Enter text to replace:")
    if target:
        replace_with = simpledialog.askstring("Replace", "Enter replacement text:")
        if replace_with:
            start_index = text_area.search(target, "1.0", stopindex=tk.END)
            if start_index:
                end_index = f"{start_index}+{len(target)}c"
                text_area.delete(start_index, end_index)
                text_area.insert(start_index, replace_with)

def about():
    messagebox.showinfo("About", "Text Editor\nVersion 1.0\nCreated by Harsh")

menu_bar = tk.Menu(root, bg=theme_colors[current_theme]["menu_bg"], fg=theme_colors[current_theme]["text_fg"])
file_menu = tk.Menu(menu_bar, tearoff=0, bg=theme_colors[current_theme]["menu_bg"], fg=theme_colors[current_theme]["text_fg"])
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
theme_menu = tk.Menu(menu_bar, tearoff=0, bg=theme_colors[current_theme]["menu_bg"], fg=theme_colors[current_theme]["text_fg"])
theme_menu.add_command(label="Toggle Theme", command=toggle_theme)
edit_menu = tk.Menu(menu_bar, tearoff=0, bg=theme_colors[current_theme]["menu_bg"], fg=theme_colors[current_theme]["text_fg"])
edit_menu.add_command(label="Find", command=find_text)
edit_menu.add_command(label="Replace", command=replace_text)
help_menu = tk.Menu(menu_bar, tearoff=0, bg=theme_colors[current_theme]["menu_bg"], fg=theme_colors[current_theme]["text_fg"])
help_menu.add_command(label="About", command=about)

menu_bar.add_cascade(label="File", menu=file_menu)
menu_bar.add_cascade(label="Edit", menu=edit_menu)
menu_bar.add_cascade(label="Theme", menu=theme_menu)
menu_bar.add_cascade(label="Help", menu=help_menu)
root.config(menu=menu_bar)

text_area = scrolledtext.ScrolledText(root, wrap="word", undo=True)
text_area.pack(fill="both", expand=True)

status_bar = tk.Label(root, text="Ready", bd=0, relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

def update_status_bar(event=None):
    line, column = text_area.index(tk.INSERT).split(".")
    status_bar.config(text=f"Ln: {line}  Col: {column}  |  Ready")

text_area.bind("<KeyRelease>", update_status_bar)

apply_theme(current_theme)

root.mainloop()
