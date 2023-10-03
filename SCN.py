import tkinter as tk
from tkinter import filedialog
from tkinter import scrolledtext
from tkinter import font as tkfont
from tkinter import colorchooser
from tkinter import messagebox
import os
import shutil

# Directory to store deleted files
deleted_files_dir = "deleted_files"

# Function to restore a deleted file
def restore_file():
    selected_file = filedialog.askopenfilename(initialdir=deleted_files_dir, filetypes=[("Text Files", "*.txt")])
    if selected_file:
        restored_file_name = os.path.basename(selected_file)
        destination = os.path.join(os.getcwd(), restored_file_name)
        shutil.move(selected_file, destination)
        open_file(destination)

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, 'w') as file:
            text = text_editor.get("1.0", tk.END)
            file.write(text)
        messagebox.showinfo("File Saved", "File saved successfully.")

def open_file(file_path):  # Pass the file_path as an argument to this function
    if file_path:
        with open(file_path, 'r') as file:
            text = file.read()
            text_editor.delete("1.0", tk.END)
            text_editor.insert("1.0", text)

def delete_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        try:
            result = messagebox.askyesno("Delete File", "Are you sure you want to delete this file?")
            if result:
                if not os.path.exists(deleted_files_dir):
                    os.makedirs(deleted_files_dir)
                destination = os.path.join(deleted_files_dir, os.path.basename(file_path))
                shutil.move(file_path, destination)
                text_editor.delete("1.0", tk.END)
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting file: {e}")

def cut_text():
    text_editor.event_generate("<<Cut>>")

def copy_text():
    text_editor.event_generate("<<Copy>>")

def paste_text():
    text_editor.event_generate("<<Paste>>")

def change_font(font_name):
    current_text = text_editor.get("1.0", tk.END)
    text_editor.configure(font=(font_name, font_size_var.get()))
    text_editor.delete("1.0", tk.END)
    text_editor.insert("1.0", current_text)

def change_font_size(font_size):
    font_name = font_var.get()
    text_editor.tag_add("font_tag", text_editor.index(tk.SEL_FIRST), text_editor.index(tk.SEL_LAST))
    text_editor.tag_configure("font_tag", font=(font_name, font_size))

def change_text_color():
    sel_start = text_editor.index(tk.SEL_FIRST)
    sel_end = text_editor.index(tk.SEL_LAST)
    
    # Check if there is selected text
    if sel_start and sel_end:
        color = colorchooser.askcolor()[1]
        text_editor.tag_add("text_color_tag", sel_start, sel_end)
        text_editor.tag_configure("text_color_tag", foreground=color)

def change_bg_color():
    color = colorchooser.askcolor()[1]
    text_editor.configure(bg=color)

def add_shape(shape):
    text_editor.insert(tk.CURRENT, f"{shape} ")

root = tk.Tk()
root.title("Simple And Customizable Notepad")

# Create a left frame for vertical menus
left_frame = tk.Frame(root)
left_frame.pack(side="left", fill="y")

# Create File, Edit, and Format menus
file_menu = tk.Menu(left_frame, tearoff=0)
# Open file dialog directly and pass the file_path to open_file
file_menu.add_command(label="Open", command=lambda: open_file(filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])))
file_menu.add_command(label="Save", command=save_file)
file_menu.add_command(label="Delete", command=delete_file)
file_menu.add_command(label="Restore Files", command=restore_file)

edit_menu = tk.Menu(left_frame, tearoff=0)
edit_menu.add_command(label="Cut", command=cut_text)
edit_menu.add_command(label="Copy", command=copy_text)
edit_menu.add_command(label="Paste", command=paste_text)

# Create Undo and Redo menu items and bind them to the functions
edit_menu.add_separator()
edit_menu.add_command(label="Undo", command=root.event_generate("<<Undo>>"))
edit_menu.add_command(label="Redo", command=root.event_generate("<<Redo>>"))

format_menu = tk.Menu(left_frame, tearoff=0)
font_var = tk.StringVar()
font_var.set("Arial")
font_menu = tk.OptionMenu(format_menu, font_var, "Arial", "Times New Roman", "Courier New", "Verdana", "Tahoma")
font_menu.pack()

font_size_var = tk.IntVar()
font_size_var.set(12)
font_size_menu = tk.OptionMenu(format_menu, font_size_var, 8, 12, 16, 20, 24)
font_size_menu.pack()

# Add Font Family option to Format menu
font_family_menu = tk.Menu(format_menu, tearoff=0)
font_family_menu.add_radiobutton(label="Arial", variable=font_var, value="Arial", command=lambda: change_font("Arial"))
font_family_menu.add_radiobutton(label="Times New Roman", variable=font_var, value="Times New Roman", command=lambda: change_font("Times New Roman"))
font_family_menu.add_radiobutton(label="Courier New", variable=font_var, value="Courier New", command=lambda: change_font("Courier New"))
font_family_menu.add_radiobutton(label="Verdana", variable=font_var, value="Verdana", command=lambda: change_font("Verdana"))
font_family_menu.add_radiobutton(label="Calibri", variable=font_var, value="Calibri", command=lambda: change_font("Calibri"))
font_family_menu.add_radiobutton(label="Georgia", variable=font_var, value="Georgia", command=lambda: change_font("Georgia"))
font_family_menu.add_radiobutton(label="Comic Sans MS", variable=font_var, value="Comic Sans MS", command=lambda: change_font("Comic Sans MS"))
font_family_menu.add_radiobutton(label="Impact", variable=font_var, value="Impact", command=lambda: change_font("Impact"))
font_family_menu.add_radiobutton(label="Trebuchet MS", variable=font_var, value="Trebuchet MS", command=lambda: change_font("Trebuchet MS"))
font_family_menu.add_radiobutton(label="Tahoma", variable=font_var, value="Tahoma", command=lambda: change_font("Tahoma"))
format_menu.add_cascade(label="Font Family", menu=font_family_menu)

