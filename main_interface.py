import customtkinter
import os
import shutil
import sys
from tkinter import Tk, Button, Canvas
from PIL import Image, ImageFont
from Database import Database
from Database import GetTable, UploadDatas
import tkinter as tk
from tkinter.messagebox import showinfo
import pandas as pd
from tksheet import Sheet
from PreloadLogfile import PreloadLogfile
from CSVShower import CSVShower
from tkinter import filedialog
from interface_methods import InterfaceMethodsYarus, InterfaceMethodsGeneral, InterfaceMethodsNorway
# from tkinter import ttk


class App(customtkinter.CTk):
    # ======== get ships
    def get_ships_list(self):
        connection = Database.connect_ships(self)
        cursorObj = connection.cursor()
        cursorObj.execute("SELECT ship FROM dist_ships;")
        ship_list = cursorObj.fetchall()
        ship_list = [elem[0] for elem in ship_list]

        cursorObj.close()
        connection.close()

        return ship_list
    # ==================
    
    def __init__(self):
        super().__init__()

        self.title("BioDesktop.py")
        self.geometry("1200x840")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # self.attributes('-fullscreen', True)



        # load images with light and dark mode image
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_images")
        self.logo_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "app_logo.png")), size=(26, 26))
        self.large_test_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "large_test_image.png")), size=(500, 150))
        self.image_icon_image = customtkinter.CTkImage(Image.open(os.path.join(image_path, "image_icon_light.png")), size=(20, 20))
        self.home_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "general_db_dark.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "general_db.png")), size=(20, 20))
        self.chat_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "norway_db.png")),
                                                 dark_image=Image.open(os.path.join(image_path, "norway_db.png")), size=(20, 20))
        self.add_user_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "yarus_db_dark.png")),
                                                     dark_image=Image.open(os.path.join(image_path, "yarus_db.png")), size=(20, 20))
        

        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(4, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  BioDesktop", image=self.logo_image,
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.home_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Основная база",
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                   image=self.home_image, anchor="w", command=self.home_button_event)
        self.home_button.grid(row=1, column=0, sticky="ew")

