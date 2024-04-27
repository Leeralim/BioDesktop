import csv, sqlite3

con = sqlite3.connect("dist_ships.db") # change to 'sqlite:///your_filename.db'
cur = con.cursor()
cur.execute("CREATE TABLE dist_ships (ship);") # use your column names here

with open('dist_ships.csv','r') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['ship']) for i in dr]

tuple_list = [(elem,) for elem in to_db]
# print(tuple_list)
cur.executemany("INSERT INTO dist_ships (ship) VALUES (?);", tuple_list)
con.commit()
con.close()