# Add Font Size option to Format menu
font_size_submenu = tk.Menu(format_menu, tearoff=0)
font_size_submenu.add_radiobutton(label="8", variable=font_size_var, value=8, command=lambda: change_font_size(8))
font_size_submenu.add_radiobutton(label="12", variable=font_size_var, value=12, command=lambda: change_font_size(12))
font_size_submenu.add_radiobutton(label="16", variable=font_size_var, value=16, command=lambda: change_font_size(16))
font_size_submenu.add_radiobutton(label="20", variable=font_size_var, value=20, command=lambda: change_font_size(20))
font_size_submenu.add_radiobutton(label="24", variable=font_size_var, value=24, command=lambda: change_font_size(24))
font_size_submenu.add_radiobutton(label="24", variable=font_size_var, value=24, command=lambda: change_font_size(24))
font_size_submenu.add_radiobutton(label="26", variable=font_size_var, value=26, command=lambda: change_font_size(26))
font_size_submenu.add_radiobutton(label="28", variable=font_size_var, value=28, command=lambda: change_font_size(28))
font_size_submenu.add_radiobutton(label="30", variable=font_size_var, value=30, command=lambda: change_font_size(30))
font_size_submenu.add_radiobutton(label="32", variable=font_size_var, value=32, command=lambda: change_font_size(32))
font_size_submenu.add_radiobutton(label="34", variable=font_size_var, value=34, command=lambda: change_font_size(34))
font_size_submenu.add_radiobutton(label="36", variable=font_size_var, value=36, command=lambda: change_font_size(36))
font_size_submenu.add_radiobutton(label="38", variable=font_size_var, value=38, command=lambda: change_font_size(38))
font_size_submenu.add_radiobutton(label="40", variable=font_size_var, value=40, command=lambda: change_font_size(40))
font_size_submenu.add_radiobutton(label="42", variable=font_size_var, value=42, command=lambda: change_font_size(42))
font_size_submenu.add_radiobutton(label="44", variable=font_size_var, value=44, command=lambda: change_font_size(44))
font_size_submenu.add_radiobutton(label="46", variable=font_size_var, value=46, command=lambda: change_font_size(46))
font_size_submenu.add_radiobutton(label="48", variable=font_size_var, value=48, command=lambda: change_font_size(48))
font_size_submenu.add_radiobutton(label="50", variable=font_size_var, value=50, command=lambda: change_font_size(50))
format_menu.add_cascade(label="Font Size", menu=font_size_submenu)

color_menu = tk.Menu(format_menu, tearoff=0)
format_menu.add_cascade(label="Colors", menu=color_menu)
color_menu.add_command(label="Text Color", command=change_text_color)
color_menu.add_command(label="Background Color", command=change_bg_color)

# Create the text editor on the right
text_editor = scrolledtext.ScrolledText(root)  # Define text_editor before using it here
text_editor.pack(fill="both", expand=True)

# Create buttons for File, Edit, Format, and Shapes
file_button = tk.Button(left_frame, text="Files", width=5, command=lambda: file_menu.post(file_button.winfo_rootx(), file_button.winfo_rooty() + file_button.winfo_height()))
file_button.pack(pady=5)

edit_button = tk.Button(left_frame, text="Edit", width=5, command=lambda: edit_menu.post(edit_button.winfo_rootx(), edit_button.winfo_rooty() + edit_button.winfo_height()))
edit_button.pack(pady=5)

format_button = tk.Button(left_frame, text="Format", width=5, command=lambda: format_menu.post(format_button.winfo_rootx(), format_button.winfo_rooty() + format_button.winfo_height()))
format_button.pack(pady=5)

shapes_menu = tk.Menu(left_frame, tearoff=0)
shapes_menu.add_command(label="Circle", command=lambda: add_shape("○"))
shapes_menu.add_command(label="Square", command=lambda: add_shape("■"))
shapes_menu.add_command(label="Triangle", command=lambda: add_shape("▲"))
shapes_menu.add_command(label="Star", command=lambda: add_shape("★"))
shapes_menu.add_command(label="Heart", command=lambda: add_shape("❤"))
shapes_menu.add_command(label="Arrow", command=lambda: add_shape("➡"))
shapes_menu.add_command(label="Smiley", command=lambda: add_shape("😊"))
shapes_menu.add_command(label="Sun", command=lambda: add_shape("☀"))
shapes_menu.add_command(label="Diamond", command=lambda: add_shape("♦"))
shapes_menu.add_command(label="Checkmark", command=lambda: add_shape("✔"))
shapes_menu.add_command(label="Cross", command=lambda: add_shape("✖"))

shapes_button = tk.Button(left_frame, text="Shapes", width=5, command=lambda: shapes_menu.post(shapes_button.winfo_rootx(), shapes_button.winfo_rooty() + shapes_button.winfo_height()))
shapes_button.pack(pady=5)

root.mainloop()






































































































