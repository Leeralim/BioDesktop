from tksheet import Sheet
import tkinter as tk
from os.path import normpath
from tkinter import filedialog
import csv
import io


class TableSheet(tk.Tk):
    def __init__(self, df, name_file):
        tk.Tk.__init__(self)
        self.title(f'{name_file}')
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        
        self.frame = tk.Frame(self)
        self.frame.grid_columnconfigure(0, weight = 1)
        self.frame.grid_rowconfigure(0, weight = 1)

        self.df = df
        data = [[j for j in i[1:]] for i in self.df.itertuples()]
        header = [i for i in self.df.columns]

        self.sheet = Sheet(self.frame,
                           data = data,
                           headers=header,
                           theme = "dark",
                           height = 700,
                           width = 1100)
        self.sheet.enable_bindings("copy",
                                   "rc_select",
                                   "arrowkeys",
                                   "double_click_column_resize",
                                   "column_width_resize",
                                   "column_select",
                                   "row_select",
                                   "drag_select",
                                   "single_select",
                                   "select_all")
        self.frame.grid(row = 0, column = 0, sticky = "nswe")
        self.sheet.grid(row = 0, column = 0, sticky = "nswe")

        self.sheet.popup_menu_add_command("Выгрузить таблицу в CSV", self.save_sheet)
        self.sheet.popup_menu_add_command("Открыть csv-файлик", self.open_csv)
        self.sheet.set_all_cell_sizes_to_text()

    def save_sheet(self):
        filepath = filedialog.asksaveasfilename(parent = self,
                                                title = "Save sheet as",
                                                filetypes = [('CSV File','.csv'),
                                                             ('TSV File','.tsv')],
                                                defaultextension = ".csv",
                                                confirmoverwrite = True)
        if not filepath or not filepath.lower().endswith((".csv", ".tsv")):
            return
        try:
            with open(normpath(filepath), "w", newline = "", encoding = "utf-8") as fh:
                writer = csv.writer(fh,
                                    dialect = csv.excel if filepath.lower().endswith(".csv") else csv.excel_tab,
                                    lineterminator = "\n", delimiter='|')
                writer.writerows(self.sheet.get_sheet_data(get_header = True, get_index = False))
        except:
            return


    def open_csv(self):
        filepath = filedialog.askopenfilename(parent = self, title = "Select a csv file")
        if not filepath or not filepath.lower().endswith((".csv", ".tsv")):
            return
        try:
            with open(normpath(filepath), "r") as filehandle:
                filedata = filehandle.read()
            self.sheet.set_sheet_data([r for r in csv.reader(io.StringIO(filedata),
                                                             dialect = csv.Sniffer().sniff(filedata),
                                                             skipinitialspace = False)])
        except:
            return
        

