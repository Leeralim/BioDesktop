import psycopg2
import sqlite3
import os
import pandas as pd
import configparser
from tkinter.messagebox import showinfo
import numpy as np
import re
from cryptography.fernet import Fernet


# коннект к базе
class Database:
    def __init__(self):
        self.conn = None
        self.cursor = None
    
    def connect_ships(self):
        try:
            con = sqlite3.connect('dist_ships.db')
        except:
            print('Can`t establish connection to database')
            
        return con

    def connect_sqlight(self):
        try:
            con = sqlite3.connect('spr_ship.db')
        except:
            print('Can`t establish connection to database')

        return con


    def connect_db(self):
        try:
            # я предварительно зашифровала файл конфигурации и тут я даю расшфировку с помощью заранее сгенерированного ключа
            with open('filekey.key', 'rb') as filekey:
                key = filekey.read()
            fernet = Fernet(key)

            with open('config.ini', 'rb') as enc_file:
                encrypted = enc_file.read()
            
            decrypted = fernet.decrypt(encrypted).decode('utf-8')

            config = configparser.ConfigParser()
            # config.read('config/config.ini')
            config.read_string(decrypted)

            self.conn = psycopg2.connect(dbname=config['postgresql']['database'], 
                                         user=config['postgresql']['user'], 
                                         password=config['postgresql']['password'], 
                                         host=config['postgresql']['host'])

        except:
            print('Can`t establish connection to database')

        return self.conn
    

