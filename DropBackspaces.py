import pandas as pd
import chardet
import os, shutil
import tempfile
from tkinter.messagebox import showinfo


class DropBackspaces:

    def drop_backspaces(self, folder_path, base):
        """
        убирает лишние пробелы в столбцах с данными в таблицах и добавляет шапочку сверху, чтобы понимать, что за поля а таблицах.
        """
        if base == 'general':
            temp_path = 'C:\\temp\general'
        else:
            temp_path = 'C:\\temp\yarus'
        # print(folder_path)

        def remove_fixed_csv_directory(directory):
            """
            проверяет наличие папки fixed_csv, куда выгружаются файлики после обработки.
            если папка уже есть - удаляет ее и все ее содержимое, затем пересоздает заново.
            """
            fixed_csv_path = os.path.join(directory, "fixed_csv")
            if os.path.exists(fixed_csv_path):
                shutil.rmtree(fixed_csv_path)
                print(f"Папка 'fixed_csv' и ее содержимое успешно удалены.")
            else:
                print(f"Папка 'fixed_csv' не найдена.")

        # Удаление папки 'fixed_csv' перед запуском программы
        remove_fixed_csv_directory(temp_path)

        files = os.listdir(folder_path)  # Получаем список файлов в папке

        df_dict = {}

        file_dict = {
            'general': {
                'tral.csv': {
                    'header': ['ship','reis','data','trl',
                            'prom_kv','rloc','rzon','rikes',
                            'rnorv','shir','dolg','v_wind',
                            'f_wind','volna','oblaco','glub',
                            'grunt','t_pov','t_dno','t_air',
                            'nach','prod','orlov','vidlov',
                            'kutok','rub','g_rask','v_rask',
                            'wire','gor','speed','kurs',
                            'ulov','uchet','avar','sel_r',
                            'tral_info','info','dist',
                            'kollov', 'commenttr', 'maincomm'
                            ]
                },

                'ulov.csv': {
                    'header': ['ship','reis','trl','u_key',
                            'kodvid','u_wes','u_mech','u_fix',
                            'u_num','u_prc','promer','step'
                            ]
                },

                'biopap.csv': {
                    'header': ['ship','reis','trl','kodvid',
                            'n_fish','l_big','l_lit','wes_ob',
                            'wes_bv','pol','zrel','puzo',
                            'salo','w_pech','w_gonad','proba',
                            'w_food','n_ring','age_ring','type_lbig',
                            'type_llit','vozr1','vozr2','menu_kap',
                            'u_key','bio_info','skap_info'
                            ]
                },

                'biokap.csv': {
                    'header': ['ship','reis','trl','kodvid',
                            'n_fish','bio_info','u_key','kodpit',
                            'st_per','l_pit','n_pit','w_pit',
                            'prpit','info_pit','info_rz','voz_pit',
                            'vos_wes','sred_ulov','devstage'
                            ]
                },

                'razm.csv': {
                    'header': ['ship','reis','trl','kodvid',
                            'pol','tip_dl','lnf','kolf',
                            'u_key','step'
                            ]
                },

                'biopit.csv': {
                    'header': ['ship','reis','trl','kodvid',
                            'n_fish','bio_info','u_key','kodpit',
                            'st_per','prpit'
                            ]
                },

                'pandalus.csv': {
                    'header': ['ship','reis','trl','u_key',
                            'kodvid','n_fish','carapace','sex',
                            'stgonad','stlink'
                            ]
                },

                'crabs.csv': {
                    'header': ['ship','reis','trl','u_key',
                            'kodvid','n_krab','shirina','dlina',
                            'dlina_nr','dlina_rs','pol','linka',
                            'wes_ob','zrel_ikra','wes_ikra','diam_ikr',
                            'color_ikra','avr_nav','area_ulc','acquire',
                            'wes_eda','napoln','condil1','kol_cl1',
                            'condil2','kol_cl2','condil3','kol_cl3',
                            'condil4','kol_cl4','condil5','kol_cl5',
                            'condir1','kol_cr1','condir2','kol_cr2',
                            'condir3','kol_cr3','condir4','kol_cr4',
                            'condir5','kol_cr5','commenb'
                            ]
                },

                'morph.csv': {
                    'header': ['ship','reis','trl','u_key',
                            'kodvid','n_krab','chela_w','chela_l',
                            'chela_h','mwl2_w','mwl2_l','mwl2_h',
                            'mwl3_w','mwl3_l','mwl3_h','mwl4_w',
                            'mwl4_l','mwl4_h','orbit_w','rostrm_w',
                            'abdom5_w'
                            ]
                },

                'acq.csv': {
                    'header': ['ship','reis','trl','u_key',
                            'kodvid','n_krab','object0','kol',
                            'kolleg'
                            ]
                },

                'trallist.csv': {
                    'header': ['ship','reis','trl1','trl2',
                            'data1','data2','ntral','nrazm',
                            'nbiopap','nbiopit','nulov','nbiokap',
                            'npandalus','ncrabs','nmorph','nacq',
                            'ins_date', 'act_date', 'bort', 'priznrs', 'operator'
                            ]
                }
            },

            'yarus': {
                'y_tral.csv': {
                    'header': [
                        'ship','reis','trl','data','stop_in','stop_ine','shir_beg','dolg_beg','glub','shir_end',
                        'dolg_end','glub_end','kas_put','hook_put','len_yr','speed','kurs','data2','stop_outb','stop_out',
                        'kas_up','hook_up','speed_up','kurs_up','prom_kv','prom_kvup','rloc','rzon','rikes','rnorv','v_wind',
                        'f_wind','volna','oblaco','t_air','t_pov','t_dno','s_dno', 'vt_dno','ft_dno','grunt','yrtype','orlov',
                        'xreb','hook_type','hook_prc','bait1','baitprc1','bait2','baitprc2','bait3','baitprc3','ulov','avar'
                        ]
                },

                'y_ulov.csv': {
                    'header': [
                        'ship','reis','trl','u_key','kodvid','u_wes','u_mech','u_fix','u_num','u_prc','promer','step'
                        ]
                },

                'y_biopap.csv': {
                    'header': [
                        'ship','reis','trl','kodvid','n_fish','l_big','l_lit','wes_ob','wes_bv','pol','zrel','puzo','salo','w_pech',
                        'w_gonad','proba','w_food','n_ring','age_ring','type_lbig','type_llit','vozr1','vozr2','menu_kap','u_key','bio_info','skap_info'
                        ]
                },

                'y_biokap.csv': {
                    'header': ['ship','reis','trl','kodvid',
                            'n_fish','bio_info','u_key','kodpit',
                            'st_per','l_pit','n_pit','w_pit',
                            'prpit','info_pit','info_rz','voz_pit',
                            'vos_wes','sred_ulov','devstage'
                            ]
                },            

                'y_razm.csv': {
                    'header': [
                        'ship','reis','trl','kodvid','pol','tip_dl','lnf','kolf','u_key','step'
                        ]
                },

                'y_biopit.csv': {
                    'header': [
                        'ship','reis','trl','kodvid','n_fish','bio_info','u_key','kodpit','st_per','prpit'
                        ]
                },

                'y_trallist.csv': {
                    'header': [
                        'ship','reis','trl1','trl2',
                        'data1','data2','ntral','nrazm',
                        'nbiopap','nbiopit','nulov','nbiokap',
                        'npandalus','ncrabs','nmorph','nacq',
                        'ins_date', 'act_date', 'bort', 'priznrs', 'operator'
                        ]
                }                
            }
        }

             # Функция для удаления пробелов из значения
        
        def remove_spaces(value):
            """
            непосредственно сама функция чиканья лишних пробелов.
            """
            if isinstance(value, str):
                return value.strip()
            return value
        
        # print(file_dict.get(base))
        
        # шагаем по файлам, перебирая и обрабатывая каждый
        for file_name in files:
            file_path = os.path.join(folder_path, file_name)  # Полный путь к файлу
            #D:/bio/Yarus/prefix\Y_Biokap.csv
            # print(os.path.isdir(file_path))
            # files = [i.lower() for i in file_dict.get(base)]
            # print(a)
            if not os.path.isfile(file_path):
                # print(os.path.isfile(file_path))
                continue
            if not file_name.lower() in file_dict.get(base):
                continue

            # print('====')
            # print(file_path)


            for key, values in file_dict.get(base).items():
                # print(key)
                header_list = file_dict.get(base)[os.path.basename(file_path).lower()].get('header')
                # print(header_list)

                if os.path.isfile(file_path):  # Проверяем, является ли путь файлом
                    with open(file_path, 'rb') as fp:
                        lines = fp.readlines()

            # Создаем временный файл
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                # Записываем содержимое файла во временный файл
                temp_file.writelines([line for line in lines])
                # Получаем путь к временному файлу
                temp_file_path = temp_file.name

