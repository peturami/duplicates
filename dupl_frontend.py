from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import simpledialog
import os
from dupl_backend import Duplicates


duplicate = Duplicates()


class Window(object):

    def __init__(self, root):

        self.root = root
        self.root.wm_title("Duplicates")
        self.dir_path = os.path.dirname(os.path.realpath(__file__))

        self.root.iconbitmap(r'{}\book.ico'.format(self.dir_path))

        # root label
        l1 = Label(root, text="separator")
        l1.grid(row=0, column=0)

        l2 = Label(root, text="header")
        l2.grid(row=1, column=0)

        l3 = Label(root, text="encoding")
        l3.grid(row=2, column=0)

        # root combobox
        self.cb1 = ttk.Combobox(values=(".", ",", ";", ":", "-", "/", "|", "\\", "-", "~", "•", "space", "tab"), state="readonly")
        self.cb1.grid(row=0, column=1)
        self.cb1.set(",")

        self.cb2 = ttk.Combobox(values=("Yes", "No"), state="readonly")
        self.cb2.grid(row=1, column=1)
        self.cb2.set(("Yes", "No")[0])

        self.cb3 = ttk.Combobox(values=("utf-8", "windows-1250"), state="readonly")
        self.cb3.grid(row=2, column=1)
        self.cb3.set(("utf-8", "windows-1250")[0])

        # root textbox
        self.text1 = Text(root, height=35, width=130)
        self.text1.grid(row=5, column=0, rowspan=2, columnspan=10)
        self.text1.config(state="disabled")

        self.text2 = Text(root, height=1, width=130)
        self.text2.grid(row=8, column=0, rowspan=1, columnspan=10)
        self.text2.config(state="normal")
        self.text2.insert(INSERT, "Ready")
        self.text2.config(state="disabled")

        # menu definition
        main_menu = Menu(root)

        self.menuSoubor = Menu(main_menu, tearoff=0)
        self.menuSoubor.add_command(label="Open", command=self.open_dialog_window)
        self.menuSoubor.add_command(label="Save unique", command=lambda: self.save_dialog_window("unique"))
        self.menuSoubor.add_command(label="Save duplicates", command=lambda: self.save_dialog_window("duplicates"))
        # lambda allows send argument withnout executing the command in init phase
        self.menuSoubor.add_separator()
        self.menuSoubor.add_command(label="Exit", command=root.quit)
        self.menuSoubor.entryconfig(1, state=DISABLED)
        self.menuSoubor.entryconfig(2, state=DISABLED)
        main_menu.add_cascade(label="File", menu=self.menuSoubor)

        self.menuRun = Menu(main_menu, tearoff=0)
        self.menuRun.add_command(label="Analyze", command=self.popup_run_options)
        self.menuRun.add_command(label="Show few rows", command=self.show_first_rows)
        self.menuRun.add_command(label="Show duplicates", command=self.show_duplicate_rows)
        self.menuRun.entryconfig(0, state=DISABLED)
        self.menuRun.entryconfig(1, state=DISABLED)
        self.menuRun.entryconfig(2, state=DISABLED)
        main_menu.add_cascade(label="Run", menu=self.menuRun)

        self.menuAdvanced = Menu(main_menu, tearoff=0)
        self.menuAdvanced.add_command(label="Find in file", command=self.find_in_file)
        self.menuAdvanced.add_command(label="Split file", command=self.split_file)
        self.menuAdvanced.entryconfig(0, state=DISABLED)
        self.menuAdvanced.entryconfig(1, state=DISABLED)
        main_menu.add_cascade(label="Advanced", menu=self.menuAdvanced)

        root.config(menu=main_menu)

    # in progress, method will find pattern and return results into main textbox
    def find_in_file(self):
        self.input = simpledialog.askstring("Find", "Looking for something?")

    # method for splitting huge files into smaller chunks - user defines chunk value
    def split_file(self):
        try:
            self.split_nbr = int(simpledialog.askstring("Split", "Split file after xx rows:"))
            self.text1.config(state="normal")
            self.text1.delete(1.0, END)
            Window.get_attributes(self, type=False)
            for i in duplicate.split_file(self.root.filename_open, self.separator_input, self.encoding_input,
                                          self.header_input, self.split_nbr):
                self.text1.insert(END, i)
            self.text1.config(state="disabled")

        except ValueError:
            self.text1.config(state="normal")
            self.text1.delete(1.0, END)
            self.text1.insert(END, "Ooops!! You can't split file by string.")
            self.text1.config(state="disabled")

    # read filename, enable/disable buttons and other features
    def open_dialog_window(self):
        self.root.filename_open = filedialog.askopenfilename(initialdir=self.dir_path, title="Select file", filetypes=(("*.csv file", "*.csv"), ("Normal text file (*.txt)", "*.txt"), ("All types (*.*)", "*.*")))

        self.text1.config(state="normal")
        self.text1.delete(1.0, END)
        self.text1.config(state="disabled")

        if (len(self.root.filename_open) == 0) or (self.root.filename_open == None):
            self.text2.config(state="normal")
            self.text2.delete(1.0, END)
            self.text2.insert(END, 'No file loaded')
            self.text2.config(state="disabled")

            self.menuAdvanced.entryconfig(0, state=DISABLED)
            self.menuAdvanced.entryconfig(1, state=DISABLED)
            self.menuRun.entryconfig(0, state=DISABLED)
            self.menuRun.entryconfig(1, state=DISABLED)
            self.menuRun.entryconfig(2, state=DISABLED)
            self.menuSoubor.entryconfig(1, state=DISABLED)
            self.menuSoubor.entryconfig(2, state=DISABLED)

        else:
            self.text2.config(state="normal")
            self.text2.delete(1.0, END)
            self.text2.insert(END, 'File {} loaded'.format(self.root.filename_open))
            self.text2.config(state="disabled")

            self.menuAdvanced.entryconfig(1, state=NORMAL)
            self.menuRun.entryconfig(0, state=NORMAL)
            self.menuRun.entryconfig(1, state=NORMAL)

    # method for saving outputs - duplicates x unique rows
    def save_dialog_window(self, what):
        self.root.filename = filedialog.asksaveasfilename(initialdir=self.dir_path, title="Save as", defaultextension="csv",
                                                          filetypes=(("*.csv file", "*.csv"), ("Normal text file (*.txt)", "*.txt"), ("All types (*.*)", "*.*")))
        Window.get_attributes(self)

        if what == "unique" and self.ChBColumnAnalysis == 1 and len(self.ColumnsForAnalysis) != 0:
            duplicate.create_unique_output(self.root.filename, self.separator_input, self.encoding_input, subset=self.ColumnsForAnalysis, keep=self.dupl_occur)
        elif what == "unique" and self.ChBColumnAnalysis == 0:
            duplicate.create_unique_output(self.root.filename, self.separator_input, self.encoding_input, subset=None, keep=self.dupl_occur)

        elif what == "duplicates" and self.ChBColumnAnalysis == 1 and len(self.ColumnsForAnalysis) != 0:
            duplicate.create_dupl_output(self.root.filename, self.separator_input, self.encoding_input, subset=self.ColumnsForAnalysis, keep=False)
        else:
            duplicate.create_dupl_output(self.root.filename, self.separator_input, self.encoding_input, subset=None, keep=self.dupl_occur)

        self.text1.config(state="normal")
        self.text1.delete(1.0, END)
        self.text1.insert(END, "Output saved to {}".format(self.root.filename))
        self.text1.config(state="disabled")

    # method gets values from settings (buttons, checkboxes and comboboxes)
    def get_attributes(self,type="all"):

        if self.cb1.get() == "space":
            self.separator_input = "\s+"
        elif self.cb1.get() == "tab":
            self.separator_input = "\t"
        else:
            self.separator_input = self.cb1.get()
        self.header_input = "infer" if self.cb2.get() == "Yes" else None
        self.encoding_input = self.cb3.get()

        if type == "all":
            try:
                self.ChBColumnAnalysis = self.use_columns.get()
            except AttributeError:
                self.ChBColumnAnalysis = None

            try:
                self.ColumnsForAnalysis = self.column_list
            except AttributeError:
                self.ColumnsForAnalysis = None

            try:
                if self.dupl_desc.get() == 1:
                    self.dupl_occur = 'first'
                elif self.dupl_desc.get() == 2:
                    self.dupl_occur = 'last'
                else:
                    self.dupl_occur = False
            except AttributeError:
                self.dupl_occur = 'first'

    # crucial method that reads the file and provides basic statistics
    def file_analysis(self):

        Window.get_attributes(self)

        self.menuSoubor.entryconfig(1, state=NORMAL)
        self.menuSoubor.entryconfig(2, state=NORMAL)
        self.menuRun.entryconfig(2, state=NORMAL)

        self.text1.config(state="normal")
        self.text1.delete(1.0, END)

        try:
            for i in duplicate.analyze(self.root.filename_open, self.separator_input, self.encoding_input,
                                       self.header_input, self.ChBColumnAnalysis, self.ColumnsForAnalysis):
                self.text1.insert(END, i)
                self.text1.insert(END, "\n")
        except:
            self.text1.insert(END, "Ooops! Something went wrong. Please try different input "
                                   "settings or see few lines of file (Run - Show few rows).")
        self.text1.config(state="disabled")
        self.popup.destroy()

    # read 30 lines of file and display the result
    def show_first_rows(self):
        self.text1.config(state="normal")
        self.text1.delete(1.0, END)
        Window.get_attributes(self, type=False)
        for i in duplicate.show_several_rows(name=self.root.filename_open, encoding=self.encoding_input):
            self.text1.insert(END, i)
        self.text1.config(state="disabled")

    # method for finding and displaying duplicates based on selected columns or whole row
    def show_duplicate_rows(self):
        self.text1.config(state="normal")
        self.text1.delete(1.0, END)

        Window.get_attributes(self)

        if self.ChBColumnAnalysis == 1 and len(self.ColumnsForAnalysis) != 0:
            for i in duplicate.find_duplicate_rows(subset=self.ColumnsForAnalysis, keep=False):
                self.text1.insert(END, i)
                self.text1.insert(END, "\n")
        else:
            for i in duplicate.find_duplicate_rows(keep=self.dupl_occur):
                self.text1.insert(END, i)
                self.text1.insert(END, "\n")

        self.text1.config(state="disabled")

    # method which run popup "setting" window
    def popup_run_options(self):
        self.popup = Toplevel()
        self.popup.wm_title("Run options")
        self.popup.iconbitmap(r'{}\book.ico'.format(self.dir_path))

        # set of functions which allow user to define columns that should be analysed
        self.column_list = []
        def add_row():
            try:
                self.pop_list_orig.delete(self.index)
                self.pop_list_new.insert(END, self.selected_item_add)
                self.column_list.append(self.selected_item_add)
                self.index = None
                self.selected_item_add = None
                return self.pop_list_new
            except TclError:
                pass

        def remove_row():
            try:
                self.pop_list_new.delete(self.index_remove)
                self.pop_list_orig.insert(END, self.selected_item_remove)
                self.column_list.remove(self.selected_item_remove)
                self.index_remove = None
                self.selected_item_remove = None
                return self.pop_list_orig
            except TclError:
                pass

        def get_selected_row_add(event):
            try:
                self.index = self.pop_list_orig.curselection()[0]
                self.selected_item_add = self.pop_list_orig.get(self.index)
            except IndexError:
                pass

        def get_selected_row_remove(event):
            try:
                self.index_remove = self.pop_list_new.curselection()[0]
                self.selected_item_remove = self.pop_list_new.get(self.index_remove)
            except IndexError:
                pass

        # method for enable/disable listboxes and buttons for column analysis - depend on user input
        def check_column_analysis():
            if self.use_columns.get() == 0:
                pop_btn_add.config(state=DISABLED)
                pop_btn_del.config(state=DISABLED)
                self.pop_list_orig.config(state="disabled")
                self.pop_list_new.config(state="disabled")
            else:
                pop_btn_add.config(state=NORMAL)
                pop_btn_del.config(state=NORMAL)
                self.pop_list_orig.config(state="normal")
                self.pop_list_new.config(state="normal")

        # duplicates description group in popup window
        dupl_group = LabelFrame(self.popup, text="Keep duplicates")
        dupl_group.grid(row=1, column=1)
        self.dupl_desc = IntVar()
        rbtn_dupl_desc1 = Radiobutton(dupl_group, text="First", variable=self.dupl_desc, value=1)
        rbtn_dupl_desc1.grid(row=2, column=1)
        rbtn_dupl_desc2 = Radiobutton(dupl_group, text="Last", variable=self.dupl_desc, value=2)
        rbtn_dupl_desc2.grid(row=2, column=2)
        rbtn_dupl_desc3 = Radiobutton(dupl_group, text="None", variable=self.dupl_desc, value=3)
        rbtn_dupl_desc3.grid(row=2, column=3)
        self.dupl_desc.set(1)

        # columns for analysis group in popup window
        columns_group = LabelFrame(self.popup, text="Column analysis")
        columns_group.grid(row=3, column=1)
        self.use_columns = IntVar()
        check_btn = Checkbutton(columns_group, text="Select columns for analysis", variable=self.use_columns, command=check_column_analysis)
        check_btn.grid(row=4, column=1, columnspan=3)
        pop_lbl1 = ttk.Label(columns_group, text="Columns for analysis")
        pop_lbl1.grid(row=5, column=3)
        pop_lbl2 = ttk.Label(columns_group, text="Columns")
        pop_lbl2.grid(row=5, column=1)
        self.pop_list_orig = Listbox(columns_group, height=15, width=20)
        self.pop_list_orig.grid(row=7, column=1, rowspan=15)
        self.pop_list_new = Listbox(columns_group, height=15, width=20)
        self.pop_list_new.grid(row=7, column=3, rowspan=15)
        pop_btn_add = ttk.Button(columns_group, text="Add", command=add_row)
        pop_btn_add.grid(row=11, column=2)
        pop_btn_del = ttk.Button(columns_group, text="Remove", command=remove_row)
        pop_btn_del.grid(row=12, column=2)

        Frame(height=2, bd=1, relief=SUNKEN).grid(row=23)

        self.pop_btn = ttk.Button(self.popup, text="Analyse", command=self.file_analysis)
        self.pop_btn.grid(row=24, column=1)

        # get input parameters and return columns for analysis into listbox in popup window
        Window.get_attributes(self,type=False)
        header = duplicate.open_file(self.root.filename_open, self.separator_input, self.encoding_input,
                                     self.header_input, None, 0)
        self.pop_list_orig.delete(0, END)
        for i in header:
            self.pop_list_orig.insert(END, i)

        self.pop_list_orig.bind('<<ListboxSelect>>', get_selected_row_add)
        self.pop_list_new.bind('<<ListboxSelect>>', get_selected_row_remove)

        # listbox + buttons disable while opening the popup window
        check_column_analysis()

        self.popup.mainloop()


window = Tk()
Window(window)
window.mainloop()
