import pandas as pd
import os
import tempfile
import chardet

class CSVProcessing:

    # Функция для удаления пробелов из значения
    def remove_spaces(value):
        if isinstance(value, str):
            return value.strip()
        return value
    
    def csv_read_and_processing(self, folder_path):
        df_dict = {}

        file_dict = {
            'Tral.csv': {
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

            'Ulov.csv': {
                'header': ['ship','reis','trl','u_key',
                        'kodvid','u_wes','u_mech','u_fix',
                        'u_num','u_prc','promer','step'
                        ]
            },

            'Biopap.csv': {
                'header': ['ship','reis','trl','kodvid',
                        'n_fish','l_big','l_lit','wes_ob',
                        'wes_bv','pol','zrel','puzo',
                        'salo','w_pech','w_gonad','proba',
                        'w_food','n_ring','age_ring','type_lbig',
                        'type_llit','vozr1','vozr2','menu_kap',
                        'u_key','bio_info','skap_info'
                        ]
            },

            'Biokap.csv': {
                'header': ['ship','reis','trl','kodvid',
                        'n_fish','bio_info','u_key','kodpit',
                        'st_per','l_pit','n_pit','w_pit',
                        'prpit','info_pit','info_rz','voz_pit',
                        'vos_wes','sred_ulov','devstage'
                        ]
            },

            'Razm.csv': {
                'header': ['ship','reis','trl','kodvid',
                        'pol','tip_dl','lnf','kolf',
                        'u_key','step'
                        ]
            },

            'Biopit.csv': {
                'header': ['ship','reis','trl','kodvid',
                        'n_fish','bio_info','u_key','kodpit',
                        'st_per','prpit'
                        ]
            },

            'Pandalus.csv': {
                'header': ['ship','reis','trl','u_key',
                        'kodvid','n_fish','carapace','sex',
                        'stgonad','stlink'
                        ]
            },

            'Crabs.csv': {
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

            'Morph.csv': {
                'header': ['ship','reis','trl','u_key',
                        'kodvid','n_krab','chela_w','chela_l',
                        'chela_h','mwl2_w','mwl2_l','mwl2_h',
                        'mwl3_w','mwl3_l','mwl3_h','mwl4_w',
                        'mwl4_l','mwl4_h','orbit_w','rostrm_w',
                        'abdom5_w'
                        ]
            },

            'Acq.csv': {
                'header': ['ship','reis','trl','u_key',
                        'kodvid','n_krab','object0','kol',
                        'kolleg'
                        ]
            },

            'TralList.csv': {
                'header': ['ship','reis','trl1','trl2',
                        'data1','data2','ntral','nrazm',
                        'nbiopap','nbiopit','nulov','nbiokap',
                        'npandalus','ncrabs','nmorph','nacq',
                        ]
            }, 
        }

        file_path = folder_path # Полный путь к файлу
        
        for key, values in file_dict.items():
            header_list = file_dict[file_path.split('/')[3]].get('header')

            # сначала я хочу вставить шапки, тут их нет в файликах
            if os.path.isfile(file_path):  # Проверяем, является ли путь файлом
                # Открываем CSV-файл для чтения
                with open(file_path, 'rb') as f:
                    lines = f.readlines() # Читаем содержимое файла

        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.writelines([line for line in lines])
            temp_file_path = temp_file.name

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

        df = pd.read_csv(temp_file_path, encoding='ANSI', sep='|')

        exclude_column = 'u_key'

        if exclude_column in df.columns:
            for column in df.columns:
                if column != exclude_column and column != 'info_rz':
                    df[column] = df[column].apply(lambda x: CSVProcessing.remove_spaces(x))

        else:
            df = df.applymap(lambda x: CSVProcessing.remove_spaces(x))

        os.remove(temp_file_path)

        self.table_show.model.df = df
        self.table_show.redraw()

