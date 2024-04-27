from tkinter import filedialog
import tkinter as tk
import os
from Database import GetTable, UploadDatas
from DropBackspaces import DropBackspaces
from PreloadLogfile import PreloadLogfile
from tkinter.messagebox import showinfo
from NorjaaParser import NorjaaParser
import customtkinter


# Основная база
class InterfaceMethodsGeneral:
    """
    Методы взаимодействия с БД для основной БД
    """
    # выбор директории csv-файлов
    def select_directory_csv(self, curr_tab):
        curr_tab = curr_tab

        if curr_tab == 'drop_backspaces':
            folder_path = filedialog.askdirectory(title="Select dir")

            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(tk.END, folder_path)

            files = os.listdir(folder_path)
            correct_files_list = ['Tral.csv', 'Ulov.csv', 'Biopap.csv', 'Biokap.csv',
                                  'Razm.csv', 'Biopit.csv', 'TralList.csv', 'Crabs.csv', 
                                  'Morph.csv', 'Acq.csv', 'Pandalus.csv']
            
            file_path = 'C:\\temp\general'
            self.path_csv_path = os.path.join(file_path, 'fixed_csv')
            # self.path_csv_path = os.path.join(self.path_entry.get(), 'fixed_csv')

            # self.files_listbox.delete(0, tk.END)
            # for file in files:
            #     if file.endswith(".csv") and file in correct_files_list:
            #         self.files_listbox.insert(tk.END, file)


        elif curr_tab == 'preload': # предзагрузки
            folder_path = filedialog.askdirectory(title="Select dir")
            files = os.listdir(folder_path)
            correct_files_list = ['Tral.csv', 'Ulov.csv', 'Biopap.csv', 'Biokap.csv',
                                  'Razm.csv', 'Biopit.csv', 'TralList.csv', 'Crabs.csv', 
                                  'Morph.csv', 'Acq.csv', 'Pandalus.csv']
            csv_files = [i for i in files if i.endswith(".csv")]

            if set(csv_files) == set(correct_files_list):
                if folder_path == '':
                    print('Пустой путь')
                else:
                    self.general_preload_path_input.delete(0, tk.END)
                    self.general_preload_path_input.insert(tk.END, folder_path)

                    files = os.listdir(folder_path)
                    # self.file_to_delete_general = os.path.join(self.general_preload_path_input.get(), "logbio.txt")
                    file_path = 'C:\\temp\general'
                    self.path_csv_path = os.path.join(file_path, 'fixed_csv')
                    # self.path_csv_path = os.path.join(self.general_preload_path_input.get(), 'fixed_csv')
            else:
                showinfo('Информация', f'Вы выбрали не ярусные файлы!')


        elif curr_tab == 'show_csv':
            folder_path = filedialog.askdirectory(title="Select dir")

            self.path_entry_csv.delete(0, tk.END)
            self.path_entry_csv.insert(tk.END, folder_path)

            files = os.listdir(folder_path)

        elif curr_tab == 'upload_datas': # загрузка
            folder_path = filedialog.askdirectory(title="Select dir")

            self.general_onload_path_input.delete(0, tk.END)
            self.general_onload_path_input.insert(tk.END, folder_path)

            files = os.listdir(folder_path)
            
            file_path = 'C:\\temp\general'
            self.path_csv_path = os.path.join(file_path, 'fixed_csv')
            # self.path_csv_path = os.path.join(self.general_onload_path_input.get(), 'fixed_csv')

        elif curr_tab == 'unloading': # выгрузка
            folder_path = filedialog.askdirectory(title="Select dir")

            self.general_filepath_upload_input.delete(0, tk.END)
            self.general_filepath_upload_input.insert(tk.END, folder_path)
            
            file_path = 'C:\\temp\general'
            self.path_csv_path = os.path.join(file_path, 'fixed_csv')
            # self.path_csv_path = os.path.join(self.general_filepath_upload_input.get(), 'fixed_csv')
            

    # выгрузка из БД
    def unloading(self):
        path = self.general_filepath_upload_input.get()
        # path = 'C:\\temp\general\outloads'
        ship = self.general_ship_upload_input.get().upper()
        reis = self.general_reis_upload_input.get()
        GetTable.unloading_tables(self, ship, reis, path, 'general')

    # журнал предзагрузки
    def make_logfile_preload(self, folder_path):
        DropBackspaces.drop_backspaces(self, folder_path, 'general')
        try:
            # path = 'C:\\temp\general'
            # PreloadLogfile.make_logfile_preload(self, path, 'general')
            PreloadLogfile.make_logfile_preload(self, folder_path, 'general')
        except Exception as error:
            showinfo('Информация', f'{error}')      

    # загрузка в БД
    def upload_to_db(self):
        path = self.general_onload_path_input.get()
        DropBackspaces.drop_backspaces(self, path, 'general')
        UploadDatas.upload_into_db(self, path, 'general')  

