import tkinter as tk
import re
from tkinter import filedialog




class EntryPopup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Entry Popup")

        self.entry = tk.Entry(self)
        self.entry.pack()

        button = tk.Button(self, text="OK", command=self.get_entry_value)
        button.pack()

    def get_entry_value(self):
        value = self.entry.get()
        print("Entry value:", value)
        self.destroy()


class SyntaxHighlighter:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Nim Text Editor NTE")

        # Top Menu
        self.menu_bar = tk.Menu(self.window)
        
        self.open_file = None
        
        # File part
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open", command=lambda     : self.file_menu_selected(event=("Open",    "File")))
        self.file_menu.add_command(label="New", command=lambda      : self.file_menu_selected(event=("New",     "File")))
        self.file_menu.add_command(label='Save', command= lambda    : self.file_menu_selected(event=("Save",    "File")))
        self.file_menu.add_command(label='Save As', command= lambda : self.file_menu_selected(event=("Save As", "File")))
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.window.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)
        
        # Edit Part
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Cut",     command=lambda : self.edit_menu_selected(event=("Cut"   ,"Edit")))
        self.edit_menu.add_command(label="Copy",    command=lambda : self.edit_menu_selected(event=("Copy"  ,"Edit")))
        self.edit_menu.add_command(label="Paste",   command=lambda : self.edit_menu_selected(event=("Paste" ,"Edit")))
        self.edit_menu.add_command(label="Edit",    command=lambda : self.edit_menu_selected(event=("Edit"  ,"Edit")))
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)
        
        # AutoComplete Part
        self.autocomplete_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.autocomplete_menu.add_command(label="New Match",   command=lambda : self.autocomplete_menu_selected(event=("New Match"   ,"AutoComplete")))
        self.autocomplete_menu.add_command(label="Remove Match",command=lambda : self.autocomplete_menu_selected(event=("Remove Match"  ,"AutoComplete")))
        self.autocomplete_menu.add_command(label="Settings",    command=lambda : self.autocomplete_menu_selected(event=("Settings" ,"AutoComplete")))
        self.autocomplete_menu.add_command(label="Turn Off",    command=lambda : self.autocomplete_menu_selected(event=("Turn Off"  ,"AutoComplete")))
        self.menu_bar.add_cascade(label="AutoComplete", menu=self.autocomplete_menu)
        
        self.window.config(menu=self.menu_bar)


        self.text = tk.Text(
            self.window,
            background="black",
            foreground="cyan",
            font=("verdana", 12, "normal"),
        )
        self.text.pack(fill="both", expand=True)

        self.autocomplete_popup = None
        self.autocomplete_listbox = None

        self.text.tag_config("keyword", foreground="magenta")
        self.text.tag_config("constants", foreground="#66B2FF")
        self.text.tag_config("comment", foreground="green")
        self.text.tag_config("declaration-keyword", foreground="RoyalBlue2")
        self.text.tag_config("function-declaration", foreground="yellow2")
        self.text.tag_config("typing", foreground="light green")
        self.text.tag_config("braces", foreground="white")
        self.text.tag_config("cursor", background="red")

        self.text.bind("<KeyRelease>", self.on_text_change)
        self.text.bind("<Motion>", self.on_mouse_motion)

        self.syntax_rules = [
            (r'\b(addr|and|as|asm|atomic|bind|block|break|case|cast|concept|const|continue|converter|'
             r'defer|in|discard|distinct|div|do|elif|else|end|enum|except|export|finally|for|from|func|'
             r'generic|if|import|include|interface|is|isnot|iterator|let|macro|method|mixin|mod|nil|not|'
             r'notin|object|of|or|out|ptr|raise|ref|return|shl|shr|template|try|tuple|type|using|var|when|'
             r'while|with|without|xor|yield)\b', 'keyword'),
            (r'\b(True|False|None|nil|null|proc)\b', "constants"),
            (r'\b(proc|type|method)\b', "declaration-keyword"),
            (r'\b([a-zA-Z_][a-zA-Z0-9_]*)\b(?!\s*\()', "identifier"),
            (r'\b([a-zA-Z_][a-zA-Z0-9_]*)\s*\((.*?)\)(?::\s*\w+)?', "function-declaration"),
            (r'\b(int|int8|int16|int32|int64|uint|uint8|uint16|uint32|uint64|float|float32|float64|bool|'
             r'char|char8|char16|char32|string|seq|array|set|tuple|enum|object)\b', "typing"),
            (r'[(){}\[\]]', "braces"),
            (r'#.*$', 'comment'),
        ]

        self.highlight_syntax()

        self.window.mainloop()


    def file_menu_selected(self, *args, **kwargs):
        if kwargs['event'] == ("Open", "File"):
            self.open_file = filedialog.askopenfilename()
            if self.open_file is not None:
                with open(self.open_file, "r") as rfile:
                    data = rfile.read()
                self.text.delete("0.0", "end")
                self.text.insert("0.0", data)
                self.highlight_syntax()
                    
        elif kwargs['event'] == ("New File", "File"):
            pass
        elif kwargs['event'] == ("Save", "File"):
            pass
        elif kwargs['event'] == ("Save As", "File"):
            pass 
    
    def edit_menu_selected(self, *args, **kwargs):
        if kwargs['event'] == ("Cut", "Edit"):
            print("CUT")
        elif kwargs['event'] == ("Copy", "Edit"):
            pass
        elif kwargs['event'] == ("Paste", "Edit"):
            pass
        elif kwargs['event'] == ("Edit", "Edit"):
            pass 
    

    def autocomplete_menu_selected(self, *args, **kwargs):
        if kwargs['event'] == ("New Match", "AutoComplete"):
            print("New Match")
            
        elif kwargs['event'] == ("Remove Match", "AutoComplete"):
            pass
        elif kwargs['event'] == ("Settings", "AutoComplete"):
            pass
        elif kwargs['event'] == ("Turn Off", "AutoComplete"):
            pass 
    

    def highlight_syntax(self, event=None):
        print("<METHOD> highlight_syntax")

        self.text.tag_remove("keyword", "1.0", "end")
        self.text.tag_remove("constants", "1.0", "end")
        self.text.tag_remove("comment", "1.0", "end")
        self.text.tag_remove("declaration-keyword", "1.0", "end")
        self.text.tag_remove("function-declaration", "1.0", "end")
        self.text.tag_remove("typing", "1.0", "end")
        self.text.tag_remove("braces", "1.0", "end")

        for pattern, tag_name in self.syntax_rules:
            matches = re.finditer(pattern, self.text.get("1.0", "end"))
            if matches is None:
                continue
            for match in matches:
                start = "1.0 + {}c".format(match.start())
                end = "1.0 + {}c".format(match.end())
                self.text.tag_add(tag_name, start, end)

    def on_text_change(self, event=None):
        print("<METHOD> on_text_change")

        self.highlight_syntax()
        self.autocomplete(event=event)

    def on_mouse_motion(self, event=None):

        cursor_index = self.text.index(tk.CURRENT)
        self.text.tag_remove("cursor", "1.0", "end")
        self.text.tag_add("cursor", cursor_index)

    def autocomplete(self, event, *args, **kwargs):
        print("args: ", args, " kwargs: ", kwargs)
        print("<METHOD> autocomplete")
        current_line, current_col = map(int, self.text.index(tk.INSERT).split("."))
        current_line_text = self.text.get(f"{current_line}.0", f"{current_line}.end")
        current_word = re.search(r"\w+$", current_line_text[:current_col])
        if current_word:
            word_start = current_col - current_word.start()
            word = current_line_text[word_start:current_col]
            options = self.get_autocomplete_options(word)
            self.clear_autocomplete_popup()  # Clear existing autocomplete popup
            if options:
                self.show_autocomplete_popup(options, current_col)

    def get_autocomplete_options(self, word, *args):
        # Replace this with your own logic to generate autocomplete options
        print("args: ", args)
        keywords = ["if", "else", "while", "for", "def", "class"]
        return [keyword for keyword in keywords if keyword.startswith(word)]

    def show_autocomplete_popup(self, options, col, *args, **kwargs):
        print("args: ", args, " kwargs: ", kwargs)
        self.autocomplete_popup = tk.Toplevel(self.window)
        self.autocomplete_popup.wm_overrideredirect(True)
        self.autocomplete_popup.wm_geometry(
            f"+{self.window.winfo_rootx() + self.text.winfo_x() + col * 8}+{self.window.winfo_rooty() + self.text.winfo_y() + 24}")
        self.autocomplete_popup.bind("<FocusOut>", lambda : self.autocomplete_popup.destroy())

        self.autocomplete_listbox = tk.Listbox(self.autocomplete_popup, background="white",
                                               selectbackground="lightblue")
        for option in options:
            self.autocomplete_listbox.insert(tk.END, option)

        self.autocomplete_listbox.pack()

        # Bind Up and Down arrow keys for keyboard navigation
        self.text.bind("<KeyPress-Up>", lambda : self.move_up(event=("Key.Up", )))
        self.text.bind("<KeyPress-Down>", lambda : self.move_down(event=("Key.Down", )))
        self.text.bind("<KeyPress-Tab>", lambda : self.autocomplete(event=("Key.Tab", )))

        self.autocomplete_listbox.bind("<Button-1>", lambda : self.text.focus_set())  # Set focus back to text widget on listbox click

        self.text.focus_set()

    def clear_autocomplete_popup(self, *args, **kwargs):
        """Clear the autocomplete popup."""
        print("args: ", args, " kwargs: ", kwargs)
        print("<METHOD> clear_autocomplete_popup")
        if self.autocomplete_popup:
            self.autocomplete_popup.destroy()
            self.autocomplete_popup = None
            self.autocomplete_listbox = None

    def move_up(self, *args, **kwargs):
        """Move the selection in autocomplete popup up."""
        print("args: ", args, " kwargs: ", kwargs)
        if self.autocomplete_listbox:
            current_index = self.autocomplete_listbox.curselection()
            if current_index:
                new_index = current_index[0] - 1
                if new_index >= 0:
                    self.autocomplete_listbox.selection_clear(current_index)
                    self.autocomplete_listbox.selection_set(new_index)
                    self.autocomplete_listbox.activate(new_index)

    def move_down(self, *args, **kwargs):
        """Move the selection in autocomplete popup down."""
        print("args: ", args, " kwargs: ", kwargs)
        if self.autocomplete_listbox:
            current_index = self.autocomplete_listbox.curselection()
            if current_index:
                new_index = current_index[0] + 1
                if new_index < self.autocomplete_listbox.size():
                    self.autocomplete_listbox.selection_clear(current_index)
                    self.autocomplete_listbox.selection_set(new_index)
                    self.autocomplete_listbox.activate(new_index)

    def insert_autocomplete(self, option, *args, **kwargs):
        print("args: ", args, " kwargs: ", kwargs)
        current_line, current_col = map(int, self.text.index(tk.INSERT).split("."))
        current_line_text = self.text.get(f"{current_line}.0", f"{current_line}.end")
        current_word = re.search(r"\w+$", current_line_text[:current_col])
        if current_word:
            word_start = current_col - current_word.start()
            self.text.delete(f"{current_line}.{word_start}", f"{current_line}.{current_col}")
        self.text.insert(tk.INSERT, option)


if __name__ == "__main__":
    editor = SyntaxHighlighter()