# делаем шапочку сверху в каждом файлике
            with open(temp_file_path, 'r') as tf:
                t_lines = tf.readlines()
                if t_lines:
                    has_header = t_lines[0].strip() == '|'.join(header_list)
                else:
                    has_header = False

                if not has_header:  # Если шапки нет, то добавляем её
                    t_lines.insert(0, '|'.join(header_list) + '\n')

            with open(temp_file_path, 'w') as tf:
                tf.writelines(t_lines)

            # Теперь работаем над чиканьем
            with open(temp_file_path, 'rb') as tf:
                result = chardet.detect(tf.read())
                

            # df = pd.read_csv(temp_file_path, encoding=result, sep='|')
            df = pd.read_csv(temp_file_path, encoding='ANSI', sep='|')
            # print(df)

            exclude_column = 'u_key'

            if exclude_column in df.columns:
                for column in df.columns:
                    if column != exclude_column and column != 'info_rz':
                        df[column] = df[column].apply(lambda x: remove_spaces(x)) 
            else:
                df = df.applymap(lambda x: remove_spaces(x))

            date_col = ('data', 'data1', 'data2')

            for col in date_col:
                # print(col)
                if col == 'data':
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], format='%d/%m/%Y')
                        df[col] = df[col].dt.strftime('%Y-%m-%d')

                # else:
                #     df['data2'] = pd.to_datetime(df['data2'], format='%d/%m/%Y')
                #     df['data2'] = df['data2'].dt.strftime('%Y-%m-%d')
                #     print(df['data2'] )

            # print(os.path.splitext(file_name)[0].lower())
            if os.path.splitext(file_name)[0].lower() == 'y_tral':
                df['data2'] = pd.to_datetime(df['data2'], format='%d/%m/%Y')
                df['data2'] = df['data2'].dt.strftime('%Y-%m-%d')

            if os.path.splitext(file_name)[0].lower() == 'trallist' or os.path.splitext(file_name)[0].lower() == 'y_trallist':
                df = df[['ship','reis','trl1','trl2','data1','data2','ntral','nulov','nbiopap','nbiopit','nrazm','nbiokap',
                         'ins_date','act_date','bort','priznrs','operator','npandalus','ncrabs','nmorph','nacq']]
                
                df['data1'] = pd.to_datetime(df['data1'], format='%d/%m/%Y')
                df['data1'] = df['data1'].dt.strftime('%Y-%m-%d')
                df['data2'] = pd.to_datetime(df['data2'], format='%d/%m/%Y')
                df['data2'] = df['data2'].dt.strftime('%Y-%m-%d')


            df_dict[f"{os.path.splitext(file_name)[0]}.csv"] = df

            os.remove(temp_file_path)

        def check_and_create_directory(directory):
            if not os.path.exists(directory):
                os.makedirs(directory)
                print(f"Директория {directory} создана.")
            else:
                print(f"Директория {directory} уже существует.")

        # Проверка и создание директории 'fixed_csv' в текущем каталоге
        def convert_and_move_dataframes(dataframe_dict, destination_directory):
            for df_name, df in dataframe_dict.items():
                # Преобразование датафрейма в CSV
                csv_file_path = os.path.join(destination_directory, f"{df_name}")
                df.to_csv(csv_file_path, encoding='ANSI', sep='|', index=False)
                print(f"Датафрейм '{df_name}' экспортирован в CSV как '{csv_file_path}' и перемещен в директорию fixed_csv'.\n")

        directory_name = temp_path + r'\fixed_csv'
        check_and_create_directory(directory_name)

        # Конвертирование и перемещение датафреймов в директорию 'fixed_csv'
        convert_and_move_dataframes(df_dict, directory_name)

        # showinfo(title="Информация", message=f"Пробелы удалены! Файлы находятся в папке {temp_path}/fixed_csv")