# удаление рейса
    def delete_reis(self):
        ship = self.general_ship_delete_input.get().upper()
        reis = self.general_reis_delete_input.get()
        UploadDatas.del_reis(self, ship, reis, 'general')    

# корректировка признака рейса
    def corr_prizn_reis(self):
        UploadDatas.correct_prizn(self, self.general_corrprizn_ship_input.get().upper(), self.general_corrprizn_reis_input.get(), 
                                  self.general_corrprizn_przn_input.get().upper(), self.general_corrprizn_operator_input.get())

# корректировка рейса
    def corr_reis(self):
        old_ship = self.general_corrreis_oldship_input.get().upper()
        old_reis = self.general_corrreis_oldreis_input.get()
        new_ship = self.general_corrreis_newship_input.get().upper()
        new_reis = self.general_corrreis_newreis_input.get()

        UploadDatas.corr_reis(self, old_ship, old_reis, new_ship, new_reis, 'general')
        
# корректировка пробы
    def corr_prob(self):
        ship = self.general_corrprob_ship_input.get().upper()
        reis = self.general_corrprob_reis_input.get()
        trl = self.general_corrprob_trl_input.get().split(',')
        kodvid = self.general_corrprob_kodvid_input.get()
        bio_info = self.general_corrprob_bioinfo_input.get()
        u_key = self.general_corrprob_ukey_input.get()
        new_proba = self.general_corrprob_proba_input.get()

        UploadDatas.corr_proba(self, ship, reis, trl, kodvid, bio_info, u_key, new_proba, 'general')

# выборка данных и показываем их в табличке
    def selection_data(self, ship, reis, trl, kodvid, bio_info, u_key):
        UploadDatas.select_data(self, ship, reis, trl, kodvid, bio_info, u_key, 'general')

# корректировка возраста
    def update_age(self):
        UploadDatas.correct_age(self, 'general')

