import customtkinter
from pandastable import Table
import pandas as pd

class TableWindow(customtkinter.CTkToplevel):

    def _get_table(self, df):
        self.df_getted = df

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("Табличка")
        self.geometry("800x700")

        self.sidebar_frame_main = customtkinter.CTkFrame(master=self, corner_radius=0)
        self.sidebar_frame_main.grid(row=0, column=4, columnspan=4, rowspan=1, sticky="nsew")
        self.sidebar_frame_main.grid_rowconfigure(0, weight=1)
        self.sidebar_frame_main.grid_columnconfigure(0, weight=1)

        self.label = customtkinter.CTkLabel(master=self.sidebar_frame_main, text='CSV Files Path:')
        self.label.grid(row=1, column=0, padx=20, pady=(20, 20))

        self.dict_test = {'A': [1, 2, 3], 'B': [1, 2, 3]}
        self.df = pd.DataFrame(self.dict_test)

        self.table_show = Table(self.sidebar_frame_main, dataframe=self.df, showtoolbar=False, showstatusbar=True)
        self.table_show.show()
        self.table_show.redraw()