import tkinter as tk
from tkinter import filedialog, messagebox, Scrollbar
from tkinter import ttk

# Initialize the main window
root = tk.Tk()
root.title("Notepad")
root.geometry("800x600")
style = ttk.Style()

file_path = None
tab_counter = 1

# Function to create a new file in a new tab
def new_file():
    global file_path, tab_counter
    file_path = None
    new_tab = ttk.Frame(notebook)
    notebook.add(new_tab, text=f"Untitled {tab_counter}")
    tab_counter += 1
    text_area = create_text_area(new_tab)
    update_status(text_area)

# Function to open an existing file in a new tab
def open_file():
    global file_path, tab_counter
    file_path = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "r") as file:
            contents = file.read()
        new_tab = ttk.Frame(notebook)
        notebook.add(new_tab, text=f"{file_path.split('/')[-1]}")
        tab_counter += 1
        text_area = create_text_area(new_tab, contents)
        update_status(text_area)

# Function to save the current file
def save_file():
    global file_path
    if file_path:
        with open(file_path, "w") as file:
            current_tab = notebook.nametowidget(notebook.select())
            text_widget = current_tab.winfo_children()[0]
            file.write(text_widget.get(1.0, tk.END))
    else:
        save_as_file()

# Function to save the current file with a new name
def save_as_file():
    global file_path
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if file_path:
        with open(file_path, "w") as file:
            current_tab = notebook.nametowidget(notebook.select())
            text_widget = current_tab.winfo_children()[0]
            file.write(text_widget.get(1.0, tk.END))
        notebook.tab(notebook.select(), text=f"{file_path.split('/')[-1]}")

# Function to exit the application
def exit_app():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

# Function to create a text area in a given tab
def create_text_area(tab, contents=""):
    text_area = tk.Text(tab, wrap='word', undo=True, font=('Consolas', 12))
    text_area.pack(expand=1, fill='both')
    text_area.insert(tk.END, contents)
    return text_area

status_bar = ttk.Label(root, text="Line: 1, Column: 1", anchor='e')
def update_status(text_area):
    row, col = text_area.index(tk.INSERT).split('.')
    status_bar.config(text=f"Line: {row}, Column: {col}")
def cut_text():
    current_tab = notebook.nametowidget(notebook.select())
    text_widget = current_tab.winfo_children()[0]
    text_widget.event_generate("<<Cut>>")

# Function to copy selected text
def copy_text():
    current_tab = notebook.nametowidget(notebook.select())
    text_widget = current_tab.winfo_children()[0]
    text_widget.event_generate("<<Copy>>")

# Function to paste text
def paste_text():
    current_tab = notebook.nametowidget(notebook.select())
    text_widget = current_tab.winfo_children()[0]
    text_widget.event_generate("<<Paste>>")

# Function to select all text
def select_all_text():
    current_tab = notebook.nametowidget(notebook.select())
    text_widget = current_tab.winfo_children()[0]
    text_widget.tag_add("sel", "1.0", "end")

# Function to toggle between dark and bright modes
def toggle_mode():
    current_theme = style.theme_use()
    if current_theme == 'clam':
        style.theme_use('default')
        root.config(bg='#fdfdfd')
        style.configure('TNotebook', background='#fdfdfd')
        style.configure('TNotebook.Tab', padding=[10, 2], font=('Arial', 12), background='#fdfdfd', foreground='#333')
        style.configure('TLabel', font=('Arial', 10), background='#fdfdfd', foreground='#333')
        style.configure('TButton', font=('Arial', 10), background='#fdfdfd', foreground='#333')
        style.configure('TEntry', font=('Arial', 10), background='#fdfdfd', foreground='#333')
        style.configure('Horizontal.TScrollbar', background='#fdfdfd', troughcolor='#fdfdfd', activebackground='#ddd')
        style.configure('TScrollbar', background='#fdfdfd', troughcolor='#fdfdfd', activebackground='#ddd')
        for tab_id in notebook.tabs():
            text_widget = notebook.nametowidget(tab_id).winfo_children()[0]
            text_widget.config(bg='#fdfdfd', fg='#333')
    else:
        style.theme_use('clam')
        root.config(bg='#333')
        style.configure('TNotebook', background='#333')
        style.configure('TNotebook.Tab', padding=[10, 2], font=('Arial', 12), background='#333', foreground='#fff')
        style.configure('TLabel', font=('Arial', 10), background='#333', foreground='#fff')
        style.configure('TButton', font=('Arial', 10), background='#333', foreground='#fff')
        style.configure('TEntry', font=('Arial', 10), background='#333', foreground='#fff')
        style.configure('Horizontal.TScrollbar', background='#333', troughcolor='#333', activebackground='#666')
        style.configure('TScrollbar', background='#333', troughcolor='#333', activebackground='#666')
        for tab_id in notebook.tabs():
            text_widget = notebook.nametowidget(tab_id).winfo_children()[0]
            text_widget.config(bg='#333', fg='#fff')

# Function to toggle word wrap
def toggle_word_wrap():
    current_tab = notebook.nametowidget(notebook.select())
    text_widget = current_tab.winfo_children()[0]
    if text_widget.cget("wrap") == "none":
        text_widget.config(wrap="word")
    else:
        text_widget.config(wrap="none")

# Create the notebook (tabs container)
notebook = ttk.Notebook(root)
notebook.pack(expand=1, fill='both')

# Create the initial tab
initial_tab = ttk.Frame(notebook)
notebook.add(initial_tab, text="Untitled 1")
text_area = create_text_area(initial_tab)
update_status(text_area)

# Create the status bar

status_bar.pack(side='bottom', fill='x')

# Create the menu bar
menu_bar = tk.Menu(root)

file_menu = tk.Menu(menu_bar, tearoff=0)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_command(label="Save As", command=save_as_file, accelerator="Ctrl+Shift+S")
file_menu.add_separator()
file_menu.add_command(label="Exit", command=exit_app, accelerator="Alt+F4")
menu_bar.add_cascade(label="File", menu=file_menu)

edit_menu = tk.Menu(menu_bar, tearoff=0)
edit_menu.add_command(label="Cut", command=cut_text, accelerator="Ctrl+X")
edit_menu.add_command(label="Copy", command=copy_text, accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=paste_text, accelerator="Ctrl+V")
edit_menu.add_separator()
edit_menu.add_command(label="Select All", command=select_all_text, accelerator="Ctrl+A")
menu_bar.add_cascade(label="Edit", menu=edit_menu)

# Create the view menu
view_menu = tk.Menu(menu_bar, tearoff=0)
view_menu.add_command(label="Toggle Dark/Bright Mode", command=toggle_mode)
view_menu.add_command(label="Toggle Word Wrap", command=toggle_word_wrap)
menu_bar.add_cascade(label="View", menu=view_menu)

root.bind_all("<Control-n>", lambda event: new_file())
root.bind_all("<Control-o>", lambda event: open_file())
root.bind_all("<Control-s>", lambda event: save_file())
root.bind_all("<Control-S>", lambda event: save_as_file())
root.bind_all("<Alt-F4>", lambda event: exit_app())
root.bind_all("<Control-x>", lambda event: cut_text())
root.bind_all("<Control-c>", lambda event: copy_text())
root.bind_all("<Control-v>", lambda event: paste_text())
root.bind_all("<Control-a>", lambda event: select_all_text())

root.config(menu=menu_bar)


root.mainloop()