# получение таблицы
class GetTable:

    def unloading_tables(self, ship, reis, path, base):
        """
        выгрузка данных из базы в CSV
        """

        connection = Database.connect_db(self)
        cursor = connection.cursor()

        copy_dict = {
            'general': {
                'check_rows': """SELECT count(*) FROM tral WHERE ship='{}' and reis={};""",

                'tral': '''COPY (SELECT ship,reis,TO_CHAR(data,'dd/mm/yyyy'),trl,prom_kv,rloc,rzon,rikes,rnorv,shir,dolg,v_wind,f_wind,volna,oblaco,glub,
                grunt,t_pov,t_dno,t_air,nach,prod,orlov,vidlov,kutok,rub,g_rask,v_rask,wire,gor,speed,kurs,ulov,uchet,avar,sel_r,
                tral_info,info,dist FROM tral WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'ulov': '''COPY (SELECT ship,reis,trl,u_key,kodvid,u_wes,u_mech,u_fix,u_num,u_prc,promer,step FROM ulov 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'razm': '''COPY (SELECT ship,reis,trl,kodvid,pol,tip_dl,lnf,kolf,u_key,step FROM razm 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'biopap': '''COPY (SELECT ship,reis,trl,kodvid,n_fish,l_big,l_lit,wes_ob,wes_bv,pol,zrel,puzo,salo,w_pech,w_gonad,proba,
                w_food,n_ring,age_ring,type_lbig,type_llit,vozr1,vozr2,menu_kap,u_key,bio_info,skap_info FROM biopap 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'biopit': '''COPY (SELECT ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,st_per,prpit FROM biopit 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'pandalus': '''COPY (SELECT ship,reis,trl,u_key,kodvid,n_fish,carapace,sex,stgonad,stlink FROM pandalus 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'biokap': '''COPY (SELECT ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,st_per,l_pit,n_pit,w_pit,prpit,info_pit,info_rz,
                voz_pit,vos_wes,sred_ulov,devstage FROM biokap WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'trallist': '''COPY (select ship,reis,trl1,trl2,TO_CHAR(data1,'dd/mm/yyyy') as data1,TO_CHAR(data2,'dd/mm/yyyy') as data2,ntral,nulov,nbiopap,nbiopit,nrazm,nbiokap,npandalus,ncrabs,nmorph,nacq
                FROM tral_doc WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'crabs': '''COPY (SELECT ship,reis,trl,u_key,kodvid,n_krab,shirina,dlina,dlina_nr,dlina_rs,pol,linka,wes_ob,zrel_ikra,wes_ikra,diam_ikr,color_ikra,
                avr_nav,area_ulc,acquire,wes_eda,napoln,condil1,kol_cl1,condil2,kol_cl2,condil3,kol_cl3,condil4,kol_cl4,condil5,kol_cl5,condir1,kol_cr1,condir2,kol_cr2,
                condir3,kol_cr3,condir4,kol_cr4,condir5,kol_cr5,commenb FROM crabs WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER'''   ,

                'morph': '''COPY (SELECT ship,reis,trl,u_key,kodvid,n_krab,chela_w,chela_l,chela_h,mwl2_w,mwl2_l,mwl2_h,mwl3_w,mwl3_l,mwl3_h,mwl4_w,mwl4_l,mwl4_h,orbit_w,
                rostrm_w,abdom5_w FROM morph WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'acq': '''COPY (SELECT ship,reis,trl,u_key,kodvid,n_krab,object0,kol,kolleg FROM acq WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER'''
            },

            'yarus': {
                'check_rows': """SELECT count(*) FROM y_tral WHERE ship='{}' and reis={};""",

                'y_tral': '''COPY (SELECT ship,reis,trl,TO_CHAR(data,'dd/mm/yyyy') as data,stop_in,stop_ine,shir_beg,dolg_beg,glub,shir_end,dolg_end,
                glub_end,kas_put,hook_put,len_yr,speed,kurs,TO_CHAR(data2,'dd/mm/yyyy'),stop_outb,stop_out,kas_up,hook_up,speed_up,kurs_up,prom_kv,
                prom_kvup,rloc,rzon,rikes,rnorv,v_wind,f_wind,volna,oblaco,t_air,t_pov,t_dno,s_dno,vt_dno,ft_dno,grunt,yrtype,orlov,xreb,hook_type,
                hook_prc,bait1,baitprc1,bait2,baitprc2,bait3,baitprc3,ulov,avar FROM y_tral 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'y_ulov': '''COPY (SELECT ship,reis,trl,u_key,kodvid,u_wes,u_mech,u_fix,u_num,u_prc,promer,step FROM y_ulov 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'y_razm': '''COPY (SELECT ship,reis,trl,kodvid,pol,tip_dl,lnf,kolf,u_key,step from y_razm 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'y_biopap': '''COPY (SELECT ship,reis,trl,kodvid,n_fish,l_big,l_lit,wes_ob,wes_bv,pol,zrel,puzo,salo,w_pech,w_gonad,proba,w_food,n_ring,
                age_ring,type_lbig,type_llit,vozr1,vozr2,menu_kap,u_key,bio_info,skap_info FROM y_biopap 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'y_biopit': '''COPY (SELECT ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,st_per,prpit FROM y_biopit 
                WHERE ship='{}' and reis={})  to STDOUT DELIMITER '|' CSV HEADER''',

                'y_trallist': '''COPY (SELECT ship,reis,trl1,trl2,TO_CHAR(data1,'dd/mm/yyyy') as data1,TO_CHAR(data2,'dd/mm/yyyy') as data2,ntral,nulov,nbiopap,nbiopit,nrazm,nbiokap,npandalus,ncrabs,nmorph,nacq
                FROM tral_doc 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                # 'pandalus': '''COPY (SELECT ship,reis,trl,u_key,kodvid,n_fish,carapace,sex,stgonad,stlink FROM pandalus 
                # WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER'''
            },

            'norway': {
                'check_rows': """SELECT count(*) FROM tral_n WHERE ship='{}' and reis={};""",

                'tral_n': '''COPY (SELECT ship,reis,data,trl,prom_kv,rloc,rzon,rikes,rnorv,shir,dolg,v_wind,f_wind,
                volna,oblaco,glub,grunt,t_pov,t_dno,t_air,nach,prod,orlov,vidlov,kutok,rub,g_rask,v_rask,
                wire,gor,speed,kurs,ulov,uchet,avar,sel_r,tral_info,info,dist FROM tral_n 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'ulov_n': '''COPY (SELECT ship,reis,trl,u_key,kodvid,u_wes,u_mech,u_fix,u_num,u_prc,promer,step FROM ulov_n 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'biopap_n': '''COPY (SELECT ship,reis,trl,kodvid,n_fish,l_big,l_lit,wes_ob,wes_bv,pol,zrel,puzo,salo,w_pech,
                w_gonad,proba,w_food,n_ring,age_ring,type_lbig,type_llit,vozr1,vozr2,menu_kap,u_key,
                bio_info,skap_info from biopap_n 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'biokap_n': '''COPY (SELECT ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,st_per,l_pit,n_pit,w_pit,prpit,info_pit,
                info_rz,voz_pit,vos_wes,sred_ulov,devstage FROM biokap_n 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER''',

                'biopit_n': '''COPY (SELECT ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,st_per,prpit FROM biopit_n 
                WHERE ship='{}' and reis={})  to STDOUT DELIMITER '|' CSV HEADER''',

                'razm_n': '''COPY (SELECT ship,reis,trl,kodvid,pol,tip_dl,lnf,kolf,u_key,step FROM razm_n 
                WHERE ship='{}' and reis={}) to STDOUT DELIMITER '|' CSV HEADER'''                
            }

        }

        try:
            cursor.execute(copy_dict[base].get('check_rows').format(ship,reis))
            rows_count = cursor.fetchone()[0]
            print(rows_count)
            
            if rows_count > 0:
                # 'Записи есть!'
                for key, value in copy_dict.get(base).items():
                    if key == 'check_rows':
                        continue
                    file_name = f'{key}.csv'
                    output_path = os.path.join(path, file_name)
                    print(output_path)

                    with open(output_path, 'w') as current_file:
                        cursor.copy_expert(value.format(ship, reis), current_file)
                showinfo('Информация', f'Успех! Данные выгружены сюда: {path}')

            else:
                # 'Записей нет!'
                showinfo('Информация', f'В базе отсутствут записи по данным рейсам!')


        except (Exception, psycopg2.Error) as error:
            print("Ошибка при выполнении запроса:", error)

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()


# загрузка данных
class UploadDatas: # загрузка данных

# окошко с информацией
    def open_info():
        showinfo(title="Информация", message="Этот файл пустой!")

# Загрузка данных в базу
    def upload_into_db(self, path, base):
        # file_path = path
        if base == 'general':
            file_path = 'C:\\temp\general'
        else:
            file_path = 'C:\\temp\yarus'

        connection = Database.connect_db(self)
        cursor = connection.cursor()        

        enter_path = os.path.join(file_path,'fixed_csv')
        files_list = os.listdir(enter_path)

        # files_list = os.listdir(file_path)
        print(files_list)

        files_dict = {
            'general': {
                'files': {
                    'tral.csv': {'path': [], 'df': []},
                    'ulov.csv': {'path': [], 'df': []},
                    'biopap.csv': {'path': [], 'df': []},
                    'biokap.csv': {'path': [], 'df': []},
                    'razm.csv': {'path': [], 'df': []},
                    'pandalus.csv': {'path': [], 'df': []},
                    'biopit.csv': {'path': [], 'df': []},
                    'crabs.csv': {'path': [], 'df': []},
                    'acq.csv': {'path': [], 'df': []},
                    'morph.csv': {'path': [], 'df': []},
                    'trallist.csv': {'path': [], 'df': []},                       
                },

                'first_query': """
                    ALTER TABLE biokap DISABLE TRIGGER ALL;
                    ALTER TABLE biopit DISABLE TRIGGER ALL;
                    ALTER TABLE pandalus DISABLE TRIGGER ALL;
                    ALTER TABLE biopap DISABLE TRIGGER ALL;
                    ALTER TABLE razm DISABLE TRIGGER ALL;
                    ALTER TABLE ulov DISABLE TRIGGER ALL;
                    ALTER TABLE tral DISABLE TRIGGER ALL;
                    ALTER TABLE tral_doc DISABLE TRIGGER ALL;
                    ALTER TABLE crabs DISABLE TRIGGER ALL;
                    ALTER TABLE morph DISABLE TRIGGER ALL;
                    ALTER TABLE acq DISABLE TRIGGER ALL;

                    DELETE FROM biokap WHERE ship='{0}' AND reis={1};
                    DELETE FROM biopit WHERE ship='{0}' AND reis={1};
                    DELETE FROM pandalus WHERE ship='{0}' AND reis={1};
                    DELETE FROM biopap WHERE ship='{0}' AND reis={1};
                    DELETE FROM razm WHERE ship='{0}' AND reis={1};
                    DELETE FROM ulov WHERE ship='{0}' AND reis={1};
                    DELETE FROM tral WHERE ship='{0}' AND reis={1};
                    DELETE FROM tral_doc WHERE ship='{0}' AND reis={1};
                    DELETE FROM crabs WHERE ship='{0}' AND reis={1};
                    DELETE FROM morph WHERE ship='{0}' AND reis={1};
                    DELETE FROM acq WHERE ship='{0}' AND reis={1};

                    ALTER TABLE biokap ENABLE TRIGGER ALL;
                    ALTER TABLE biopit ENABLE TRIGGER ALL;
                    ALTER TABLE pandalus ENABLE TRIGGER ALL;
                    ALTER TABLE biopap ENABLE TRIGGER ALL;
                    ALTER TABLE razm ENABLE TRIGGER ALL;
                    ALTER TABLE ulov ENABLE TRIGGER ALL;
                    ALTER TABLE tral ENABLE TRIGGER ALL;
                    ALTER TABLE tral_doc ENABLE TRIGGER ALL;
                    ALTER TABLE crabs ENABLE TRIGGER ALL;
                    ALTER TABLE morph ENABLE TRIGGER ALL;
                    ALTER TABLE acq ENABLE TRIGGER ALL;
                    """,

                'copy_queries': {
                    'biokap': """COPY biokap (ship, reis, trl, kodvid, n_fish, bio_info, u_key, kodpit, st_per,
                    l_pit, n_pit, w_pit, prpit, info_pit, info_rz, voz_pit, vos_wes, sred_ulov, devstage)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",
                    
                    'pandalus': """COPY pandalus (ship, reis, trl, u_key, kodvid, n_fish, carapace, sex, stgonad, stlink)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'biopit': """COPY biopit (ship, reis, trl, kodvid, n_fish, bio_info, u_key, kodpit, st_per, prpit)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'biopap': """COPY biopap (ship, reis, trl, kodvid, n_fish, l_big, l_lit, wes_ob, wes_bv, pol, zrel,
                    puzo, salo, w_pech, w_gonad, proba, w_food, n_ring, age_ring, type_lbig, type_llit, vozr1,
                    vozr2, menu_kap, u_key, bio_info, skap_info) 
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'razm': """COPY razm (ship, reis, trl, kodvid, pol, tip_dl, lnf, kolf, u_key, step)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'ulov': """COPY ulov (ship, reis, trl, u_key, kodvid, u_wes, u_mech, u_fix, u_num, u_prc, promer, step) 
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'tral': """COPY tral (ship, reis, data, trl, prom_kv, rloc, rzon, rikes, rnorv, shir, dolg, v_wind, f_wind,
                    volna, oblaco, glub, grunt, t_pov, t_dno, t_air, nach, prod, orlov, vidlov, kutok, rub, g_rask, v_rask,
                    wire, gor, speed, kurs, ulov, uchet, avar, sel_r, tral_info, info, dist, kollov, commenttr, maincomm)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'trallist': """COPY tral_doc (ship,reis,trl1,trl2,data1,data2,ntral,nulov,nbiopap,nbiopit,nrazm,nbiokap,ins_date,
                    act_date,bort,priznrs,operator,npandalus,ncrabs,nmorph,nacq)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'crabs': """COPY crabs (ship,reis,trl,u_key,kodvid,n_krab,shirina,dlina,dlina_nr,dlina_rs,pol,linka,wes_ob,
                    zrel_ikra,wes_ikra,diam_ikr,color_ikra,avr_nav,area_ulc,acquire,wes_eda,napoln,condil1,kol_cl1,condil2,
                    kol_cl2,condil3,kol_cl3,condil4,kol_cl4,condil5,kol_cl5,condir1,kol_cr1,condir2,kol_cr2,condir3,kol_cr3,
                    condir4,kol_cr4,condir5,kol_cr5,commenb)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'acq': """COPY acq (ship,reis,trl,u_key,kodvid,n_krab,object0,kol,kolleg)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'morph': """COPY morph (ship,reis,trl,u_key,kodvid,n_krab,chela_w,chela_l,chela_h,mwl2_w,mwl2_l,mwl2_h,mwl3_w,mwl3_l,mwl3_h,
                    mwl4_w,mwl4_l,mwl4_h,orbit_w,rostrm_w,abdom5_w)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'"""
                },

                'post_query': """
                    UPDATE ulov SET trkl=(select trkl from tral where ulov.ship=tral.ship and ulov.reis=tral.reis and ulov.trl=tral.trl) 
                    where ship='{0}' and reis={1} and trkl is null;

                    UPDATE razm SET ulkl=(select ulkl from ulov where razm.ship=ulov.ship and razm.reis=ulov.reis and razm.trl=ulov.trl and razm.step=ulov.step 
                    and razm.kodvid=ulov.kodvid and razm.u_key=ulov.u_key) where ship='{0}' and reis={1} and ulkl is NULL;

                    UPDATE biopap SET (trkl,ulkl)=((select trkl,ulkl from ulov where biopap.ship=ulov.ship and biopap.reis=ulov.reis and biopap.trl=ulov.trl and 
                    biopap.kodvid=ulov.kodvid and biopap.u_key=ulov.u_key)) where ship='{0}' and reis={1} and ulkl is null;

                    UPDATE biopit SET bikl=(select bikl from biopap where biopit.ship=biopap.ship and biopit.reis=biopap.reis and biopit.trl=biopap.trl and 
                    biopit.kodvid=biopap.kodvid and biopit.u_key=biopap.u_key and biopit.bio_info=biopap.bio_info and biopit.n_fish=biopap.n_fish) 
                    where ship='{0}' and reis={1} and bikl is null;

                    UPDATE biokap SET bikl=(select bikl from biopap where biokap.ship=biopap.ship and biokap.reis=biopap.reis and biokap.trl=biopap.trl and 
                    biokap.kodvid=biopap.kodvid and biokap.u_key=biopap.u_key and biokap.bio_info=biopap.bio_info and biokap.n_fish=biopap.n_fish) 
                    where ship='{0}' and reis={1} and bikl is null;

                    UPDATE pandalus SET ulkl=(select ulkl from ulov where pandalus.ship=ulov.ship and pandalus.reis=ulov.reis and pandalus.trl=ulov.trl and 
                    pandalus.kodvid=ulov.kodvid and pandalus.u_key=ulov.u_key) 
                    where ship='{0}' and reis={1} and ulkl is NULL;

                    UPDATE crabs SET trkl=(select trkl from tral where crabs.ship=tral.ship and crabs.reis=tral.reis and crabs.trl=tral.trl) 
                    where ship='{0}' and reis={1} and trkl is null;

                    UPDATE acq SET crkl=(select crkl from crabs where acq.ship=crabs.ship and acq.reis=crabs.reis and acq.trl=crabs.trl and 
                    acq.u_key=crabs.u_key and acq.kodvid=crabs.kodvid and acq.n_krab=crabs.n_krab) 
                    where ship='{0}' and reis={1} and crkl is null;

                    UPDATE morph SET crkl=(select crkl from crabs where morph.ship=crabs.ship and morph.reis=crabs.reis and morph.trl=crabs.trl and 
                    morph.u_key=crabs.u_key and morph.kodvid=crabs.kodvid and morph.n_krab=crabs.n_krab) 
                    where ship='{0}' and reis={1} and crkl is null;
            """
            },

            'yarus': {
                'files': {
                    'y_tral.csv': {'path': [], 'df': []},
                    'y_ulov.csv': {'path': [], 'df': []},
                    'y_biopap.csv': {'path': [], 'df': []},
                    # 'y_biokap.csv': {'path': [], 'df': []},
                    'y_razm.csv': {'path': [], 'df': []},
                    'y_biopit.csv': {'path': [], 'df': []},
                    'y_trallist.csv': {'path': [], 'df': []},                    
                },

                'first_query': """
                    ALTER TABLE y_biopit DISABLE TRIGGER ALL;
                    ALTER TABLE y_biopap DISABLE TRIGGER ALL;
                    ALTER TABLE y_razm DISABLE TRIGGER ALL;
                    ALTER TABLE y_ulov DISABLE TRIGGER ALL;
                    ALTER TABLE y_tral DISABLE TRIGGER ALL;
                    ALTER TABLE tral_doc DISABLE TRIGGER ALL;

                    DELETE FROM y_biopit WHERE ship='{0}' AND reis={1};
                    DELETE FROM y_biopap WHERE ship='{0}' AND reis={1};
                    DELETE FROM y_razm WHERE ship='{0}' AND reis={1};
                    DELETE FROM y_ulov WHERE ship='{0}' AND reis={1};
                    DELETE FROM y_tral WHERE ship='{0}' AND reis={1};
                    DELETE FROM tral_doc WHERE ship='{0}' AND reis={1};

                    ALTER TABLE y_biopit ENABLE TRIGGER ALL;
                    ALTER TABLE y_biopap ENABLE TRIGGER ALL;
                    ALTER TABLE y_razm ENABLE TRIGGER ALL;
                    ALTER TABLE y_ulov ENABLE TRIGGER ALL;
                    ALTER TABLE y_tral ENABLE TRIGGER ALL;
                    ALTER TABLE tral_doc ENABLE TRIGGER ALL;
                    """,

                'copy_queries': {
                    'y_biopit': """COPY y_biopit (ship,reis,trl,kodvid,n_fish,bio_info,u_key,kodpit,st_per,prpit)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'y_biopap': """COPY y_biopap (ship,reis,trl,kodvid,n_fish,l_big,l_lit,wes_ob,wes_bv,pol,zrel,
                    puzo,salo,w_pech,w_gonad,proba,w_food,n_ring,age_ring,type_lbig,type_llit,vozr1,
                    vozr2,menu_kap,u_key,bio_info,skap_info) 
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'y_razm': """COPY y_razm (ship,reis,trl,kodvid,pol,tip_dl,lnf,kolf,u_key,step)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'y_ulov': """COPY y_ulov (ship,reis,trl,u_key,kodvid,u_wes,u_mech,u_fix,u_num,u_prc,promer,step) 
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'y_tral': """COPY y_tral (ship,reis,trl,data,stop_in,stop_ine,shir_beg,dolg_beg,glub,shir_end,
                    dolg_end,glub_end,kas_put,hook_put,len_yr,speed,kurs,data2,stop_outb,stop_out,kas_up,hook_up,speed_up,kurs_up,
                    prom_kv,prom_kvup,rloc,rzon,rikes,rnorv,v_wind,f_wind,volna,oblaco,t_air,t_pov,t_dno,s_dno,
                    vt_dno,ft_dno,grunt,yrtype,orlov,xreb,hook_type,hook_prc,bait1,baitprc1,bait2,baitprc2,bait3,baitprc3,ulov,avar)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'y_trallist': """COPY tral_doc (ship,reis,trl1,trl2,data1,data2,ntral,nulov,nbiopap,nbiopit,nrazm,nbiokap,ins_date,
                    act_date,bort,priznrs,operator,npandalus,ncrabs,nmorph,nacq)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'"""
                },

                'post_query': """
                    UPDATE y_ulov SET trkl=(select trkl from y_tral where y_ulov.ship=y_tral.ship and y_ulov.reis=y_tral.reis and y_ulov.trl=y_tral.trl) 
                    where ship='{0}' and reis={1} and trkl is null;

                    UPDATE y_razm SET ulkl=(select ulkl from y_ulov where y_razm.ship=y_ulov.ship and y_razm.reis=y_ulov.reis and y_razm.trl=y_ulov.trl and 
                    y_razm.step=y_ulov.step and y_razm.kodvid=y_ulov.kodvid and y_razm.u_key=y_ulov.u_key) 
                    where ship='{0}' and reis={1} and ulkl is NULL;

                    UPDATE y_biopap SET (trkl,ulkl)=((select trkl,ulkl from y_ulov where y_biopap.ship=y_ulov.ship and y_biopap.reis=y_ulov.reis and
                    y_biopap.trl=y_ulov.trl and y_biopap.kodvid=y_ulov.kodvid and y_biopap.u_key=y_ulov.u_key)) 
                    where ship='{0}' and reis={1} and ulkl is null;

                    UPDATE y_biopit SET bikl=(select bikl from y_biopap where y_biopit.ship=y_biopap.ship and y_biopit.reis=y_biopap.reis and y_biopit.trl=y_biopap.trl and 
                    y_biopit.kodvid=y_biopap.kodvid and y_biopit.u_key=y_biopap.u_key and y_biopit.bio_info=y_biopap.bio_info and y_biopit.n_fish=y_biopap.n_fish) 
                    where ship='{0}' and reis={1} and bikl is null;
                    """
            },

            'norway': {
                'files': {
                    'tral.csv': {'path': [], 'df': []},
                    'ulov.csv': {'path': [], 'df': []},
                    'biopap.csv': {'path': [], 'df': []},
                    'biokap.csv': {'path': [], 'df': []},
                    'razm.csv': {'path': [], 'df': []},
                    'pandalus.csv': {'path': [], 'df': []},
                    'biopit.csv': {'path': [], 'df': []},
                },

                'first_query': """
                    ALTER TABLE biokap_n DISABLE TRIGGER ALL;
                    ALTER TABLE biopit_n DISABLE TRIGGER ALL;
                    ALTER TABLE pandalus DISABLE TRIGGER ALL;
                    ALTER TABLE biopap_n DISABLE TRIGGER ALL;
                    ALTER TABLE razm_n DISABLE TRIGGER ALL;
                    ALTER TABLE ulov_n DISABLE TRIGGER ALL;
                    ALTER TABLE tral_n DISABLE TRIGGER ALL;

                    DELETE FROM biokap_n WHERE ship='{0}' AND reis={1};
                    DELETE FROM biopit_n WHERE ship='{0}' AND reis={1};
                    DELETE FROM pandalus WHERE ship='{0}' AND reis={1};
                    DELETE FROM biopap_n WHERE ship='{0}' AND reis={1};
                    DELETE FROM razm_n WHERE ship='{0}' AND reis={1};
                    DELETE FROM ulov_n WHERE ship='{0}' AND reis={1};
                    DELETE FROM tral_n WHERE ship='{0}' AND reis={1};

                    ALTER TABLE biokap_n ENABLE TRIGGER ALL;
                    ALTER TABLE biopit_n ENABLE TRIGGER ALL;
                    ALTER TABLE pandalus ENABLE TRIGGER ALL;
                    ALTER TABLE biopap_n ENABLE TRIGGER ALL;
                    ALTER TABLE razm_n ENABLE TRIGGER ALL;
                    ALTER TABLE ulov_n ENABLE TRIGGER ALL;
                    ALTER TABLE tral_n ENABLE TRIGGER ALL;
                    """,

                'copy_queries': {
                    'biokap': """COPY biokap_n (ship, reis, trl, kodvid, n_fish, bio_info, u_key, kodpit, st_per,
                    l_pit, n_pit, w_pit, prpit, info_pit, info_rz, voz_pit, vos_wes, sred_ulov)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'pandalus': """COPY pandalus (ship, reis, trl, u_key, kodvid, n_fish, carapace, sex, stgonad, stlink)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'biopit': """COPY biopit_n (ship, reis, trl, kodvid, n_fish, bio_info, u_key, kodpit, st_per, prpit)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'biopap': """COPY biopap_n (ship, reis, trl, kodvid, n_fish, l_big, l_lit, wes_ob, wes_bv, pol, zrel,
                    puzo, salo, w_pech, w_gonad, proba, w_food, n_ring, age_ring, type_lbig, type_llit, vozr1,
                    vozr2, menu_kap, u_key, bio_info, skap_info) 
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'razm': """COPY razm_n (ship, reis, trl, kodvid, pol, tip_dl, lnf, kolf, u_key, step)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'ulov': """COPY ulov_n (ship, reis, trl, u_key, kodvid, u_wes, u_mech, u_fix, u_num, u_prc, promer, step) 
                    FROM STDIN WITH HEADER CSV DELIMITER '|'""",

                    'tral': """COPY tral_n (ship, reis, data, trl, prom_kv, rloc, rzon, rikes, rnorv, shir, dolg, v_wind, f_wind,
                    volna, oblaco, glub, grunt, t_pov, t_dno, t_air, nach, prod, orlov, vidlov, kutok, rub, g_rask, v_rask,
                    wire, gor, speed, kurs, ulov, uchet, avar, sel_r, tral_info, info, dist)
                    FROM STDIN WITH HEADER CSV DELIMITER '|'"""
                },

                'post_query': """
                    UPDATE ulov_n SET trkl=(select trkl from tral_n where ulov_n.ship=tral_n.ship and ulov_n.reis=tral_n.reis and ulov_n.trl=tral_n.trl) 
                    where ship='{0}' and reis={1} and trkl is null;

                    UPDATE razm_n SET ulkl=(select ulkl from ulov_n where razm_n.ship=ulov_n.ship and razm_n.reis=ulov_n.reis and razm_n.trl=ulov_n.trl and razm_n.step=ulov_n.step 
                    and razm_n.kodvid=ulov_n.kodvid and razm_n.u_key=ulov_n.u_key) where ship='{0}' and reis={1} and ulkl is NULL;

                    UPDATE biopap_n SET (trkl,ulkl)=((select trkl,ulkl from ulov_n where biopap_n.ship=ulov_n.ship and biopap_n.reis=ulov_n.reis and biopap_n.trl=ulov_n.trl and 
                    biopap_n.kodvid=ulov_n.kodvid and biopap_n.u_key=ulov_n.u_key)) where ship='{0}' and reis={1} and ulkl is null;

                    UPDATE biopit_n SET bikl=(select bikl from biopap_n where biopit_n.ship=biopap_n.ship and biopit_n.reis=biopap_n.reis and biopit_n.trl=biopap_n.trl and biopit_n.kodvid=biopap_n.kodvid and 
                    biopit_n.u_key=biopap_n.u_key and biopit_n.bio_info=biopap_n.bio_info and biopit_n.n_fish=biopap_n.n_fish) where ship='{0}' and reis={1} and bikl is null;

                    UPDATE biokap_n SET bikl=(select bikl from biopap_n where biokap_n.ship=biopap_n.ship and biokap_n.reis=biopap_n.reis and biokap_n.trl=biopap_n.trl and biokap_n.kodvid=biopap_n.kodvid and 
                    biokap_n.u_key=biopap_n.u_key and biokap_n.bio_info=biopap_n.bio_info and biokap_n.n_fish=biopap_n.n_fish) where ship='{0}' and reis={1} and bikl is null;

                    UPDATE pandalus SET ulkl=(select ulkl from ulov_n where pandalus.ship=ulov_n.ship and pandalus.reis=ulov_n.reis and pandalus.trl=ulov_n.trl and pandalus.kodvid=ulov_n.kodvid and 
                    pandalus.u_key=ulov_n.u_key) 
                    where ship='{0}' and reis={1} and ulkl is NULL;
                    """
            }
        }

        for i in files_list:
            if i == 'Y_Biokap.csv':
                continue

            curr_file = f"{file_path}/fixed_csv/{i}"
            # print(curr_file)

            if not os.path.isfile(curr_file):
                print(f'not os.path.isfile({curr_file})\n')
                continue
            if not i.lower() in [k.lower() for k in files_dict.get(base).get('files')]:
                print(f'not i in files_dict: {i}\n')
                continue

            try:
                df = pd.read_csv(curr_file, encoding='utf-8', sep='|')
                # print(df.columns)
            except UnicodeDecodeError:
                df = pd.read_csv(curr_file, encoding='latin-1', sep='|')
            # except ValueError:
            #     df = pd.read_csv(curr_file, encoding='ISO8601', sep='|')
            except pd.errors.EmptyDataError:
                files_dict.get(base).get('files')[i.split('/')[-1].lower()].get('path').append(curr_file)
                continue

            files_dict.get(base).get('files')[i.split('/')[-1].lower()].get('path').append(curr_file)
            files_dict.get(base).get('files')[i.split('/')[-1].lower()].get('df').append(df)
            
        try:
            pattern = re.compile(r'(^Y_)?Tral(_n)?\.csv')
            tral_file = [file for file in files_list if pattern.search(file)]
            # print(tral_file)

            tral_df = files_dict.get(base).get('files')[tral_file[0].lower()].get('df')[0]
            ship_reis = tral_df.groupby(['ship', 'reis']).size().reset_index().rename(columns={0: 'count'})
            # print(tral_df)

            for index, row in ship_reis.iterrows():
                ship_value = row['ship']
                reis_value = row['reis']

            cursor.execute(files_dict.get(base).get('first_query').format(ship_value, reis_value))
            connection.commit()
            
            for i in files_dict.get(base).get('files').items():
                print(i)
                file_key = i[1].get('path')[0].split("/")[-1].split('.')[0].lower()
                print(file_key)
                with open(f"{i[1].get('path')[0]}") as f:
                    # print(f.readline())
                    if file_key in files_dict.get(base).get('copy_queries'):
                        cursor.copy_expert(files_dict.get(base).get('copy_queries')[file_key], f)
                    else:
                        continue

            cursor.execute(files_dict.get(base).get('post_query').format(ship_value, reis_value))
            connection.commit()

            showinfo(title="Информация", message="Данные загружены!")

            cursor.close()
            connection.close()

        except Exception as e:
            print(f"{e}")
            
# Удаление рейса из базы
    def del_reis(self, param1, param2, base):
        connection = Database.connect_db(self)
        cursor = connection.cursor()
        cursor2 = connection.cursor()

        query_dict = {
            'general': {
                'select_script': """
                    SELECT count(*) FROM tral
                    WHERE ship='{0}' AND reis={1};
                    """,
                'delete_script': """
                    ALTER TABLE biokap DISABLE TRIGGER ALL;
                    ALTER TABLE biopit DISABLE TRIGGER ALL;
                    ALTER TABLE pandalus DISABLE TRIGGER ALL;
                    ALTER TABLE biopap DISABLE TRIGGER ALL;
                    ALTER TABLE razm DISABLE TRIGGER ALL;
                    ALTER TABLE ulov DISABLE TRIGGER ALL;
                    ALTER TABLE tral DISABLE TRIGGER ALL;
                    ALTER TABLE crabs DISABLE TRIGGER ALL;
                    ALTER TABLE acq DISABLE TRIGGER ALL;
                    ALTER TABLE morph DISABLE TRIGGER ALL;

                    DELETE FROM biokap WHERE ship='{0}' AND reis={1};
                    DELETE FROM biopit WHERE ship='{0}' AND reis={1};
                    DELETE FROM pandalus WHERE ship='{0}' AND reis={1};
                    DELETE FROM biopap WHERE ship='{0}' AND reis={1};
                    DELETE FROM razm WHERE ship='{0}' AND reis={1};
                    DELETE FROM ulov WHERE ship='{0}' AND reis={1};
                    DELETE FROM tral WHERE ship='{0}' AND reis={1};
                    DELETE FROM crabs WHERE ship='{0}' AND reis={1};
                    DELETE FROM acq WHERE ship='{0}' AND reis={1};
                    DELETE FROM morph WHERE ship='{0}' AND reis={1};

                    ALTER TABLE biokap ENABLE TRIGGER ALL;
                    ALTER TABLE biopit ENABLE TRIGGER ALL;
                    ALTER TABLE pandalus ENABLE TRIGGER ALL;
                    ALTER TABLE biopap ENABLE TRIGGER ALL;
                    ALTER TABLE razm ENABLE TRIGGER ALL;
                    ALTER TABLE ulov ENABLE TRIGGER ALL;
                    ALTER TABLE tral ENABLE TRIGGER ALL;
                    ALTER TABLE crabs ENABLE TRIGGER ALL;
                    ALTER TABLE acq ENABLE TRIGGER ALL;
                    ALTER TABLE morph ENABLE TRIGGER ALL;
                    """
                },
            
            'yarus': {
                'select_script': """
                    SELECT count(*) FROM y_tral
                    WHERE ship='{0}' AND reis={1};
                    """,
                'delete_script': """
                    ALTER TABLE y_biopit DISABLE TRIGGER ALL;
                    ALTER TABLE y_biopap DISABLE TRIGGER ALL;
                    ALTER TABLE y_razm DISABLE TRIGGER ALL;
                    ALTER TABLE y_ulov DISABLE TRIGGER ALL;
                    ALTER TABLE y_tral DISABLE TRIGGER ALL;
                    ALTER TABLE tral_doc DISABLE TRIGGER ALL;

                    DELETE FROM y_biopit WHERE ship='{0}' AND reis={1};
                    DELETE FROM y_biopap WHERE ship='{0}' AND reis={1};
                    DELETE FROM y_razm WHERE ship='{0}' AND reis={1};
                    DELETE FROM y_ulov WHERE ship='{0}' AND reis={1};
                    DELETE FROM y_tral WHERE ship='{0}' AND reis={1};
                    DELETE FROM tral_doc WHERE ship='{0}' AND reis={1};

                    ALTER TABLE y_biopit ENABLE TRIGGER ALL;
                    ALTER TABLE y_biopap ENABLE TRIGGER ALL;
                    ALTER TABLE y_razm ENABLE TRIGGER ALL;
                    ALTER TABLE y_ulov ENABLE TRIGGER ALL;
                    ALTER TABLE y_tral ENABLE TRIGGER ALL;
                    ALTER TABLE tral_doc ENABLE TRIGGER ALL;
                    """
                },

            'norway': {
                'select_script': """
                    SELECT distinct t.ship, t.reis from tral_n t
                    JOIN biopap_n b ON b.trkl = t.trkl
                    WHERE extract(year from t."data")='{0}' AND b.kodvid='{1}';
                    """,
                'delete_script': """
                    ALTER TABLE biopit_n DISABLE TRIGGER ALL;
                    ALTER TABLE biopap_n DISABLE TRIGGER ALL;
                    ALTER TABLE biokap_n DISABLE TRIGGER ALL;
                    ALTER TABLE razm_n DISABLE TRIGGER ALL;
                    ALTER TABLE ulov_n DISABLE TRIGGER ALL;
                    ALTER TABLE tral_n DISABLE TRIGGER ALL;

                    DELETE FROM biopit_n WHERE ship='{0}' AND reis IN {1};
                    DELETE FROM biopap_n WHERE ship='{0}' AND reis IN {1};
                    DELETE FROM biokap_n WHERE ship='{0}' AND reis IN {1};
                    DELETE FROM razm_n WHERE ship='{0}' AND reis IN {1};
                    DELETE FROM ulov_n WHERE ship='{0}' AND reis IN {1};
                    DELETE FROM tral_n WHERE ship='{0}' AND reis IN {1};

                    ALTER TABLE biopit_n ENABLE TRIGGER ALL;
                    ALTER TABLE biopap_n ENABLE TRIGGER ALL;
                    ALTER TABLE biokap_n ENABLE TRIGGER ALL;
                    ALTER TABLE razm_n ENABLE TRIGGER ALL;
                    ALTER TABLE ulov_n ENABLE TRIGGER ALL;
                    ALTER TABLE tral_n ENABLE TRIGGER ALL;
                    """
                }
        }

        try:
        # cursor.execute(query_dict.get(base).get('select_script').format(param1, param2))
        # row = cursor.fetchall()
        # print(row)
            if base == 'norway':
                cursor.execute(query_dict.get(base).get('select_script').format(param1, param2))
                row = cursor.fetchall()
                # print(row)
                dict_params = dict()
                if len(row) > 0:
                    for i in row:
                        if i[0] in dict_params:
                            dict_params[i[0]].append(i[1])
                        else:
                            dict_params[i[0]] = [i[1]]
                    
                    for ship, reis in dict_params.items():
                        if len(reis) == 1:
                            reis = f'({reis[0]})'
                            cursor2.execute(query_dict.get(base).get('delete_script').format(ship, reis))
                            connection.commit()
                        elif len(reis) > 1:
                            cursor2.execute(query_dict.get(base).get('delete_script').format(ship, tuple(reis)))
                            connection.commit()
                        
                        connection.commit()

                    showinfo(title="Информация", message="Рейсы {0} удалены из базы.".format(dict_params))
                
                    cursor2.close()
                else:
                    showinfo(title="Информация", message="Информация отсутствует в базе.")

            else:
                cursor.execute(query_dict.get(base).get('select_script').format(param1, param2))
                rows_count = cursor.fetchone()[0]

                if rows_count > 0:
                    cursor.execute(query_dict.get(base).get('delete_script').format(param1, param2))
                    connection.commit()
                    showinfo(title="Информация", message="Рейс {0} {1} удален из базы.".format(param1, param2))
                else:
                    showinfo(title="Информация", message="Рейс {0} {1} отсутствует в базе.".format(param1, param2))


            cursor.close()
            connection.close()

        except Exception as e:
            showinfo(title="Информация", message=f"Данные не удалены.\n Ошибка: {e}")

# корректировка признака рейса (для всех)
    def correct_prizn(self, ship, reis, new_prizn, new_oper):
        connection = Database.connect_db(self)
        cursor = connection.cursor()

        try:
            if new_prizn == '' and new_oper == '':
                sql_script = """UPDATE tral_doc SET (priznrs,operator)=(null,null) where ship=%s and reis=%s;"""
                cursor.execute(sql_script, (ship, reis))
            else:
                sql_script = 'UPDATE tral_doc SET (priznrs,operator)=(%s,%s) where ship=%s and reis=%s;'

                cursor.execute(sql_script, (new_prizn, new_oper, ship, reis))

            connection.commit()

            showinfo(title="Информация", message=f"Информация скорректирована успешно!")

        except Exception as e:
            showinfo(title="Информация", message=f"Ошибка: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

# корректировка рейса
    def corr_reis(self, ship, reis, new_ship, new_reis, base):
        connection = Database.connect_db(self)
        cursor = connection.cursor()

        query_dict = {
            'general': {
                'count_query': "SELECT count(*) FROM tral WHERE ship='{0}' and reis={1};",

                'correct_query': """
                    UPDATE biokap SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE biopit SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE pandalus SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE biopap SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE razm SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE ulov SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE tral SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE tral_doc SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    """
            },

            'yarus': {
                'count_query': "SELECT count(*) FROM y_tral WHERE ship='{0}' and reis={1};",

                'correct_query': """
                    UPDATE y_biopit SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE y_biopap SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE y_razm SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE y_ulov SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE y_tral SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    UPDATE tral_doc SET (ship,reis)=('{0}',{1}) WHERE ship='{2}' and reis={3};
                    """
            }
        }

        cursor.execute(query_dict.get(base).get('count_query').format(new_ship, new_reis))
        row = cursor.fetchone()

        if row[0] > 0:
            showinfo(title="Информация", message=f"Рейс {new_ship} {new_reis} уже есть в базе!")
            cursor.close()
            connection.close()

        else:
            cursor.execute(query_dict.get(base).get('correct_query').format(new_ship, new_reis, ship, reis))

            connection.commit()
            showinfo(title="Информация", message=f"Рейс заменен успешно!")

            cursor.close()
            connection.close()

# корректировка пробы базовая
    def corr_proba(self, ship, reis, trl, kodvid, bio_info, u_key, new_proba, base):
        connection = Database.connect_db(self)
        cursor = connection.cursor()

        dict_query = {
            'general': {
                'update_new_proba': "UPDATE biopap set proba={0} where ship='{1}' and reis={2} and trl in {3} and kodvid={4} and bio_info={5} and u_key='{6}';"
            },

            'yarus': {
                'update_new_proba': "UPDATE y_biopap set proba={0} where ship='{1}' and reis={2} and trl in {3} and kodvid={4} and bio_info={5} and u_key='{6}';"
            }
        }

        try:

            if len(trl) == 1:
                trl = f"({trl[0]})"
            else:
                trl = f"({','.join(trl)})"

            if new_proba == '':
                new_proba = 'NULL'

            cursor.execute(dict_query.get(base).get('update_new_proba').format(new_proba, ship, reis, trl, kodvid, bio_info, u_key))
            connection.commit()

            print("Ну все....*????")
            showinfo(title="Информация", message=f"Проба скорректирована")

        except Exception as e:
            print(e)
            showinfo(title="Информация", message=f"Ошибка: {e}")

        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

# делаем из запроса к постгресу датафрейм
    def postgresql_to_dataframe(self, conn, select_query, column_names):
        """
        Tranform a SELECT query into a pandas dataframe
        """
        cursor = conn.cursor()
        try:
            cursor.execute(select_query)
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            cursor.close()
            return 1
        
        # Naturally we get a list of tupples
        tupples = cursor.fetchall()
        cursor.close()
        
        # We just need to turn it into a pandas dataframe
        df = pd.DataFrame(tupples, columns=column_names)
        return df            

# выборка данных из основной базы (отображает в таблице)
    def select_data(self, ship, reis, trl, kodvid, bio_info, u_key, base):
        # Connect to the database
        conn = Database.connect_db(self)

        dict_query = {

            'columns': ['bikl', 'ship','reis','trl','kodvid','n_fish','bio_info','u_key','vozr1','vozr2','l_big','l_lit','n_ring'],

            'select_query': """
                SELECT bikl,ship,reis,trl,kodvid,n_fish,bio_info,u_key,vozr1,vozr2,l_big,l_lit,n_ring 
                FROM {0} 
                WHERE ship='{1}' AND reis={2} AND trl={3} AND kodvid={4} AND bio_info={5} AND u_key='{6}';
                """,

            'general': {
                'table': 'biopap',
            },

            'yarus': {
                'table': 'y_biopap',
            }
        }

        df = UploadDatas.postgresql_to_dataframe(self, conn, dict_query.get('select_query').format(dict_query.get(base).get('table'),
                                                                                                   ship, reis, trl, kodvid, bio_info, u_key), dict_query.get('columns'))
        # print(df)
        data = [[j for j in i[1:]] for i in df.itertuples()]

        self.sheet.set_sheet_data(data = data,
                                  reset_col_positions = True,
                                  reset_row_positions = True,
                                  redraw = True,
                                  verify = False,
                                  reset_highlights = False)
        
        self.sheet.display_columns(columns=[i for i in range(1, len(dict_query.get('columns')))], all_displayed = False, redraw = True,)
        self.sheet.set_all_column_widths()
        self.sheet.readonly_columns(columns = [i for i in range(1,8)], readonly = True, redraw = True)


# показываем данные в таблице и заливаем изменения
    def correct_age(self, base):
        a = self.sheet.data

        dict_query = {
            'header': ['bikl','ship','reis','trl','kodvid','n_fish','bio_info','u_key','vozr1','vozr2','l_big','l_lit','n_ring'],

            'columns_to_update': ['l_lit', 'l_big', 'n_ring', 'vozr1', 'vozr2'],

            'update_queries': {
                'yarus': {
                    'vozr1': """
                        UPDATE y_biopap
                        SET vozr1 = {0}
                        WHERE bikl = {1};
                    """,

                    'vozr2': """
                        UPDATE y_biopap
                        SET vozr2 = {0}
                        WHERE bikl = {1};
                    """,

                    'l_lit': """
                        UPDATE y_biopap
                        SET l_lit = {0}
                        WHERE bikl = {1};
                    """,

                    'l_big': """
                        UPDATE y_biopap
                        SET l_big = {0}
                        WHERE bikl = {1};
                    """,

                    'n_ring': """
                        UPDATE y_biopap
                        SET n_ring = {0}
                        WHERE bikl = {1};
                    """
                },

                'general': {
                    'vozr1': """
                        UPDATE biopap
                        SET vozr1 = {0}
                        WHERE bikl = {1};
                    """,

                    'vozr2': """
                        UPDATE biopap
                        SET vozr2 = {0}
                        WHERE bikl = {1};
                    """,

                    'l_lit': """
                        UPDATE biopap
                        SET l_lit = {0}
                        WHERE bikl = {1};
                    """,

                    'l_big': """
                        UPDATE biopap
                        SET l_big = {0}
                        WHERE bikl = {1};
                    """,

                    'n_ring': """
                        UPDATE biopap
                        SET n_ring = {0}
                        WHERE bikl = {1};
                    """                    
                }
            }
        }

        header = dict_query.get('header')
        df = pd.DataFrame(a, columns=header)

        for col in dict_query.get('columns_to_update'):
            df[col] = df[col].replace(r'^\s*$', None, regex=True)

            df = df.astype({col: 'float64'})

        conn = Database.connect_db(self)
        cursor = conn.cursor()

        for index, row in df.iterrows():
            pk = int(row['bikl'])

            for column in dict_query.get('columns_to_update'):
                value = row[column]

                correct_value = 'null' if value == None else value

                if correct_value == 'null':
                    continue
                else:
                    if (not np.isnan(correct_value)):
                        correct_value = int(correct_value)
                        cursor.execute(dict_query.get('update_queries').get(base)[column].format(correct_value, pk))
                    if np.isnan(correct_value):
                        cursor.execute(dict_query.get('update_queries').get(base)[column].format('NULL', pk))


        print("Данные изменены")
        showinfo('Информация', f'Успех! Данные изменены')

        conn.commit()            
        cursor.close()
        conn.close()