# ============ Ярусная база ============
class InterfaceMethodsYarus:
# функции ======================================================
    # выбор директории csv-файлов
    # yarus
    def select_directory_csv(self, curr_tab):
        curr_tab = curr_tab

        if curr_tab == 'drop_backspaces':
            self.folder_path = filedialog.askdirectory(title="Select dir")

            self.path_entry_delete.delete(0, tk.END)
            self.path_entry_delete.insert(tk.END, self.folder_path)

            files = os.listdir(self.folder_path)
            correct_files_list = ['Y_Tral.csv', 'Y_Ulov.csv', 'Y_Biopap.csv', 'Y_Biokap.csv',
                                  'Y_Razm.csv', 'Y_Biopit.csv', 'Y_TralList.csv']
            
            # self.path_csv_path_y = os.path.join(self.path_entry_delete.get(), 'fixed_csv')
            file_path = 'C:\\temp\yarus'
            self.path_csv_path_y = os.path.join(file_path, 'fixed_csv')

            # self.files_listbox_delete.delete(0, tk.END)
            # for file in files:
            #     if file.endswith(".csv") and file in correct_files_list:
            #         self.files_listbox_delete.insert(tk.END, file)


        elif curr_tab == 'preload':
            folder_path = filedialog.askdirectory(title="Select dir")
            files = os.listdir(folder_path)
            correct_files_list = ['Y_Tral.csv', 'Y_Ulov.csv', 'Y_Biopap.csv', 'Y_Biokap.csv',
                                  'Y_Razm.csv', 'Y_Biopit.csv', 'Y_TralList.csv']
            csv_files = [i for i in files if i.endswith(".csv")]

            if set(csv_files) == set(correct_files_list):
                if folder_path == '':
                    print('Пустой путь')
                else:
                    self.yarus_preload_path_input.delete(0, tk.END)
                    self.yarus_preload_path_input.insert(tk.END, folder_path)

                    # self.file_to_delete_yarus = os.path.join(self.yarus_preload_path_input.get(), "logbio.txt")
                    file_path = 'C:\\temp\yarus'
                    self.path_csv_path_y = os.path.join(file_path, 'fixed_csv')
                    # self.path_csv_path_y = os.path.join(self.yarus_preload_path_input.get(), 'fixed_csv')
            else:
                showinfo('Информация', f'Вы выбрали не ярусные файлы!')


        elif curr_tab == 'show_csv':
            folder_path = filedialog.askdirectory(title="Select dir")

            self.path_entry_csv.delete(0, tk.END)
            self.path_entry_csv.insert(tk.END, folder_path)

            files = os.listdir(folder_path)

            self.files_listbox_csv.delete(0, tk.END)
            for file in files:
                if file.endswith(".csv"):
                    self.files_listbox_csv.insert(tk.END, file)


        elif curr_tab == 'upload_datas':
            folder_path = filedialog.askdirectory(title="Select dir")

            self.yarus_onload_path_input.delete(0, tk.END)
            self.yarus_onload_path_input.insert(tk.END, folder_path)

            files = os.listdir(folder_path)
            file_path = 'C:\\temp\yarus'
            self.path_csv_path_y = os.path.join(file_path, 'fixed_csv')
            # self.path_csv_path_y = os.path.join(self.yarus_onload_path_input.get(), 'fixed_csv')

            # self.files_listbox_upload.delete(0, tk.END)
            # for file in files:
            #     if file.endswith(".csv"):
            #         self.files_listbox_upload.insert(tk.END, file)


        elif curr_tab == 'unloading':
            folder_path = filedialog.askdirectory(title="Select dir")

            self.yarus_filepath_upload_input.delete(0, tk.END)
            self.yarus_filepath_upload_input.insert(tk.END, folder_path)

            file_path = 'C:\\temp\yarus'
            self.path_csv_path_y = os.path.join(file_path, 'fixed_csv')
            # self.path_csv_path_y = os.path.join(self.yarus_filepath_upload_input.get(), 'fixed_csv')


# выгрузка из БД
    def unloading(self):
        path = self.yarus_filepath_upload_input.get()
        ship = self.yarus_ship_upload_input.get().upper()
        reis = self.yarus_reis_upload_input.get()
        GetTable.unloading_tables(self, ship, reis, path, 'yarus')

# журнал предзагрузки
    def make_logfile_preload(self, folder_path, base):
        # PreloadLogfile.make_logfile_preload_yarus(self, folder_path)
        folder_path = self.yarus_preload_path_input.get()
        DropBackspaces.drop_backspaces(self, folder_path, base)
        try:
            PreloadLogfile.make_logfile_preload(self, folder_path, base)
        except Exception as error:
            showinfo('Информация', f'{error}')

# загрузка в БД
    def upload_to_db(self):
        path = self.yarus_onload_path_input.get()
        DropBackspaces.drop_backspaces(self, path, 'yarus')
        UploadDatas.upload_into_db(self, path, 'yarus')

# удаление рейса
    def delete_reis(self):
        ship = self.yarus_ship_delete_input.get().upper()
        reis = self.yarus_reis_delete_input.get()
        UploadDatas.del_reis(self, ship, reis, 'yarus')

# корректировка признака рейса
    def corr_prizn_reis(self):
        UploadDatas.correct_prizn(self, self.yarus_corrprizn_ship_input.get().upper(), self.yarus_corrprizn_reis_input.get(), 
                                  self.yarus_corrprizn_przn_input.get().upper(), self.yarus_corrprizn_operator_input.get()) 

