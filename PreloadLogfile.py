from Database import Database, UploadDatas
from tkinter.messagebox import showinfo
import os
import psycopg2
import pandas as pd
from tabulate import tabulate
import re


class PreloadLogfile:

    def make_logfile_preload(self, folder_path, base):
        if base == 'general':
            temp_path = 'C:\\temp\general'
        else:
            temp_path = 'C:\\temp\yarus'

        folder_path_new = temp_path + '\\fixed_csv'
        files = os.listdir(folder_path_new)
        
        pattern = re.compile(r'TralList')
        trallist_file = [file for file in files if pattern.search(file)]
        # print(trallist_file)

        connection = Database.connect_db(self)
        cursor = connection.cursor()

        tral_df = pd.read_csv(os.path.join(folder_path_new, trallist_file[0]), sep='|')
        ship_reis = tral_df.groupby(['ship','reis']).size().reset_index().rename(columns={0: 'count'})

        for index, row in ship_reis.iterrows():
            ship_value = row['ship']
            reis_value = row['reis']

        query_dict = {
            'general': {
                'first_query' : """
                    set datestyle to DMY;

                    ALTER TABLE temp_biokap DISABLE TRIGGER ALL;
                    ALTER TABLE temp_biopit DISABLE TRIGGER ALL;
                    ALTER TABLE temp_pandalus DISABLE TRIGGER ALL;
                    ALTER TABLE temp_biopap DISABLE TRIGGER ALL;
                    ALTER TABLE temp_razm DISABLE TRIGGER ALL;
                    ALTER TABLE temp_ulov DISABLE TRIGGER ALL;
                    ALTER TABLE temp_tral DISABLE TRIGGER ALL;
                    ALTER TABLE temp_crabs DISABLE TRIGGER ALL;
                    ALTER TABLE temp_morph DISABLE TRIGGER ALL;
                    ALTER TABLE temp_acq DISABLE TRIGGER ALL;

                    truncate temp_biokap;
                    truncate temp_biopit;
                    truncate temp_pandalus;
                    truncate temp_biopap;
                    truncate temp_razm;
                    truncate temp_ulov;
                    truncate temp_tral;
                    truncate temp_crabs;
                    truncate temp_morph;
                    truncate temp_acq;

                    ALTER TABLE temp_biokap ENABLE TRIGGER ALL;
                    ALTER TABLE temp_biopit ENABLE TRIGGER ALL;
                    ALTER TABLE temp_pandalus ENABLE TRIGGER ALL;
                    ALTER TABLE temp_biopap ENABLE TRIGGER ALL;
                    ALTER TABLE temp_razm ENABLE TRIGGER ALL;
                    ALTER TABLE temp_ulov ENABLE TRIGGER ALL;
                    ALTER TABLE temp_tral ENABLE TRIGGER ALL;
                    ALTER TABLE temp_crabs ENABLE TRIGGER ALL;
                    ALTER TABLE temp_morph ENABLE TRIGGER ALL;
                    ALTER TABLE temp_acq ENABLE TRIGGER ALL;
                    """,

                'copy_queries': {
                    'biokap': """
                        COPY temp_biokap (ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,st_per,l_pit,n_pit,w_pit,
                        prpit,info_pit,info_rz,voz_pit,vos_wes,sred_ulov,devstage)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,

                    'pandalus': """
                        COPY temp_pandalus (ship,reis,trl,u_key,kodvid,n_fish,carapace,sex,stgonad,stlink)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,

                    'biopit': """
                        COPY temp_biopit (ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,st_per,prpit)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,

                    'biopap': """
                        COPY temp_biopap (ship,reis,trl,kodvid,n_fish,l_big,l_lit,wes_ob,wes_bv,pol,zrel,puzo,salo,
                        w_pech,w_gonad,proba,w_food,n_ring,age_ring,type_lbig,type_llit,vozr1,vozr2,menu_kap,u_key,bio_info,skap_info)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,

                    'razm': """
                        COPY temp_razm (ship,reis,trl,kodvid,pol,tip_dl,lnf,kolf,u_key,step)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,

                    'ulov': """
                        COPY temp_ulov (ship,reis,trl,u_key,kodvid,u_wes,u_mech,u_fix,u_num,u_prc,promer,step)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,

                    'tral': """
                        COPY temp_tral (ship,reis,data,trl,prom_kv,rloc,rzon,rikes,rnorv,shir,dolg,v_wind,f_wind,volna,oblaco,glub,grunt,
                        t_pov,t_dno,t_air,nach,prod,orlov,vidlov,kutok,rub,g_rask,v_rask,wire,gor,speed,kurs,ulov,uchet,avar,sel_r,tral_info,
                        info,dist,kollov,commenttr,maincomm)
                        FROM STDIN DELIMITER '|' CSV HEADER
                    """,

                    'crabs': """
                        COPY temp_crabs (ship,reis,trl,u_key,kodvid,n_krab,shirina,dlina,dlina_nr,dlina_rs,pol,linka,wes_ob,zrel_ikra,wes_ikra,
                        diam_ikr,color_ikra,avr_nav,area_ulc,acquire,wes_eda,napoln,condil1,kol_cl1,condil2,kol_cl2,condil3,kol_cl3,condil4,kol_cl4,
                        condil5,kol_cl5,condir1,kol_cr1,condir2,kol_cr2,condir3,kol_cr3,condir4,kol_cr4,condir5,kol_cr5,commenb)
                        FROM STDIN DELIMITER '|' CSV HEADER
                    """,

                    'acq': """
                        COPY temp_acq (ship,reis,trl,u_key,kodvid,n_krab,object0,kol,kolleg)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,

                    'morph': """
                        COPY temp_morph (ship,reis,trl,u_key,kodvid,n_krab,chela_w,chela_l,chela_h,mwl2_w,mwl2_l,mwl2_h,mwl3_w,mwl3_l,mwl3_h,
                        mwl4_w,mwl4_l,mwl4_h,orbit_w,rostrm_w,abdom5_w)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,
                },

                'temp_queries' : {
                    'BIOKAP': {
                        'temp_qur' : f"SELECT * FROM temp_biokap WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,
                        st_per,l_pit,n_pit,w_pit,prpit,info_pit,info_rz,voz_pit,vos_wes,sred_ulov,devstage
                        FROM biokap WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','kodvid','n_fish','bio_info','u_key','kodpit','st_per',
                                    'l_pit','n_pit','w_pit','prpit','info_pit','info_rz','voz_pit','vos_wes',
                                    'sred_ulov','devstage'],

                        'order_by' : "ORDER BY ship,reis,trl,kodvid,n_fish;"
                    },

                    'PANDALUS': {
                        'temp_qur' : f"SELECT * FROM temp_pandalus WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,u_key,kodvid,n_fish,carapace,sex,stgonad,stlink
                        FROM pandalus WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','u_key','kodvid','n_fish','carapace','sex','stgonad','stlink'],

                        'order_by' : "ORDER BY ship,reis,trl,u_key,kodvid,n_fish;"
                    },

                    'BIOPIT': {
                        'temp_qur' : f"SELECT * FROM temp_biopit WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,st_per,prpit
                        FROM biopit WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','kodvid','n_fish','bio_info','u_key','kodpit','st_per','prpit'],

                        'order_by' : "ORDER BY ship,reis,trl,kodvid,n_fish;"                
                    },

                    'BIOPAP': {
                        'temp_qur' : f"SELECT * FROM temp_biopap WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,kodvid,n_fish,l_big,l_lit,wes_ob,wes_bv,pol,zrel,puzo,salo,w_pech,
                        w_gonad,proba,w_food,n_ring,age_ring,type_lbig,type_llit,vozr1,vozr2,menu_kap,u_key,bio_info,skap_info
                        FROM biopap WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','kodvid','n_fish','l_big','l_lit','wes_ob','wes_bv','pol','zrel','puzo','salo','w_pech',
                                    'w_gonad','proba','w_food','n_ring','age_ring','type_lbig','type_llit','vozr1','vozr2','menu_kap','u_key','bio_info','skap_info'],

                        'order_by' : "ORDER BY ship,reis,trl,kodvid,n_fish;"
                    },

                    'RAZM': {
                        'temp_qur' : f"SELECT * FROM temp_razm WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,kodvid,pol,tip_dl,lnf,kolf,u_key,step
                        FROM razm WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','kodvid','pol','tip_dl','lnf','kolf','u_key','step'],

                        'order_by' : "ORDER BY ship,reis,trl,kodvid;"
                    },

                    'ULOV': {
                        'temp_qur' : f"SELECT * FROM temp_ulov WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,u_key,kodvid,u_wes,u_mech,u_fix,u_num,u_prc,promer,step
                        FROM ulov WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','u_key','kodvid','u_wes','u_mech','u_fix','u_num','u_prc','promer','step'],

                        'order_by' : "ORDER BY ship,reis,trl,kodvid;"
                    },

                    'CRABS': {
                        'temp_qur' : f"SELECT * FROM temp_crabs WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,u_key,kodvid,n_krab,shirina,dlina,dlina_nr,dlina_rs,pol,
                        linka,wes_ob,zrel_ikra,wes_ikra,diam_ikr,color_ikra,avr_nav,area_ulc,acquire,wes_eda,napoln,condil1,
                        kol_cl1,condil2,kol_cl2,condil3,kol_cl3,condil4,kol_cl4,condil5,kol_cl5,condir1,kol_cr1,condir2,kol_cr2,
                        condir3,kol_cr3,condir4,kol_cr4,condir5,kol_cr5,commenb 
                        FROM crabs WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','u_key','kodvid','n_krab','shirina','dlina','dlina_nr','dlina_rs','pol','linka','wes_ob',
                                    'zrel_ikra','wes_ikra','diam_ikr','color_ikra','avr_nav','area_ulc','acquire','wes_eda','napoln','condil1',
                                    'kol_cl1','condil2','kol_cl2','condil3','kol_cl3','condil4','kol_cl4','condil5','kol_cl5','condir1','kol_cr1',
                                    'condir2','kol_cr2','condir3','kol_cr3','condir4','kol_cr4','condir5','kol_cr5','commenb'],
                        
                        'order_by' : "ORDER BY ship,reis,trl,kodvid;"
                    },

                    'ACQ': {
                        'temp_qur' : f"SELECT * FROM temp_acq WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,u_key,kodvid,n_krab,object0,kol,kolleg
                        FROM acq WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','u_key','kodvid','n_krab','object0','kol','kolleg'],
                        
                        'order_by' : "ORDER BY ship,reis,trl,kodvid,n_krab;"
                    },

                    'MORPH': {
                        'temp_qur' : f"SELECT * FROM temp_morph WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,u_key,kodvid,n_krab,chela_w,chela_l,chela_h,mwl2_w,mwl2_l,mwl2_h,
                        mwl3_w,mwl3_l,mwl3_h,mwl4_w,mwl4_l,mwl4_h,orbit_w,rostrm_w,abdom5_w
                        FROM morph WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','u_key','kodvid','n_krab','chela_w','chela_l','chela_h','mwl2_w',
                                    'mwl2_l','mwl2_h','mwl3_w','mwl3_l','mwl3_h','mwl4_w','mwl4_l','mwl4_h','orbit_w','rostrm_w','abdom5_w'],
                        
                        'order_by' : "ORDER BY ship,reis,trl,kodvid,n_krab;"                
                    },

                    'TRAL': {
                        'temp_qur' : f"SELECT * FROM temp_tral WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,data,trl,prom_kv,rloc,rzon,rikes,rnorv,shir,dolg,v_wind,f_wind,volna,oblaco,glub,
                        grunt,t_pov,t_dno,t_air,nach,prod,orlov,vidlov,kutok,rub,g_rask,v_rask,wire,gor,speed,kurs,ulov,uchet,avar,sel_r,
                        tral_info,info,dist,kollov,commenttr,maincomm
                        FROM tral WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','data','trl','prom_kv','rloc','rzon','rikes','rnorv','shir','dolg','v_wind','f_wind','volna',
                                    'oblaco','glub','grunt','t_pov','t_dno','t_air','nach','prod','orlov','vidlov','kutok','rub','g_rask','v_rask',
                                    'wire','gor','speed','kurs','ulov','uchet','avar','sel_r','tral_info','info','dist','kollov','commenttr','maincomm'],
                        
                        'order_by' : "ORDER BY ship,reis,trl;"                   
                    }
                }
            },

            'yarus': {
                'first_query' : """
                    set datestyle to DMY;

                    ALTER TABLE temp_y_biopit DISABLE TRIGGER ALL;
                    ALTER TABLE temp_y_biopap DISABLE TRIGGER ALL;
                    ALTER TABLE temp_y_razm DISABLE TRIGGER ALL;
                    ALTER TABLE temp_y_ulov DISABLE TRIGGER ALL;
                    ALTER TABLE temp_y_tral DISABLE TRIGGER ALL;

                    truncate temp_y_biopit;
                    truncate temp_y_biopap;
                    truncate temp_y_razm;
                    truncate temp_y_ulov;
                    truncate temp_y_tral;

                    ALTER TABLE temp_y_biopit ENABLE TRIGGER ALL;
                    ALTER TABLE temp_y_biopap ENABLE TRIGGER ALL;
                    ALTER TABLE temp_y_razm ENABLE TRIGGER ALL;
                    ALTER TABLE temp_y_ulov ENABLE TRIGGER ALL;
                    ALTER TABLE temp_y_tral ENABLE TRIGGER ALL;
                    """,

                'copy_queries': {
                    'y_biopit': """
                        COPY temp_y_biopit (ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,st_per,prpit)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,

                    'y_biopap': """
                        COPY temp_y_biopap (ship,reis,trl,kodvid,n_fish,l_big,l_lit,wes_ob,wes_bv,pol,zrel,puzo,salo,
                        w_pech,w_gonad,proba,w_food,n_ring,age_ring,type_lbig,type_llit,vozr1,vozr2,menu_kap,u_key,bio_info,skap_info)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,

                    'y_razm': """
                        COPY temp_y_razm (ship,reis,trl,kodvid,pol,tip_dl,lnf,kolf,u_key,step)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,

                    'y_ulov': """
                        COPY temp_y_ulov (ship,reis,trl,u_key,kodvid,u_wes,u_mech,u_fix,u_num,u_prc,promer,step)
                        FROM STDIN DELIMITER '|' CSV HEADER encoding 'windows-1251'
                    """,

                    'y_tral': """
                        COPY temp_y_tral (ship,reis,trl,data,stop_in,stop_ine,shir_beg,dolg_beg,glub,shir_end,
                        dolg_end,glub_end,kas_put,hook_put,len_yr,speed,kurs,data2,stop_outb,stop_out,kas_up,hook_up,speed_up,kurs_up,
                        prom_kv,prom_kvup,rloc,rzon,rikes,rnorv,v_wind,f_wind,volna,oblaco,t_air,t_pov,t_dno,s_dno,
                        vt_dno,ft_dno,grunt,yrtype,orlov,xreb,hook_type,hook_prc,bait1,baitprc1,bait2,baitprc2,bait3,baitprc3,ulov,avar)
                        FROM STDIN DELIMITER '|' CSV HEADER
                    """
                },

                'temp_queries': {
                    'Y_BIOPIT': {
                        'temp_qur' : f"SELECT * FROM temp_y_biopit WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,st_per,prpit
                        FROM y_biopit WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','kodvid','n_fish','bio_info','u_key','kodpit','st_per','prpit'],

                        'order_by' : "ORDER BY ship,reis,trl,kodvid,n_fish;"                
                    },

                    'Y_BIOPAP': {
                        'temp_qur' : f"SELECT * FROM temp_y_biopap WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,kodvid,n_fish,l_big,l_lit,wes_ob,wes_bv,pol,zrel,puzo,salo,w_pech,
                        w_gonad,proba,w_food,n_ring,age_ring,type_lbig,type_llit,vozr1,vozr2,menu_kap,u_key,bio_info,skap_info
                        FROM y_biopap WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','kodvid','n_fish','l_big','l_lit','wes_ob','wes_bv','pol','zrel','puzo','salo','w_pech',
                                    'w_gonad','proba','w_food','n_ring','age_ring','type_lbig','type_llit','vozr1','vozr2','menu_kap','u_key','bio_info','skap_info'],

                        'order_by' : "ORDER BY ship,reis,trl,kodvid,n_fish;"
                    },

                    'Y_RAZM': {
                        'temp_qur' : f"SELECT * FROM temp_y_razm WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,kodvid,pol,tip_dl,lnf,kolf,u_key,step
                        FROM y_razm WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','kodvid','pol','tip_dl','lnf','kolf','u_key','step'],

                        'order_by' : "ORDER BY ship,reis,trl,kodvid;"
                    },

                    'Y_ULOV': {
                        'temp_qur' : f"SELECT * FROM temp_y_ulov WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,trl,u_key,kodvid,u_wes,u_mech,u_fix,u_num,u_prc,promer,step
                        FROM y_ulov WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis','trl','u_key','kodvid','u_wes','u_mech','u_fix','u_num','u_prc','promer','step'],

                        'order_by' : "ORDER BY ship,reis,trl,kodvid;"
                    },

                    'Y_TRAL': {
                        'temp_qur' : f"SELECT * FROM temp_y_tral WHERE ship='{ship_value}' and reis={reis_value}",

                        'main_qur' : f"""SELECT ship,reis,"data",trl,stop_in,stop_ine,shir_beg,dolg_beg,glub,shir_end,
                        dolg_end,glub_end,kas_put,hook_put,len_yr,speed,kurs,data2,stop_outb,stop_out,kas_up,hook_up,speed_up,
                        kurs_up,prom_kv,prom_kvup,rloc,rzon,rikes,rnorv,v_wind,f_wind,volna,oblaco,grunt,t_pov,t_dno,t_air,s_dno,
                        vt_dno,ft_dno,yrtype,orlov,xreb,hook_type,hook_prc,bait1,baitprc1,bait2,baitprc2,bait3,baitprc3,ulov,avar
                        FROM y_tral WHERE ship='{ship_value}' and reis={reis_value}""",

                        'columns' : ['ship','reis',"data",'trl','stop_in','stop_ine','shir_beg','dolg_beg','glub','shir_end',
                        'dolg_end','glub_end','kas_put','hook_put','len_yr','speed','kurs','data2','stop_outb','stop_out','kas_up',
                        'hook_up','speed_up','kurs_up','prom_kv','prom_kvup','rloc','rzon','rikes','rnorv','v_wind','f_wind','volna',
                        'oblaco','grunt','t_pov','t_dno','t_air','s_dno','vt_dno','ft_dno','yrtype','orlov','xreb','hook_type','hook_prc',
                        'bait1','baitprc1','bait2','baitprc2','bait3','baitprc3','ulov','avar'],
                        
                        'order_by' : "ORDER BY ship,reis,trl;"                   
                    }
                }
            }
        }

        cursor.execute(query_dict.get(base).get('first_query'))

        try:

            for key, value in query_dict.get(base).get('copy_queries').items():
                print(key)
                file_name = f'{key}.csv'
                full_path = os.path.join(folder_path_new, file_name) #D:/bio/0812/UFJN121/fixed_csv\biokap.csv

                with open(full_path, 'r') as current_file:
                    cursor.copy_expert(value, current_file)

            connection.commit()
            print('Все загрузилось в temp таблицы...')

        except (Exception, psycopg2.Error) as error:
            showinfo('Информация', f'{error}')
            print("Ошибка при выполнении запроса:", error)

        save_path = folder_path
        logfile = save_path + r'\logbio.txt'
        log_bio = open(f"{logfile}", "w")

        for key, value in query_dict.get(base).get('temp_queries').items():
            insert_result = f"""
                {query_dict.get(base).get('temp_queries')[key].get('temp_qur')} except {query_dict.get(base).get('temp_queries')[key].get('main_qur')} {query_dict.get(base).get('temp_queries')[key].get('order_by')}
            """
            delete_result = f"""
                {query_dict.get(base).get('temp_queries')[key].get('main_qur')} except {query_dict.get(base).get('temp_queries')[key].get('temp_qur')} {query_dict.get(base).get('temp_queries')[key].get('order_by')}
            """
            count_qur = f"select count(*) as Количество_записей from temp_{key.lower()};"

# ==================== dataframes ====================
# --------- insert            
            df_insert = UploadDatas.postgresql_to_dataframe(self, connection, insert_result,
                                                            query_dict.get(base).get('temp_queries')[key].get('columns'))
            
            if key == 'BIOKAP':
                df_insert['kodpit'] = df_insert['kodpit'].map('{:.0f}'.format)

            data_insert = [[j for j in i[1:]] for i in df_insert.itertuples()]

# --------- delete
            df_delete = UploadDatas.postgresql_to_dataframe(self, connection, delete_result,
                                                            query_dict.get(base).get('temp_queries')[key].get('columns'))
            
            if key == 'BIOKAP':
                df_delete['kodpit'] = df_delete['kodpit'].map('{:.0f}'.format)

            data_delete = [[j for j in i[1:]] for i in df_delete.itertuples()]

# --------- count rows
            df_count = UploadDatas.postgresql_to_dataframe(self, connection, count_qur, ['Количество_записей'])
            count_rows_data = [[j for j in i[1:]] for i in df_count.itertuples()]      

# ---------
            pd.set_option('display.max_rows', None)      

            log_bio.write(f"""
                В таблицу {key} будет загружено:\n
{tabulate(data_insert, headers=query_dict.get(base).get('temp_queries')[key].get('columns'), tablefmt='psql')}\n

                Из таблицы {key} будет удалено:\n
{tabulate(data_delete, headers=query_dict.get(base).get('temp_queries')[key].get('columns'), tablefmt='psql')}\n

                Всего записей в {key}:\n
{tabulate(count_rows_data, headers=['Количество_записей'], tablefmt='psql')}                
            """)

        log_bio.close()

        cursor.close()
        connection.close()
        showinfo('Информация', f'Успех! Журнал предзагрузки выгружен в {save_path}/logbio.txt')