# state='disabled'
        self.frame_2_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Норвежская база",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.chat_image, anchor="w", command=self.frame_2_button_event)
        self.frame_2_button.grid(row=2, column=0, sticky="ew")

        self.frame_3_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Ярусная база",
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                      image=self.add_user_image, anchor="w", command=self.frame_3_button_event)
        self.frame_3_button.grid(row=3, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Light", "Dark", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create home frame ========================
        self.general_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color=('#F5F8FF', "#14212A"))
        # self.general_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=('#F5F8FF', "#14212A"))
        self.general_frame.grid_columnconfigure(0, weight=1)
        self.general_frame.grid_rowconfigure(0, weight=1)

        # tabs
        self.tabview_general_frame = customtkinter.CTkTabview(self.general_frame, fg_color=('#F5F8FF', "#14212A"))
        self.tabview_general_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview_general_frame.add("Манипуляции с базой")
        self.tabview_general_frame.add("Корректировка")

        self.tabview_general_frame.tab("Манипуляции с базой").grid_columnconfigure((0,1), weight=1)
        self.tabview_general_frame.tab("Манипуляции с базой").grid_rowconfigure((0,1), weight=1)
        self.tabview_general_frame.tab("Корректировка").grid_columnconfigure((0,1), weight=1)
        self.tabview_general_frame.tab("Корректировка").grid_rowconfigure((0,1), weight=1)

        # frames of tabs
        # Выгрузка
        self.general_upload_frame = customtkinter.CTkFrame(self.tabview_general_frame.tab("Манипуляции с базой"), 
                                                           fg_color=('#FAFBFF', "#02263A"), border_color=("#5C6987", "#0F9BC8"), border_width=1)
        self.general_upload_frame.grid(row=0, column=0, padx=(20, 5), pady=(20, 5), sticky="nsew")
        self.image_icon_upload = customtkinter.CTkImage(Image.open(os.path.join(image_path, "download_light.png")), size=(20, 20))
        self.general_upload_frame.grid_columnconfigure((0,1), weight=1)
        self.general_upload_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        # Корректировка признака
        self.general_corrprizn_frame = customtkinter.CTkFrame(self.tabview_general_frame.tab("Корректировка"),
                                                              fg_color=('#FAFBFF', "#02263A"), border_color=("#5C6987", "#0F9BC8"), 
                                                              border_width=1)
        self.general_corrprizn_frame.grid(row=0, column=0, padx=(20, 5), pady=(20, 5), sticky="nsew")
        self.general_corrprizn_frame.grid_columnconfigure((0,1), weight=1)
        self.general_corrprizn_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

        # Предзагрузка
        self.general_preload_frame = customtkinter.CTkFrame(self.tabview_general_frame.tab("Манипуляции с базой"), 
                                                            fg_color=('#FAFBFF', "#02263A"), border_color=("#5C6987", "#0F9BC8"), 
                                                            border_width=1)
        self.general_preload_frame.grid(row=1, column=1, padx=(20, 5), pady=(5, 20), sticky="nsew")
        self.image_icon_preload = customtkinter.CTkImage(Image.open(os.path.join(image_path, "journal_light.png")), size=(20, 20))
        self.general_preload_frame.grid_columnconfigure((0,1), weight=1)
        self.general_preload_frame.grid_rowconfigure((0,1,2,3), weight=1)
        # Корректировка рейса
        self.general_corrreis_frame = customtkinter.CTkFrame(self.tabview_general_frame.tab("Корректировка"),
                                                             fg_color=('#FAFBFF', "#02263A"), border_color=("#5C6987", "#0F9BC8"), 
                                                             border_width=1)
        self.general_corrreis_frame.grid(row=0, column=1, padx=(5, 20), pady=(20, 5), sticky="nsew")
        self.general_corrreis_frame.grid_columnconfigure((0,1), weight=1)
        self.general_corrreis_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

        # Загрузка в базу
        self.general_onload_frame = customtkinter.CTkFrame(self.tabview_general_frame.tab("Манипуляции с базой"),
                                                           fg_color=('#FAFBFF', "#02263A"), border_color=("#5C6987", "#0F9BC8"), 
                                                           border_width=1)
        self.general_onload_frame.grid(row=1, column=0, padx=(20, 5), pady=(5, 20), sticky="nsew")
        self.image_icon_onload = customtkinter.CTkImage(Image.open(os.path.join(image_path, "upload_light.png")), size=(20, 20))
        self.general_onload_frame.grid_columnconfigure((0,1), weight=1)
        self.general_onload_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
        # Корректировка пробы
        self.general_corrprob_frame = customtkinter.CTkFrame(self.tabview_general_frame.tab("Корректировка"),
                                                             fg_color=('#FAFBFF', "#02263A"), border_color=("#5C6987", "#0F9BC8"), 
                                                             border_width=1)
        self.general_corrprob_frame.grid(row=1, column=0, padx=(20, 5), pady=(5, 20), sticky="nsew")
        self.general_corrprob_frame.grid_columnconfigure((0,1), weight=1)
        self.general_corrprob_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

        # Удаление из базы
        self.general_delete_frame = customtkinter.CTkFrame(self.tabview_general_frame.tab("Манипуляции с базой"),
                                                           fg_color=('#FAFBFF', "#02263A"), border_color=("#5C6987", "#0F9BC8"), 
                                                           border_width=1)
        self.general_delete_frame.grid(row=0, column=1, padx=(20, 5), pady=(20, 5), sticky="nsew")
        self.image_icon_delete = customtkinter.CTkImage(Image.open(os.path.join(image_path, "delete_light.png")), size=(20, 20))
        self.general_delete_frame.grid_columnconfigure((0,1), weight=1)
        self.general_delete_frame.grid_rowconfigure((0,1,2,3,5,6), weight=1)
        # Корректировка возраста 
        self.general_corrvozr_frame = customtkinter.CTkFrame(self.tabview_general_frame.tab("Корректировка"),
                                                             fg_color=('#FAFBFF', "#02263A"), border_color=("#5C6987", "#0F9BC8"), 
                                                             border_width=1)
        self.general_corrvozr_frame.grid(row=1, column=1, padx=(5, 20), pady=(5, 20), sticky="nsew")
        self.general_corrvozr_frame.grid_columnconfigure((0,1), weight=1)
        self.general_corrvozr_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)


       # =========================== ВЫГРУЗКА ===========================
        self.general_upload_label = customtkinter.CTkLabel(self.general_upload_frame, text="Выгрузка из базы",
                                                           fg_color=("#E9ECF3", "#021927"), corner_radius=0, 
                                                           text_color=("#282828", "#e2e2e2"))
        self.general_upload_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.general_ship_upload_label = customtkinter.CTkLabel(self.general_upload_frame, text="Введите позывной:", 
                                                                text_color=("#282828", "#e2e2e2"))
        self.general_ship_upload_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_ship_upload_input = customtkinter.CTkEntry(self.general_upload_frame, placeholder_text="ship", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"), 
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_ship_upload_input.grid(row=2, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_reis_upload_label = customtkinter.CTkLabel(self.general_upload_frame, text="Введите № рейса:",
                                                                text_color=("#282828", "#e2e2e2"))
        self.general_reis_upload_label.grid(row=3, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_reis_upload_input = customtkinter.CTkEntry(self.general_upload_frame, placeholder_text="reis",
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"), 
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_reis_upload_input.grid(row=4, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_filepath_upload_label = customtkinter.CTkLabel(self.general_upload_frame, text="Куда выгружать:",
                                                                    text_color=("#282828", "#e2e2e2"))
        self.general_filepath_upload_label.grid(row=5, column=0, padx=(10, 10), pady=(30, 5), sticky="w")

        self.general_filepath_upload_input = customtkinter.CTkEntry(self.general_upload_frame, placeholder_text="Path:/to/dir",
                                                                  border_width=1, corner_radius=5, border_color=("#5C6987", "#0F9BC8"),
                                                                  text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"))
        self.general_filepath_upload_input.grid(row=6, column=0, padx=(10, 0), pady=(0, 10), sticky="ew")

        self.general_filepath_upload_btn = customtkinter.CTkButton(self.general_upload_frame, text="Browse...", 
                                                                   fg_color="transparent", border_color=("#5C6987", "#0F9BC8"), border_width=1,
                                                                   text_color=("#5C6987", "#E2E2E2"), hover_color=('#D8E0FF', "#04334F"),
                                                                   command=lambda: InterfaceMethodsGeneral.select_directory_csv(self,'unloading'))
        self.general_filepath_upload_btn.grid(row=6, column=1, padx=(0, 10), pady=(0, 10), sticky="w")

        self.general_upload_btn = customtkinter.CTkButton(self.general_upload_frame, text="Выгрузить", 
                                                          command=lambda: InterfaceMethodsGeneral.unloading(self),
                                                          image=self.image_icon_upload, compound="right",
                                                          text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C6987", "#0A81C4")
                                                          )
        self.general_upload_btn.grid(row=7, column=0, padx=(10, 10), pady=(30, 40), columnspan=2, sticky="ew")

        # =========================== ЖУРНАЛ ПРЕДЗАГРЗУКИ ===========================
        self.general_preload_label = customtkinter.CTkLabel(self.general_preload_frame, text="Предзагрузка данных:",
                                                            fg_color=("#E9ECF3", "#021927"), corner_radius=0, text_color=("#282828", "#e2e2e2"))
        self.general_preload_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.general_preload_label = customtkinter.CTkLabel(self.general_preload_frame, text="")
        self.general_preload_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        self.general_preload_path_label = customtkinter.CTkLabel(self.general_preload_frame, text="Откуда брать:",
                                                                 text_color=("#282828", "#e2e2e2"))
        self.general_preload_path_label.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        self.general_preload_path_input = customtkinter.CTkEntry(self.general_preload_frame, placeholder_text="Path:/to/dir",
                                                                 text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                 border_color=("#5C6987", "#0F9BC8"))
        self.general_preload_path_input.grid(row=3, column=0, padx=(10, 0), pady=(0, 10), sticky="ew")

        self.general_filepath_preload_btn = customtkinter.CTkButton(self.general_preload_frame, text="Browse...", 
                                                                    fg_color="transparent", border_color=("#5C6987", "#0F9BC8"), border_width=1,
                                                                    text_color=("#5C6987", "#E2E2E2"), hover_color=('#D8E0FF', "#04334F"),
                                                                    command=lambda: InterfaceMethodsGeneral.select_directory_csv(self,'preload'))
        self.general_filepath_preload_btn.grid(row=3, column=1, padx=(0, 0), pady=(0, 10), sticky="w")

        self.general_preload_btn = customtkinter.CTkButton(self.general_preload_frame, text="Сформировать журнал", 
                                                           text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C6987", "#0A81C4"), 
                                                           image=self.image_icon_preload, compound="right",
                                                           command=lambda: InterfaceMethodsGeneral.make_logfile_preload(self, self.general_preload_path_input.get()))
        self.general_preload_btn.grid(row=5, column=0, padx=(10, 10), pady=(30, 40), columnspan=2, sticky="ew")

        # =========================== ЗАГРЗУКА ===========================
        self.general_onload_label = customtkinter.CTkLabel(self.general_onload_frame, text="Загрузка в базу",
                                                           fg_color=("#E9ECF3", "#021927"), corner_radius=0, text_color=("#282828", "#e2e2e2"))
        self.general_onload_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.general_onload_label2 = customtkinter.CTkLabel(self.general_onload_frame, text="")
        self.general_onload_label2.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        self.general_onload_path_label = customtkinter.CTkLabel(self.general_onload_frame, text="Откуда загружать:",
                                                                text_color=("#282828", "#e2e2e2"))
        self.general_onload_path_label.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        self.general_onload_path_input = customtkinter.CTkEntry(self.general_onload_frame, placeholder_text="Path:/to/dir",
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_onload_path_input.grid(row=3, column=0, padx=(10, 0), pady=(0, 10), sticky="ew")

        self.general_filepath_onload_btn = customtkinter.CTkButton(self.general_onload_frame, text="Browse...", 
                                                                   fg_color="transparent", border_color=("#5C6987", "#0F9BC8"), border_width=1,
                                                                   text_color=("#5C6987", "#E2E2E2"), hover_color=('#D8E0FF', "#04334F"),
                                                                   command=lambda: InterfaceMethodsGeneral.select_directory_csv(self,'upload_datas'))
        self.general_filepath_onload_btn.grid(row=3, column=1, padx=(0, 0), pady=(0, 10), sticky="w")

        self.general_onload_btn = customtkinter.CTkButton(self.general_onload_frame, text="Загрузить", 
                                                          text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C6987", "#0A81C4"),
                                                          image=self.image_icon_onload, compound="right",
                                                          command=lambda: InterfaceMethodsGeneral.upload_to_db(self))
        self.general_onload_btn.grid(row=4, column=0, padx=(10, 10), pady=(30, 40), columnspan=2, sticky="ew")

        # =========================== УДАЛЕНИЕ ===========================
        self.general_delete_label = customtkinter.CTkLabel(self.general_delete_frame, text="Удаление из базы",
                                                           fg_color=("#E9ECF3", "#021927"), corner_radius=0, text_color=("#282828", "#e2e2e2"))
        self.general_delete_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")
        
        self.label1 = customtkinter.CTkLabel(self.general_delete_frame, text="")
        self.label1.grid(row=1, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.general_ship_delete_label = customtkinter.CTkLabel(self.general_delete_frame, text="Введите позывной:",
                                                                text_color=("#282828", "#e2e2e2"))
        self.general_ship_delete_label.grid(row=2, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_ship_delete_input = customtkinter.CTkEntry(self.general_delete_frame, placeholder_text="ship",
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_ship_delete_input.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_reis_delete_label = customtkinter.CTkLabel(self.general_delete_frame, text="Введите № рейса:",
                                                                text_color=("#282828", "#e2e2e2"))
        self.general_reis_delete_label.grid(row=4, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_reis_delete_input = customtkinter.CTkEntry(self.general_delete_frame, placeholder_text="reis",
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_reis_delete_input.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_delete_btn = customtkinter.CTkButton(self.general_delete_frame, text="Удалить", 
                                                          text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C6987", "#0A81C4"), 
                                                          image=self.image_icon_delete, compound="right",
                                                          command=lambda: InterfaceMethodsGeneral.delete_reis(self))
        self.general_delete_btn.grid(row=6, column=0, padx=(10, 10), pady=(30, 40), columnspan=2, sticky="ew")

        # =========================== таб Корректировка признака 1 ===========================
        self.general_corrprizn_lable = customtkinter.CTkLabel(self.general_corrprizn_frame, text="Коректировка признака",
                                                              fg_color=("#E9ECF3", "#021927"), corner_radius=0,
                                                              text_color=("#282828", "#e2e2e2"))
        self.general_corrprizn_lable.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")
        
        self.general_corrprizn_title1_lable = customtkinter.CTkLabel(self.general_corrprizn_frame, text="Где меняем признак:",
                                                                     fg_color=("#E9ECF3", "#021927"),
                                                                     text_color=("#282828", "#e2e2e2"))
        self.general_corrprizn_title1_lable.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrprizn_ship_lable = customtkinter.CTkLabel(self.general_corrprizn_frame, text="Введите позывной:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.general_corrprizn_ship_lable.grid(row=2, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrprizn_ship_input = customtkinter.CTkEntry(self.general_corrprizn_frame, placeholder_text="ship", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrprizn_ship_input.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrprizn_reis_lable = customtkinter.CTkLabel(self.general_corrprizn_frame, text="Введите № рейса:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.general_corrprizn_reis_lable.grid(row=4, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrprizn_reis_input = customtkinter.CTkEntry(self.general_corrprizn_frame, placeholder_text="reis", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrprizn_reis_input.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrprizn_title2_lable = customtkinter.CTkLabel(self.general_corrprizn_frame, text="Введите новые параметры, где:\n1 - совместный\n2 - из АтлантНИРО",
                                                                     fg_color=("#E9ECF3", "#021927"), justify="left",
                                                                     text_color=("#282828", "#e2e2e2"))
        self.general_corrprizn_title2_lable.grid(row=6, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrprizn_przn_lable = customtkinter.CTkLabel(self.general_corrprizn_frame, text="Новый признак рейса:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.general_corrprizn_przn_lable.grid(row=7, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrprizn_przn_input = customtkinter.CTkEntry(self.general_corrprizn_frame, placeholder_text="przn", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrprizn_przn_input.grid(row=8, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrprizn_operator_lable = customtkinter.CTkLabel(self.general_corrprizn_frame, text="Новый оператор:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.general_corrprizn_operator_lable.grid(row=9, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrprizn_operator_input = customtkinter.CTkEntry(self.general_corrprizn_frame, placeholder_text="operator", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrprizn_operator_input.grid(row=10, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrprizn_btn = customtkinter.CTkButton(self.general_corrprizn_frame, text="Применить", 
                                                           text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C6987", "#0A81C4"),
                                                           command=lambda: InterfaceMethodsGeneral.corr_prizn_reis(self))
        self.general_corrprizn_btn.grid(row=11, column=0, padx=(10, 10), pady=(40, 30), columnspan=2, sticky="ew")

        # =========================== таб Корректировка рейса 2 ===========================
        self.general_corrreis_lable = customtkinter.CTkLabel(self.general_corrreis_frame, text="Коректировка рейса",
                                                              fg_color=("#E9ECF3", "#021927"), corner_radius=0,
                                                              text_color=("#282828", "#e2e2e2"))
        self.general_corrreis_lable.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.general_corrreis_title1_lable = customtkinter.CTkLabel(self.general_corrreis_frame, text="Где меняем рейс:",
                                                                     fg_color=("#E9ECF3", "#021927"),
                                                                     text_color=("#282828", "#e2e2e2"))
        self.general_corrreis_title1_lable.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrreis_oldship_lable = customtkinter.CTkLabel(self.general_corrreis_frame, text="Введите старый позывной:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.general_corrreis_oldship_lable.grid(row=2, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrreis_oldship_input = customtkinter.CTkEntry(self.general_corrreis_frame, placeholder_text="ship", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrreis_oldship_input.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrreis_oldreis_lable = customtkinter.CTkLabel(self.general_corrreis_frame, text="Введите старый № рейса:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.general_corrreis_oldreis_lable.grid(row=4, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrreis_oldreis_input = customtkinter.CTkEntry(self.general_corrreis_frame, placeholder_text="reis", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrreis_oldreis_input.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrreis_title2_lable = customtkinter.CTkLabel(self.general_corrreis_frame, text="Введите новые параметры:",
                                                                     fg_color=("#E9ECF3", "#021927"), justify="left",
                                                                     text_color=("#282828", "#e2e2e2"))
        self.general_corrreis_title2_lable.grid(row=6, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrreis_newship_lable = customtkinter.CTkLabel(self.general_corrreis_frame, text="Введите новый позывной:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.general_corrreis_newship_lable.grid(row=7, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrreis_newship_input = customtkinter.CTkEntry(self.general_corrreis_frame, placeholder_text="ship", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrreis_newship_input.grid(row=8, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrreis_newreis_lable = customtkinter.CTkLabel(self.general_corrreis_frame, text="Введите новый № рейса:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.general_corrreis_newreis_lable.grid(row=9, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrreis_newreis_input = customtkinter.CTkEntry(self.general_corrreis_frame, placeholder_text="reis", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrreis_newreis_input.grid(row=10, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")
        
        self.general_corrreis_btn = customtkinter.CTkButton(self.general_corrreis_frame, text="Применить", 
                                                           text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C6987", "#0A81C4"),
                                                           command=lambda: InterfaceMethodsGeneral.corr_reis(self))
        self.general_corrreis_btn.grid(row=11, column=0, padx=(10, 10), pady=(40, 30), columnspan=2, sticky="ew")

        # =========================== таб Корректировка пробы 3 ===========================
        self.general_corrprob_label = customtkinter.CTkLabel(self.general_corrprob_frame, text="Коректировка пробы",
                                                              fg_color=("#E9ECF3", "#021927"), corner_radius=0,
                                                              text_color=("#282828", "#e2e2e2"))
        self.general_corrprob_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.general_corrprob_title1_label = customtkinter.CTkLabel(self.general_corrprob_frame, text="Параметры, где будем менять пробу:",
                                                                     fg_color=("#E9ECF3", "#021927"),
                                                                     text_color=("#282828", "#e2e2e2"))
        self.general_corrprob_title1_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrprob_ship_input = customtkinter.CTkEntry(self.general_corrprob_frame, placeholder_text="Позывной", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrprob_ship_input.grid(row=2, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrprob_reis_input = customtkinter.CTkEntry(self.general_corrprob_frame, placeholder_text="№ рейса", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrprob_reis_input.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrprob_trl_input = customtkinter.CTkEntry(self.general_corrprob_frame, placeholder_text="Тралы (через запятую)", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrprob_trl_input.grid(row=4, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrprob_kodvid_input = customtkinter.CTkEntry(self.general_corrprob_frame, placeholder_text="Код объекта", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrprob_kodvid_input.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrprob_bioinfo_input = customtkinter.CTkEntry(self.general_corrprob_frame, placeholder_text="bio_info", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrprob_bioinfo_input.grid(row=6, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrprob_ukey_input = customtkinter.CTkEntry(self.general_corrprob_frame, placeholder_text="u_key", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrprob_ukey_input.grid(row=7, column=0, padx=(10, 10), pady=(0, 10), sticky="ew") 

        self.general_corrprob_title2_label = customtkinter.CTkLabel(self.general_corrprob_frame, text="Новая проба:",
                                                                     fg_color=("#E9ECF3", "#021927"),
                                                                     text_color=("#282828", "#e2e2e2"))
        self.general_corrprob_title2_label.grid(row=8, column=0, padx=(10, 10), pady=(10, 5), sticky="w")   

        self.general_corrprob_proba_input = customtkinter.CTkEntry(self.general_corrprob_frame, placeholder_text="Новая проба", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrprob_proba_input.grid(row=9, column=0, padx=(10, 10), pady=(0, 10), sticky="ew") 

        self.general_corrprob_btn = customtkinter.CTkButton(self.general_corrprob_frame, text="Применить", 
                                                           text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C6987", "#0A81C4"),
                                                           command=lambda: InterfaceMethodsGeneral.corr_prob(self))
        self.general_corrprob_btn.grid(row=10, column=0, padx=(10, 10), pady=(40, 30), columnspan=2, sticky="ew")

        # =========================== таб Корректировка возраста 4 ===========================
        self.general_corrvozr_label = customtkinter.CTkLabel(self.general_corrvozr_frame, text="Коректировка возраста",
                                                              fg_color=("#E9ECF3", "#021927"), corner_radius=0,
                                                              text_color=("#282828", "#e2e2e2"))
        self.general_corrvozr_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.general_corrvozr_title1_label = customtkinter.CTkLabel(self.general_corrvozr_frame, text="Введите параметры для выборки:",
                                                                     fg_color=("#E9ECF3", "#021927"),
                                                                     text_color=("#282828", "#e2e2e2"))
        self.general_corrvozr_title1_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.general_corrvozr_ship_input = customtkinter.CTkEntry(self.general_corrvozr_frame, placeholder_text="Позывной", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrvozr_ship_input.grid(row=2, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrvozr_reis_input = customtkinter.CTkEntry(self.general_corrvozr_frame, placeholder_text="№ рейса", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrvozr_reis_input.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrvozr_trl_input = customtkinter.CTkEntry(self.general_corrvozr_frame, placeholder_text="Трал (один)", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                border_color=("#5C6987", "#0F9BC8"))
        self.general_corrvozr_trl_input.grid(row=4, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrvozr_kodvid_input = customtkinter.CTkEntry(self.general_corrvozr_frame, placeholder_text="Код объекта", 
                                                                    text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                    border_color=("#5C6987", "#0F9BC8"))
        self.general_corrvozr_kodvid_input.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrvozr_bioinfo_input = customtkinter.CTkEntry(self.general_corrvozr_frame, placeholder_text="bio_info", 
                                                                    text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                    border_color=("#5C6987", "#0F9BC8"))
        self.general_corrvozr_bioinfo_input.grid(row=6, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.general_corrvozr_ukey_input = customtkinter.CTkEntry(self.general_corrvozr_frame, placeholder_text="u_key", 
                                                                  text_color=("#5C6987", "#FFFFFF"), fg_color=("#FFFDF9", "#021927"),
                                                                  border_color=("#5C6987", "#0F9BC8"))
        self.general_corrvozr_ukey_input.grid(row=7, column=0, padx=(10, 10), pady=(0, 10), sticky="ew") 

        self.general_corrvozr_select_btn = customtkinter.CTkButton(self.general_corrvozr_frame, text="Выбрать", 
                                                           text_color=("#5C6987", "#E2E2E2"), fg_color=("#FFFDF9", "#021927"),
                                                           border_color=("#5C6987", "#0F9BC8"), border_width=1,hover_color=('#D8E0FF', "#04334F"),
                                                           command=lambda: InterfaceMethodsGeneral.selection_data(self, self.general_corrvozr_ship_input.get().upper(), self.general_corrvozr_reis_input.get(),
                                                                                                                        self.general_corrvozr_trl_input.get(), self.general_corrvozr_kodvid_input.get(),
                                                                                                                        self.general_corrvozr_bioinfo_input.get(), self.general_corrvozr_ukey_input.get()))
        self.general_corrvozr_select_btn.grid(row=8, column=0, padx=(10, 10), pady=(10, 30), columnspan=1, sticky="ew")

        dict_test = {'A': [1, 2, 3], 'B': [1, 2, 3]}
        df = pd.DataFrame(dict_test)

        data = [[j for j in i[1:]] for i in df.itertuples()]
        header = ['bikl', 'ship','reis','trl','kodvid','n_fish','bio_info','u_key','vozr1','vozr2','l_big','l_lit','n_ring']
        self.sheet = Sheet(self.general_corrvozr_frame,
                           data = data,
                           header=header,
                           theme = "dark",
                           width=650)
        self.sheet.enable_bindings("all", "edit_header", "edit_index")
        self.sheet.set_all_cell_sizes_to_text()
        self.sheet.grid(row=9, column=0, padx=(10, 10), pady=(10, 30), sticky = "nswe")

        self.general_corrvozr_btn = customtkinter.CTkButton(self.general_corrvozr_frame, text="Скорректировать", 
                                                            text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C6987", "#0A81C4"),
                                                            command=lambda: InterfaceMethodsGeneral.update_age(self))
        self.general_corrvozr_btn.grid(row=10, column=0, padx=(10, 10), pady=(10, 30), columnspan=2, sticky="ew")



        # create second frame NORWAY ======================
        self.second_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color=("#FFF5F5","#2A1414"))
        self.second_frame.grid_columnconfigure((0,1), weight=1)
        self.second_frame.grid_rowconfigure((0,1), weight=1)

        self.image_icon_parse = customtkinter.CTkImage(Image.open(os.path.join(image_path, "parse_icon.png")), size=(20, 20))

        # frames
        # Парсинг
        self.norway_parse_frame = customtkinter.CTkFrame(self.second_frame, fg_color=('#FFFAFA', "#3A0202"), 
                                                         border_color=("#4F0404","#C80F0F"), border_width=1)
        self.norway_parse_frame.grid(row=0, column=0, padx=(20, 5), pady=(20, 5), columnspan='2', sticky="nsew")
        self.norway_parse_frame.grid_columnconfigure((0,1), weight=1)
        self.norway_parse_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)

        # Выгрузка
        # self.norway_upload_frame = customtkinter.CTkFrame(self.second_frame, fg_color=('#FFFAFA', "#3A0202"),
        #                                                  border_color=("#4F0404","#C80F0F"), border_width=1)
        # self.norway_upload_frame.grid(row=0, column=1, padx=(20, 20), pady=(20, 5), sticky="nsew")
        # self.norway_upload_frame.grid_columnconfigure((0,1), weight=1)
        # self.norway_upload_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)

        # Загрузка
        self.norway_onload_frame = customtkinter.CTkFrame(self.second_frame, fg_color=('#FFFAFA', "#3A0202"), 
                                                         border_color=("#4F0404","#C80F0F"), border_width=1)
        self.norway_onload_frame.grid(row=1, column=0, padx=(20, 5), pady=(20, 20), sticky="nsew")
        self.norway_onload_frame.grid_columnconfigure((0,1), weight=1)
        self.norway_onload_frame.grid_rowconfigure((0,1,2), weight=1)

        # Удаление
        self.norway_delete_frame = customtkinter.CTkFrame(self.second_frame, fg_color=('#FFFAFA', "#3A0202"), 
                                                         border_color=("#4F0404","#C80F0F"), border_width=1)
        self.norway_delete_frame.grid(row=1, column=1, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.norway_delete_frame.grid_columnconfigure((0,1), weight=1)
        self.norway_delete_frame.grid_rowconfigure((0,1,2,3), weight=1)  

        # =========================== ПАРСИНГ ===========================
        self.norway_parse_label = customtkinter.CTkLabel(self.norway_parse_frame, text="Распарсить норвежский DAT-файл",
                                                         fg_color=("#F3E9E9", "#270202"), corner_radius=0,
                                                         text_color=("#282828", "#e2e2e2"))
        self.norway_parse_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.norway_filepath_parse_label = customtkinter.CTkLabel(self.norway_parse_frame, text="Выберите dat-файл:",
                                                                  text_color=("#282828", "#e2e2e2"))
        self.norway_filepath_parse_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.norway_parse_path_input = customtkinter.CTkEntry(self.norway_parse_frame, placeholder_text="Path:/to/file",
                                                                  border_width=1, corner_radius=5, border_color=("#875C5C", "#C80F0F"),
                                                                  text_color=("#E2E2E2", "#FFFFFF"), fg_color=("#FFF9F9", "#270202"))
        self.norway_parse_path_input.grid(row=2, column=0, padx=(10, 0), pady=(0, 10), sticky="ew")

        self.norway_filepath_parse_btn = customtkinter.CTkButton(self.norway_parse_frame, text="Browse...", 
                                                                 fg_color=("#FFF9F9", "#270202"), border_color=("#875C5C", "#C80F0F"), border_width=1,
                                                                 text_color=("#875C5C", "#f2f2f2"), hover_color=('#FFD8D8', "#4F0404"),
                                                                 command=lambda: InterfaceMethodsNorway.select_directory_csv(self,'parse_norjaa'))
        self.norway_filepath_parse_btn.grid(row=2, column=1, padx=(0, 10), pady=(0, 10), sticky="w")

        self.norway_parse_btn = customtkinter.CTkButton(self.norway_parse_frame, text="Распарсить", 
                                                        text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#875C5C","#C40A0A"),
                                                        image=self.image_icon_parse, compound="right",hover_color=('#6A4848', "#790606"),
                                                        command=lambda: InterfaceMethodsNorway.parse(self))
        self.norway_parse_btn.grid(row=3, column=0, padx=(10, 10), pady=(30, 40), columnspan=1, sticky="ew")

        self.output_logger_label = customtkinter.CTkLabel(master=self.norway_parse_frame, text='Окно информации')
        self.output_logger_label.grid(row=4, column=0, padx=(10, 10), pady=(10, 0), sticky="w")

        self.output_logger = customtkinter.CTkTextbox(master=self.norway_parse_frame, corner_radius=15, activate_scrollbars=True,
                                                      border_color=("#875C5C", "#C80F0F"), border_width=1)
        self.output_logger.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), columnspan=2, sticky="ew")

        # =========================== ВЫГРУЗКА ===========================
        # self.norway_upload_label = customtkinter.CTkLabel(self.norway_upload_frame, text="Выгрузка из базы",
        #                                                  fg_color=("#F3E9E9", "#270202"), corner_radius=0,
        #                                                  text_color=("#282828", "#e2e2e2"))
        # self.norway_upload_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        # self.norway_ship_upload_label = customtkinter.CTkLabel(self.norway_upload_frame, text="Введите позывной:",
        #                                                       text_color=("#282828", "#e2e2e2"))
        # self.norway_ship_upload_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        # self.norway_ship_upload_input = customtkinter.CTkEntry(self.norway_upload_frame, placeholder_text="ship",
        #                                                       text_color=("#E2E2E2", "#FFFFFF"), fg_color=("#FFF9F9", "#270202"),
        #                                                       border_color=("#875C5C", "#C80F0F"), corner_radius=5)
        # self.norway_ship_upload_input.grid(row=2, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        # self.norway_reis_upload_label = customtkinter.CTkLabel(self.norway_upload_frame, text="Введите № рейса:",
        #                                                       text_color=("#282828", "#e2e2e2"))
        # self.norway_reis_upload_label.grid(row=3, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        # self.norway_reis_upload_input = customtkinter.CTkEntry(self.norway_upload_frame, placeholder_text="reis",
        #                                                       text_color=("#E2E2E2", "#FFFFFF"), fg_color=("#FFF9F9", "#270202"),
        #                                                       border_color=("#875C5C", "#C80F0F"), corner_radius=5)
        # self.norway_reis_upload_input.grid(row=4, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        # self.norway_filepath_upload_label = customtkinter.CTkLabel(self.norway_upload_frame, text="Куда выгружать:",
        #                                                           text_color=("#282828", "#e2e2e2"))
        # self.norway_filepath_upload_label.grid(row=5, column=0, padx=(10, 10), pady=(30, 5), sticky="w")

        # self.norway_filepath_upload_input = customtkinter.CTkEntry(self.norway_upload_frame, placeholder_text="Path:/to/dir",
        #                                                           border_width=1, corner_radius=5, border_color=("#875C5C", "#C80F0F"),
        #                                                           text_color=("#E2E2E2", "#FFFFFF"), fg_color=("#FFF9F9", "#270202"))
        # self.norway_filepath_upload_input.grid(row=6, column=0, padx=(10, 0), pady=(0, 10), sticky="ew")

        # self.norway_filepath_upload_btn = customtkinter.CTkButton(self.norway_upload_frame, text="Browse...", 
        #                                                          fg_color=("#FFF9F9", "#270202"), border_color=("#875C5C", "#C80F0F"), border_width=1,
        #                                                          text_color=("#875C5C", "#f2f2f2"), hover_color=('#FFD8D8', "#4F0404"),
        #                                                          command=lambda: InterfaceMethodsNorway.select_directory_csv(self,'unloading'))
        # self.norway_filepath_upload_btn.grid(row=6, column=1, padx=(0, 10), pady=(0, 10), sticky="w")

        # self.norway_upload_btn = customtkinter.CTkButton(self.norway_upload_frame, text="Выгрузить", 
        #                                                 text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#875C5C","#C40A0A"),
        #                                                 image=self.image_icon_upload, compound="right",hover_color=('#6A4848', "#790606"),
        #                                                 command=lambda: InterfaceMethodsNorway.unloading(self))
        # self.norway_upload_btn.grid(row=7, column=0, padx=(10, 10), pady=(30, 40), columnspan=2, sticky="ew")

        # =========================== ЗАГРУЗКА ===========================
        self.norway_onload_label = customtkinter.CTkLabel(self.norway_onload_frame, text="Загрузка в базу",
                                                         fg_color=("#F3E9E9", "#270202"), corner_radius=0,
                                                         text_color=("#282828", "#e2e2e2"))
        self.norway_onload_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.norway_onload_label2 = customtkinter.CTkLabel(self.norway_onload_frame, text="")
        self.norway_onload_label2.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.norway_onload_path_label = customtkinter.CTkLabel(self.norway_onload_frame, text="Откуда загружать:",
                                                              text_color=("#282828", "#e2e2e2"))
        self.norway_onload_path_label.grid(row=2, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        self.norway_onload_path_input = customtkinter.CTkEntry(self.norway_onload_frame, placeholder_text="Path:/to/dir",
                                                              border_width=1, corner_radius=5, border_color=("#875C5C", "#C80F0F"),
                                                              text_color=("#E2E2E2", "#FFFFFF"), fg_color=("#FFF9F9", "#270202"))
        self.norway_onload_path_input.grid(row=3, column=0, padx=(10, 0), pady=(10, 10), sticky="ew")

        self.norway_filepath_onload_btn = customtkinter.CTkButton(self.norway_onload_frame, text="Browse...",
                                                                  fg_color=("#FFF9F9", "#270202"), border_color=("#875C5C", "#C80F0F"), border_width=1,
                                                                  text_color=("#875C5C", "#f2f2f2"), hover_color=('#FFD8D8', "#4F0404"),
                                                                  command=lambda: InterfaceMethodsNorway.select_directory_csv(self,'upload_datas'))
        self.norway_filepath_onload_btn.grid(row=3, column=1, padx=(0, 0), pady=(10, 10), sticky="w")

        self.norway_onload_btn = customtkinter.CTkButton(self.norway_onload_frame, text="Загрузить", 
                                                        text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#875C5C","#C40A0A"),
                                                        image=self.image_icon_onload, compound="right", hover_color=('#6A4848', "#790606"),
                                                        command=lambda: InterfaceMethodsNorway.upload_to_db(self))
        self.norway_onload_btn.grid(row=4, column=0, padx=(10, 10), pady=(30, 40), columnspan=2, sticky="ew")

        # =========================== УДАЛЕНИЕ ===========================
        self.norway_delete_label = customtkinter.CTkLabel(self.norway_delete_frame, text="Удаление из базы",
                                                         fg_color=("#F3E9E9", "#270202"), corner_radius=0,
                                                         text_color=("#282828", "#e2e2e2"))
        self.norway_delete_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.norway_delete_label2 = customtkinter.CTkLabel(self.norway_delete_frame, text="")
        self.norway_delete_label2.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.norway_ship_delete_label = customtkinter.CTkLabel(self.norway_delete_frame, text="Введите год:",
                                                              text_color=("#282828", "#e2e2e2"))
        self.norway_ship_delete_label.grid(row=2, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.norway_ship_delete_input = customtkinter.CTkEntry(self.norway_delete_frame, placeholder_text="year",
                                                               border_width=1, corner_radius=5, border_color=("#875C5C", "#C80F0F"),
                                                               text_color=("#E2E2E2", "#FFFFFF"), fg_color=("#FFF9F9", "#270202"))
        self.norway_ship_delete_input.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.norway_reis_delete_label = customtkinter.CTkLabel(self.norway_delete_frame, text="Введите код рыбки:",
                                                              text_color=("#282828", "#e2e2e2"))
        self.norway_reis_delete_label.grid(row=4, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.norway_reis_delete_input = customtkinter.CTkEntry(self.norway_delete_frame, placeholder_text="kodvid",
                                                               border_width=1, corner_radius=5, border_color=("#875C5C", "#C80F0F"),
                                                               text_color=("#E2E2E2", "#FFFFFF"), fg_color=("#FFF9F9", "#270202"))
        self.norway_reis_delete_input.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.norway_delete_btn = customtkinter.CTkButton(self.norway_delete_frame, text="Удалить",
                                                        text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#875C5C","#C40A0A"),
                                                        image=self.image_icon_delete, compound="right",hover_color=('#6A4848', "#790606"),
                                                        command=lambda: InterfaceMethodsNorway.delete_reis(self))
        self.norway_delete_btn.grid(row=6, column=0, padx=(10, 10), pady=(30, 40), columnspan=2, sticky="ew")





        # create third frame YARUS ======================
        self.third_frame = customtkinter.CTkScrollableFrame(self, corner_radius=0, fg_color=("#F5FFFC","#142A23"))
        self.third_frame.grid_columnconfigure(0, weight=1)
        self.third_frame.grid_rowconfigure(0, weight=1)

        # tabs
        self.tabview_third_frame = customtkinter.CTkTabview(self.third_frame, fg_color=("#F5FFFC","#142A23"))
        self.tabview_third_frame.grid(row=0, column=0, padx=(20, 20), pady=(20, 20), sticky="nsew")
        self.tabview_third_frame.add("Манипуляции с базой")
        self.tabview_third_frame.add("Корректировка")

        self.tabview_third_frame.tab("Манипуляции с базой").grid_columnconfigure((0,1), weight=1)  # configure grid of individual tabs
        self.tabview_third_frame.tab("Манипуляции с базой").grid_rowconfigure((0,1), weight=1)
        self.tabview_third_frame.tab("Корректировка").grid_columnconfigure((0,1), weight=1)  # configure grid of individual tabs
        self.tabview_third_frame.tab("Корректировка").grid_rowconfigure((0,1), weight=1)

        # frames of tabs
        # Выгрузка
        self.yarus_upload_frame = customtkinter.CTkFrame(self.tabview_third_frame.tab("Манипуляции с базой"),
                                                         fg_color=('#FAFFFD', "#023A27"), border_color=("#5C8779", "#0FC88A"), border_width=1)
        self.yarus_upload_frame.grid(row=0, column=0, padx=(20, 5), pady=(20, 5), sticky="nsew")
        self.yarus_upload_frame.grid_columnconfigure((0,1), weight=1)
        self.yarus_upload_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8), weight=1)
        # Корректировка признака
        self.yarus_corrprizn_frame = customtkinter.CTkFrame(self.tabview_third_frame.tab("Корректировка"),
                                                              fg_color=('#FAFFFD', "#023A27"), border_color=("#5C8779", "#0FC88A"), border_width=1)
        self.yarus_corrprizn_frame.grid(row=0, column=0, padx=(20, 5), pady=(20, 5), sticky="nsew")
        self.yarus_corrprizn_frame.grid_columnconfigure((0,1), weight=1)
        self.yarus_corrprizn_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)     
        
        # Предзагрузка
        self.yarus_preload_frame = customtkinter.CTkFrame(self.tabview_third_frame.tab("Манипуляции с базой"),
                                                          fg_color=('#FAFFFD', "#023A27"), border_color=("#5C8779", "#0FC88A"), border_width=1)
        self.yarus_preload_frame.grid(row=1, column=1, padx=(20, 5), pady=(5, 20), sticky="nsew")
        self.yarus_preload_frame.grid_columnconfigure((0,1), weight=1)
        self.yarus_preload_frame.grid_rowconfigure((0,1,2,3), weight=1)
        # Корректировка рейса
        self.yarus_corrreis_frame = customtkinter.CTkFrame(self.tabview_third_frame.tab("Корректировка"),
                                                             fg_color=('#FAFFFD', "#023A27"), border_color=("#5C8779", "#0FC88A"), border_width=1)
        self.yarus_corrreis_frame.grid(row=0, column=1, padx=(5, 20), pady=(20, 5), sticky="nsew")
        self.yarus_corrreis_frame.grid_columnconfigure((0,1), weight=1)
        self.yarus_corrreis_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

        # Загрузка в бд
        self.yarus_onload_frame = customtkinter.CTkFrame(self.tabview_third_frame.tab("Манипуляции с базой"),
                                                         fg_color=('#FAFFFD', "#023A27"), border_color=("#5C8779", "#0FC88A"), border_width=1)
        self.yarus_onload_frame.grid(row=1, column=0, padx=(20, 5), pady=(5, 20), sticky="nsew")
        self.yarus_onload_frame.grid_columnconfigure((0,1), weight=1)
        self.yarus_onload_frame.grid_rowconfigure((0,1,2,3,4), weight=1)
        # Корретировка пробы
        self.yarus_corrprob_frame = customtkinter.CTkFrame(self.tabview_third_frame.tab("Корректировка"),
                                                             fg_color=('#FAFFFD', "#023A27"), border_color=("#5C8779", "#0FC88A"), border_width=1)
        self.yarus_corrprob_frame.grid(row=1, column=0, padx=(20, 5), pady=(5, 20), sticky="nsew")
        self.yarus_corrprob_frame.grid_columnconfigure((0,1), weight=1)
        self.yarus_corrprob_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)

        # Удаление
        self.yarus_delete_frame = customtkinter.CTkFrame(self.tabview_third_frame.tab("Манипуляции с базой"),
                                                         fg_color=('#FAFFFD', "#023A27"), border_color=("#5C8779", "#0FC88A"), border_width=1)
        self.yarus_delete_frame.grid(row=0, column=1, padx=(20, 5), pady=(20, 5), sticky="nsew")
        self.yarus_delete_frame.grid_columnconfigure((0,1), weight=1)
        self.yarus_delete_frame.grid_rowconfigure((0,1,2,3,5,6), weight=1)
        # Коррективка возраста
        self.yarus_corrvozr_frame = customtkinter.CTkFrame(self.tabview_third_frame.tab("Корректировка"),
                                                             fg_color=('#FAFFFD', "#023A27"), border_color=("#5C8779", "#0FC88A"), border_width=1)
        self.yarus_corrvozr_frame.grid(row=1, column=1, padx=(5, 20), pady=(5, 20), sticky="nsew")
        self.yarus_corrvozr_frame.grid_columnconfigure((0,1), weight=1)
        self.yarus_corrvozr_frame.grid_rowconfigure((0,1,2,3,4,5,6,7,8,9,10,11), weight=1)


        # =========================== ВЫГРУЗКА ===========================
        self.yarus_upload_label = customtkinter.CTkLabel(self.yarus_upload_frame, text="Выгрузка из базы",
                                                         fg_color=("#E9F3F0", "#02271B"), corner_radius=0,
                                                         text_color=("#282828", "#e2e2e2"))
        self.yarus_upload_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.yarus_ship_upload_label = customtkinter.CTkLabel(self.yarus_upload_frame, text="Введите позывной:",
                                                              text_color=("#282828", "#e2e2e2"))
        self.yarus_ship_upload_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_ship_upload_input = customtkinter.CTkEntry(self.yarus_upload_frame, placeholder_text="ship",
                                                              text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                              border_color=("#5C8779", "#0FC88A"))
        self.yarus_ship_upload_input.grid(row=2, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_reis_upload_label = customtkinter.CTkLabel(self.yarus_upload_frame, text="Введите № рейса:",
                                                              text_color=("#282828", "#e2e2e2"))
        self.yarus_reis_upload_label.grid(row=3, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_reis_upload_input = customtkinter.CTkEntry(self.yarus_upload_frame, placeholder_text="reis",
                                                              text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                              border_color=("#5C8779", "#0FC88A"))
        self.yarus_reis_upload_input.grid(row=4, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_filepath_upload_label = customtkinter.CTkLabel(self.yarus_upload_frame, text="Куда выгружать:",
                                                                  text_color=("#282828", "#e2e2e2"))
        self.yarus_filepath_upload_label.grid(row=5, column=0, padx=(10, 10), pady=(30, 5), sticky="w")

        self.yarus_filepath_upload_input = customtkinter.CTkEntry(self.yarus_upload_frame, placeholder_text="Path:/to/dir",
                                                                  border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"),
                                                                  text_color=("#E2E2E2", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"))
        self.yarus_filepath_upload_input.grid(row=6, column=0, padx=(10, 0), pady=(0, 10), sticky="ew")

        self.yarus_filepath_upload_btn = customtkinter.CTkButton(self.yarus_upload_frame, text="Browse...", 
                                                                 fg_color="transparent", border_color=("#5C8779", "#0FC88A"), border_width=1,
                                                                 text_color=("#5C8779", "#E2E2E2"), hover_color=('#D8FFF2', "#044F36"),
                                                                 command=lambda: InterfaceMethodsYarus.select_directory_csv(self,'unloading'))
        self.yarus_filepath_upload_btn.grid(row=6, column=1, padx=(0, 10), pady=(0, 10), sticky="w")

        self.yarus_upload_btn = customtkinter.CTkButton(self.yarus_upload_frame, text="Выгрузить", 
                                                        text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C8779", "#008A5C"),
                                                        image=self.image_icon_upload, compound="right",
                                                        command=lambda: InterfaceMethodsYarus.unloading(self))
        self.yarus_upload_btn.grid(row=7, column=0, padx=(10, 10), pady=(30, 40), columnspan=2, sticky="ew")
        
        # =========================== ЖУРНАЛ ПРЕДЗАГРЗУКИ ===========================
        self.yarus_preload_label = customtkinter.CTkLabel(self.yarus_preload_frame, text="Предзагрузка данных:",
                                                          fg_color=("#E9F3F0", "#02271B"), corner_radius=0,
                                                          text_color=("#282828", "#e2e2e2"))
        self.yarus_preload_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")        

        self.yarus_preload_path_label = customtkinter.CTkLabel(self.yarus_preload_frame, text="Откуда брать:",
                                                               text_color=("#282828", "#e2e2e2"))
        self.yarus_preload_path_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        self.yarus_preload_path_input = customtkinter.CTkEntry(self.yarus_preload_frame, placeholder_text="Path:/to/dir",
                                                               border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"),
                                                               text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"))
        self.yarus_preload_path_input.grid(row=2, column=0, padx=(10, 0), pady=(10, 10), sticky="ew")

        self.yarus_filepath_preload_btn = customtkinter.CTkButton(self.yarus_preload_frame, text="Browse...", 
                                                                  fg_color="transparent", border_color=("#5C8779", "#0FC88A"), border_width=1,
                                                                  text_color=("#5C8779", "#E2E2E2"), hover_color=('#D8FFF2', "#044F36"),
                                                                  command=lambda: InterfaceMethodsYarus.select_directory_csv(self,'preload'))
        self.yarus_filepath_preload_btn.grid(row=2, column=1, padx=(0, 0), pady=(10, 10), sticky="w")

        self.yarus_preload_btn = customtkinter.CTkButton(self.yarus_preload_frame, text="Сформировать журнал", 
                                                         text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C8779", "#008A5C"),
                                                         image=self.image_icon_preload, compound="right",
                                                         command=lambda: InterfaceMethodsYarus.make_logfile_preload(self, self.yarus_preload_path_input.get(), 'yarus'))
        self.yarus_preload_btn.grid(row=3, column=0, padx=(10, 10), pady=(30, 40), columnspan=2, sticky="ew")

        # =========================== ЗАГРЗУКА ===========================
        self.yarus_onload_label = customtkinter.CTkLabel(self.yarus_onload_frame, text="Загрузка в базу",
                                                         fg_color=("#E9F3F0", "#02271B"), corner_radius=0,
                                                         text_color=("#282828", "#e2e2e2"))
        self.yarus_onload_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.yarus_onload_path_label = customtkinter.CTkLabel(self.yarus_onload_frame, text="Откуда загружать:",
                                                              text_color=("#282828", "#e2e2e2"))
        self.yarus_onload_path_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 10), sticky="w")

        self.yarus_onload_path_input = customtkinter.CTkEntry(self.yarus_onload_frame, placeholder_text="Path:/to/dir",
                                                              border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"),
                                                              text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"))
        self.yarus_onload_path_input.grid(row=2, column=0, padx=(10, 0), pady=(10, 10), sticky="ew")

        self.yarus_filepath_onload_btn = customtkinter.CTkButton(self.yarus_onload_frame, text="Browse...", fg_color="transparent",
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"),
                                                                 text_color=("#5C8779", "#E2E2E2"), hover_color=('#D8FFF2', "#044F36"),
                                                                 command=lambda: InterfaceMethodsYarus.select_directory_csv(self,'upload_datas'))
        self.yarus_filepath_onload_btn.grid(row=2, column=1, padx=(0, 0), pady=(10, 10), sticky="w")

        self.yarus_onload_btn = customtkinter.CTkButton(self.yarus_onload_frame, text="Загрузить", 
                                                        text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C8779", "#008A5C"),
                                                        image=self.image_icon_onload, compound="right",
                                                        command=lambda: InterfaceMethodsYarus.upload_to_db(self))
        self.yarus_onload_btn.grid(row=3, column=0, padx=(10, 10), pady=(30, 40), columnspan=2, sticky="ew")

        # =========================== УДАЛЕНИЕ ===========================
        self.yarus_delete_label = customtkinter.CTkLabel(self.yarus_delete_frame, text="Удаление из базы",
                                                         fg_color=("#E9F3F0", "#02271B"), corner_radius=0,
                                                         text_color=("#282828", "#e2e2e2"))
        self.yarus_delete_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.yarus_delete_label2 = customtkinter.CTkLabel(self.yarus_delete_frame, text="")
        self.yarus_delete_label2.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_ship_delete_label = customtkinter.CTkLabel(self.yarus_delete_frame, text="Введите позывной:",
                                                              text_color=("#282828", "#e2e2e2"))
        self.yarus_ship_delete_label.grid(row=2, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_ship_delete_input = customtkinter.CTkEntry(self.yarus_delete_frame, placeholder_text="ship",
                                                              text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                              border_color=("#5C8779", "#0FC88A"))
        self.yarus_ship_delete_input.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_reis_delete_label = customtkinter.CTkLabel(self.yarus_delete_frame, text="Введите № рейса:",
                                                              text_color=("#282828", "#e2e2e2"))
        self.yarus_reis_delete_label.grid(row=4, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_reis_delete_input = customtkinter.CTkEntry(self.yarus_delete_frame, placeholder_text="reis",
                                                              text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                              border_color=("#5C8779", "#0FC88A"))
        self.yarus_reis_delete_input.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_delete_btn = customtkinter.CTkButton(self.yarus_delete_frame, text="Удалить",
                                                        text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C8779", "#008A5C"),
                                                        image=self.image_icon_delete, compound="right",
                                                        command=lambda: InterfaceMethodsYarus.delete_reis(self))
        self.yarus_delete_btn.grid(row=6, column=0, padx=(10, 10), pady=(30, 40), columnspan=2, sticky="ew")

        # =========================== таб Корректировка признака 1 ===========================
        self.yarus_corrprizn_lable = customtkinter.CTkLabel(self.yarus_corrprizn_frame, text="Коректировка признака",
                                                            fg_color=("#E9F3F0", "#02271B"), corner_radius=0, text_color=("#282828", "#e2e2e2"))
        self.yarus_corrprizn_lable.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.yarus_corrprizn_title1_lable = customtkinter.CTkLabel(self.yarus_corrprizn_frame, text="Где меняем признак:",
                                                                   text_color=("#282828", "#ffffff"), fg_color=("#E9F3F0", "#02271B"))
        self.yarus_corrprizn_title1_lable.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrprizn_ship_lable = customtkinter.CTkLabel(self.yarus_corrprizn_frame, text="Введите позывной:",
                                                                 text_color=("#282828", "#e2e2e2"))
        self.yarus_corrprizn_ship_lable.grid(row=2, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrprizn_ship_input = customtkinter.CTkEntry(self.yarus_corrprizn_frame, placeholder_text="ship",
                                                                 text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrprizn_ship_input.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrprizn_reis_lable = customtkinter.CTkLabel(self.yarus_corrprizn_frame, text="Введите № рейса:", 
                                                                 text_color=("#282828", "#e2e2e2"))
        self.yarus_corrprizn_reis_lable.grid(row=4, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrprizn_reis_input = customtkinter.CTkEntry(self.yarus_corrprizn_frame, placeholder_text="reis", 
                                                                 text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrprizn_reis_input.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrprizn_title2_lable = customtkinter.CTkLabel(self.yarus_corrprizn_frame, text="Введите новые параметры, где:\n1 - совместный\n2 - из АтлантНИРО",
                                                                   justify="left", text_color=("#282828", "#ffffff"), fg_color=("#E9F3F0", "#02271B"))
        self.yarus_corrprizn_title2_lable.grid(row=6, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrprizn_przn_lable = customtkinter.CTkLabel(self.yarus_corrprizn_frame, text="Новый признак рейса:", 
                                                                 text_color=("#282828", "#e2e2e2"))
        self.yarus_corrprizn_przn_lable.grid(row=7, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrprizn_przn_input = customtkinter.CTkEntry(self.yarus_corrprizn_frame, placeholder_text="przn", 
                                                                 text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrprizn_przn_input.grid(row=8, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrprizn_operator_lable = customtkinter.CTkLabel(self.yarus_corrprizn_frame, text="Новый оператор:", 
                                                                     text_color=("#282828", "#e2e2e2"))
        self.yarus_corrprizn_operator_lable.grid(row=9, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrprizn_operator_input = customtkinter.CTkEntry(self.yarus_corrprizn_frame, placeholder_text="operator", 
                                                                     border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"),
                                                                     text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"))
        self.yarus_corrprizn_operator_input.grid(row=10, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrprizn_btn = customtkinter.CTkButton(self.yarus_corrprizn_frame, text="Применить", 
                                                           text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C8779", "#008A5C"),
                                                           command=lambda: InterfaceMethodsYarus.corr_prizn_reis(self))
        self.yarus_corrprizn_btn.grid(row=11, column=0, padx=(10, 10), pady=(40, 30), columnspan=2, sticky="ew")

        # =========================== таб Корректировка рейса 2 ===========================
        self.yarus_corrreis_lable = customtkinter.CTkLabel(self.yarus_corrreis_frame, text="Коректировка рейса",
                                                           fg_color=("#E9F3F0", "#02271B"), corner_radius=0, text_color=("#282828", "#e2e2e2"))
        self.yarus_corrreis_lable.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.yarus_corrreis_title1_lable = customtkinter.CTkLabel(self.yarus_corrreis_frame, text="Где меняем рейс:",
                                                                  fg_color=("#E9F3F0", "#02271B"), corner_radius=0, text_color=("#282828", "#e2e2e2"))
        self.yarus_corrreis_title1_lable.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrreis_oldship_lable = customtkinter.CTkLabel(self.yarus_corrreis_frame, text="Введите старый позывной:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.yarus_corrreis_oldship_lable.grid(row=2, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrreis_oldship_input = customtkinter.CTkEntry(self.yarus_corrreis_frame, placeholder_text="ship", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrreis_oldship_input.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrreis_oldreis_lable = customtkinter.CTkLabel(self.yarus_corrreis_frame, text="Введите старый № рейса:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.yarus_corrreis_oldreis_lable.grid(row=4, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrreis_oldreis_input = customtkinter.CTkEntry(self.yarus_corrreis_frame, placeholder_text="reis", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrreis_oldreis_input.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrreis_title2_lable = customtkinter.CTkLabel(self.yarus_corrreis_frame, text="Введите новые параметры:",
                                                                  fg_color=("#E9F3F0", "#02271B"), corner_radius=0, text_color=("#282828", "#e2e2e2"))
        self.yarus_corrreis_title2_lable.grid(row=6, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrreis_newship_lable = customtkinter.CTkLabel(self.yarus_corrreis_frame, text="Введите новый позывной:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.yarus_corrreis_newship_lable.grid(row=7, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrreis_newship_input = customtkinter.CTkEntry(self.yarus_corrreis_frame, placeholder_text="ship", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrreis_newship_input.grid(row=8, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrreis_newreis_lable = customtkinter.CTkLabel(self.yarus_corrreis_frame, text="Введите новый № рейса:", 
                                                                   text_color=("#282828", "#e2e2e2"))
        self.yarus_corrreis_newreis_lable.grid(row=9, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrreis_newreis_input = customtkinter.CTkEntry(self.yarus_corrreis_frame, placeholder_text="reis", 
                                                                   text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrreis_newreis_input.grid(row=10, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrreis_btn = customtkinter.CTkButton(self.yarus_corrreis_frame, text="Применить", 
                                                           text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C8779", "#008A5C"),
                                                           command=lambda: InterfaceMethodsYarus.corr_reis(self))
        self.yarus_corrreis_btn.grid(row=11, column=0, padx=(10, 10), pady=(40, 30), columnspan=2, sticky="ew")

        # =========================== таб Корректировка пробы 3 ===========================
        self.yarus_corrprob_label = customtkinter.CTkLabel(self.yarus_corrprob_frame, text="Коректировка пробы",
                                                           fg_color=("#E9F3F0", "#02271B"), corner_radius=0, text_color=("#282828", "#e2e2e2"))
        self.yarus_corrprob_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.yarus_corrprob_title1_label = customtkinter.CTkLabel(self.yarus_corrprob_frame, text="Параметры, где будем менять пробу:",
                                                                  fg_color=("#E9F3F0", "#02271B"), corner_radius=0, text_color=("#282828", "#e2e2e2"))
        self.yarus_corrprob_title1_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrprob_ship_input = customtkinter.CTkEntry(self.yarus_corrprob_frame, placeholder_text="Позывной", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrprob_ship_input.grid(row=2, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrprob_reis_input = customtkinter.CTkEntry(self.yarus_corrprob_frame, placeholder_text="№ рейса", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrprob_reis_input.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrprob_trl_input = customtkinter.CTkEntry(self.yarus_corrprob_frame, placeholder_text="Тралы (через запятую)", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrprob_trl_input.grid(row=4, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrprob_kodvid_input = customtkinter.CTkEntry(self.yarus_corrprob_frame, placeholder_text="Код объекта", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrprob_kodvid_input.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrprob_bioinfo_input = customtkinter.CTkEntry(self.yarus_corrprob_frame, placeholder_text="bio_info", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrprob_bioinfo_input.grid(row=6, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrprob_ukey_input = customtkinter.CTkEntry(self.yarus_corrprob_frame, placeholder_text="u_key", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrprob_ukey_input.grid(row=7, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrprob_title2_label = customtkinter.CTkLabel(self.yarus_corrprob_frame, text="Новая проба:",
                                                                  fg_color=("#E9F3F0", "#02271B"), corner_radius=0, text_color=("#282828", "#e2e2e2"))
        self.yarus_corrprob_title2_label.grid(row=8, column=0, padx=(10, 10), pady=(10, 5), sticky="w")   

        self.yarus_corrprob_proba_input = customtkinter.CTkEntry(self.yarus_corrprob_frame, placeholder_text="Новая проба", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrprob_proba_input.grid(row=9, column=0, padx=(10, 10), pady=(0, 10), sticky="ew") 

        self.yarus_corrprob_btn = customtkinter.CTkButton(self.yarus_corrprob_frame, text="Применить", 
                                                           text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C8779", "#008A5C"),
                                                           command=lambda: InterfaceMethodsYarus.corr_prob(self))
        self.yarus_corrprob_btn.grid(row=10, column=0, padx=(10, 10), pady=(40, 30), columnspan=2, sticky="ew")

        # =========================== таб Корректировка возраста 4 ===========================
        self.yarus_corrvozr_label = customtkinter.CTkLabel(self.yarus_corrvozr_frame, text="Коректировка возраста",
                                                           fg_color=("#E9F3F0", "#02271B"), corner_radius=0, text_color=("#282828", "#e2e2e2"))
        self.yarus_corrvozr_label.grid(row=0, column=0, padx=(1, 2), pady=(10, 10), columnspan=2, sticky="ew")

        self.yarus_corrvozr_title1_label = customtkinter.CTkLabel(self.yarus_corrvozr_frame, text="Введите параметры для выборки:",
                                                                     fg_color=("#E9F3F0", "#02271B"),
                                                                     text_color=("#282828", "#e2e2e2"))
        self.yarus_corrvozr_title1_label.grid(row=1, column=0, padx=(10, 10), pady=(10, 5), sticky="w")

        self.yarus_corrvozr_ship_input = customtkinter.CTkEntry(self.yarus_corrvozr_frame, placeholder_text="Позывной", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrvozr_ship_input.grid(row=2, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrvozr_reis_input = customtkinter.CTkEntry(self.yarus_corrvozr_frame, placeholder_text="№ рейса", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrvozr_reis_input.grid(row=3, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrvozr_trl_input = customtkinter.CTkEntry(self.yarus_corrvozr_frame, placeholder_text="Трал (один)", 
                                                               text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrvozr_trl_input.grid(row=4, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrvozr_kodvid_input = customtkinter.CTkEntry(self.yarus_corrvozr_frame, placeholder_text="Код объекта", 
                                                                  text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrvozr_kodvid_input.grid(row=5, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrvozr_bioinfo_input = customtkinter.CTkEntry(self.yarus_corrvozr_frame, placeholder_text="bio_info", 
                                                                   text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrvozr_bioinfo_input.grid(row=6, column=0, padx=(10, 10), pady=(0, 10), sticky="ew")

        self.yarus_corrvozr_ukey_input = customtkinter.CTkEntry(self.yarus_corrvozr_frame, placeholder_text="u_key", 
                                                                text_color=("#5C6987", "#FFFFFF"), fg_color=("#F9FFFD", "#02271B"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"))
        self.yarus_corrvozr_ukey_input.grid(row=7, column=0, padx=(10, 10), pady=(0, 10), sticky="ew") 

        self.yarus_corrvozr_select_btn = customtkinter.CTkButton(self.yarus_corrvozr_frame, text="Выбрать", 
                                                                 text_color=("#5C8779", "#E2E2E2"), fg_color=("#F9FFFD", "#044F36"),hover_color=('#D8FFF2', "#5C8779"),
                                                                 border_width=1, corner_radius=5, border_color=("#5C8779", "#0FC88A"),
                                                                 command=lambda: InterfaceMethodsYarus.selection_data(self, self.yarus_corrvozr_ship_input.get().upper(), self.yarus_corrvozr_reis_input.get(),
                                                                                                                        self.yarus_corrvozr_trl_input.get(), self.yarus_corrvozr_kodvid_input.get(),
                                                                                                                        self.yarus_corrvozr_bioinfo_input.get(), self.yarus_corrvozr_ukey_input.get()))
        self.yarus_corrvozr_select_btn.grid(row=8, column=0, padx=(10, 10), pady=(10, 30), columnspan=1, sticky="ew")

        dict_test_y = {'A': [1, 2, 3], 'B': [1, 2, 3]}
        df_y = pd.DataFrame(dict_test_y)

        data_y = [[j for j in i[1:]] for i in df_y.itertuples()]
        header_y = ['bikl', 'ship','reis','trl','kodvid','n_fish','bio_info','u_key','vozr1','vozr2','l_big','l_lit','n_ring']
        self.sheet_y = Sheet(self.yarus_corrvozr_frame,
                           data = data_y,
                           header=header_y,
                           theme = "dark",
                           width=650)
        self.sheet_y.enable_bindings("all", "edit_header", "edit_index")
        self.sheet_y.set_all_cell_sizes_to_text()
        self.sheet_y.grid(row=9, column=0, padx=(10, 10), pady=(10, 30), sticky = "nswe")

        self.yarus_corrvozr_btn = customtkinter.CTkButton(self.yarus_corrvozr_frame, text="Скорректировать", 
                                                          text_color=("#FFFFFF", "#E2E2E2"), fg_color=("#5C8779", "#008A5C"),
                                                          command=lambda: InterfaceMethodsYarus.update_age(self))
        self.yarus_corrvozr_btn.grid(row=10, column=0, padx=(10, 10), pady=(10, 30), columnspan=2, sticky="ew")



        # select default frame
        self.select_frame_by_name("home")


    def select_frame_by_name(self, name):
        # set button color for selected button
        self.home_button.configure(fg_color=("gray75", "gray25") if name == "home" else "transparent")
        self.frame_2_button.configure(fg_color=("gray75", "gray25") if name == "frame_2" else "transparent")
        self.frame_3_button.configure(fg_color=("gray75", "gray25") if name == "frame_3" else "transparent")

        # show selected frame
        if name == "home":
            self.general_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.general_frame.grid_forget()

        if name == "frame_2":
            self.second_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.second_frame.grid_forget()
            
        if name == "frame_3":
            self.third_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.third_frame.grid_forget()

    def home_button_event(self):
        self.select_frame_by_name("home")

    def frame_2_button_event(self):
        self.select_frame_by_name("frame_2")

    def frame_3_button_event(self):
        self.select_frame_by_name("frame_3")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)


# self.file_to_delete_general
    def on_closing(self):
        """
        функция отрабаыватет при закрытии приложения.
        удаляет (если существует) папку fixed_csv во временных файлах
        """
        # shutil.rmtree(self.path_csv_path)
        # self.destroy()
        temp_path_g = 'C:\\temp\general\\fixed_csv'
        temp_path_y = 'C:\\temp\yarus\\fixed_csv'
        if os.path.exists(temp_path_g):
            shutil.rmtree(temp_path_g)

        if os.path.exists(temp_path_y):
            shutil.rmtree(temp_path_y)
        
        self.destroy()

        # try:
        #     try:
        #         try:
        #             if os.path.exists(temp_path_g):
        #                 # print(f'yos: {os.join(self.path_entry, 'fixed_csv')}')
        #                 # print(os.join(self.path_entry))
        #                 # print(self.path_csv_path)
        #                 shutil.rmtree(temp_path_g)

        #         except AttributeError:
        #             if os.path.exists(temp_path_y):
        #                 print(temp_path_y)
        #                 # print(os.join(self.path_csv_path_y))
        #                 shutil.rmtree(temp_path_y)
        #     except:
        #         try:
        #             if os.path.exists(temp_path_y):
        #                 print(temp_path_y)
        #                 # print(os.join(self.path_csv_path_y))
        #                 shutil.rmtree(temp_path_y)

        #         except AttributeError:
        #             if os.path.exists(temp_path_g):
        #                 # print(self.path_csv_path)
        #                 # print(f'yos: {os.join(self.path_entry, 'fixed_csv')}')
        #                 # print(os.join(self.path_entry))
        #                 shutil.rmtree(temp_path_g)
            # self.destroy()
        # except:
        #     self.destroy()


if __name__ == "__main__":
    app = App()
    app.mainloop()


    