# корректировка самого рейса (позывной и номер)
    def corr_reis(self):
        old_ship = self.yarus_corrreis_oldship_input.get().upper()
        old_reis = self.yarus_corrreis_oldreis_input.get()
        new_ship = self.yarus_corrreis_newship_input.get().upper()
        new_reis = self.yarus_corrreis_newreis_input.get()

        UploadDatas.corr_reis(self, old_ship, old_reis, new_ship, new_reis, 'yarus')

# корректировка пробы
    def corr_prob(self):
        ship = self.yarus_corrprob_ship_input.get().upper()
        reis = self.yarus_corrprob_reis_input.get()
        trl = self.yarus_corrprob_trl_input.get().split(',')
        kodvid = self.yarus_corrprob_kodvid_input.get()
        bio_info = self.yarus_corrprob_bioinfo_input.get()
        u_key = self.yarus_corrprob_ukey_input.get()
        new_proba = self.yarus_corrprob_proba_input.get()

        UploadDatas.corr_proba(self, ship, reis, trl, kodvid, bio_info, u_key, new_proba, 'yarus')

# выборка данных и показыванье в табличке
    def selection_data(self, ship, reis, trl, kodvid, bio_info, u_key):
        UploadDatas.select_data(self, ship, reis, trl, kodvid, bio_info, u_key, 'yarus')

# корректировка возраста
    def update_age(self):
        UploadDatas.correct_age(self, 'yarus')

        
# ============ Норвежская база ============
class InterfaceMethodsNorway:
# функции ======================================================
    # выбор директории csv-файлов
    def select_directory_csv(self, curr_tab):
        curr_tab = curr_tab

        if curr_tab == 'parse_norjaa':
            folder_path = filedialog.askdirectory(title="Select dir")

            self.norway_parse_path_input.delete(0, tk.END)
            self.norway_parse_path_input.insert(tk.END, folder_path)
    
            files = os.listdir(folder_path)
            self.output_logger.delete('1.0', tk.END)
            for file in files:
                if file.endswith(".dat"):
                    self.output_logger.insert(tk.END, f"Выбран файл: {file}")

        elif curr_tab == 'upload_datas':
            folder_path = filedialog.askdirectory(title="Select dir")

            self.norway_onload_path_input.delete(0, tk.END)
            self.norway_onload_path_input.insert(tk.END, folder_path)

            files = os.listdir(folder_path)

        elif curr_tab == 'unloading':
            folder_path = filedialog.askdirectory(title="Select dir")

            self.norway_filepath_upload_input.delete(0, tk.END)
            self.norway_filepath_upload_input.insert(tk.END, folder_path)

# распарсить норвежский dat-файл
    def parse(self):
        path = self.norway_parse_path_input.get()
        dialog = customtkinter.CTkInputDialog(text="Введите код рыбки:", title="Код рыбки")
        # self.output_logger.delete(0, tk.END)
        try:
            NorjaaParser.parse_norjaa_files(self, path, dialog.get_input())
        except Exception as e:
            showinfo(title="Информация", message=f"Ошибка: {e}")

# выгрузка из БД
    def unloading(self):
        path = self.norway_filepath_upload_input.get()
        ship = self.norway_ship_upload_input.get().upper()
        reis = self.norway_reis_upload_input.get()
        GetTable.unloading_tables(self, ship, reis, path, 'norway')

# загрузка данных в БД
    def upload_to_db(self):
        path = self.norway_onload_path_input.get()
        dialog = customtkinter.CTkInputDialog(text="Введите код рыбки:", title="Код рыбки")
        try:
            NorjaaParser.parse_norjaa_files(self, path, dialog.get_input())
        except Exception as e:
            showinfo(title="Информация", message=f"Ошибка: {e}")
            
        UploadDatas.upload_into_db(self, path, 'norway')

# удаление рейса из БД
    def delete_reis(self):
        ship = self.norway_ship_delete_input.get().upper()
        reis = self.norway_reis_delete_input.get()
        UploadDatas.del_reis(self, ship, reis, 'norway')
