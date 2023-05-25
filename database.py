import psycopg2
botcity = 'butovo'

class DB:
    def __init__(self, dbname, user, password, host):
        self.connection = psycopg2.connect(dbname=dbname, user=user, password=password, host=host, sslmode='disable')
        self.cursor = self.connection.cursor()
        self.connection.autocommit = True


    def add_user(self, user_id):
        with self.connection:
            self.cursor.execute('SELECT user_id FROM users WHERE user_id=%s', (user_id,))
            result = self.cursor.fetchone()
            if result == None:
                self.cursor.execute('INSERT INTO users (user_id) VALUES (%s)', (user_id,))
                return
            else:
                return

    def get_categoriesadm(self):
        with self.connection:
            self.cursor.execute('SELECT id, name FROM categories')
            result = self.cursor.fetchall()
            return result

    def add_cat(self, name):
        with self.connection:
            self.cursor.execute('INSERT INTO categories (name) VALUES (%s)', (name,))
            self.cursor.execute('SELECT id FROM categories WHERE name=%s ORDER BY id DESC', (name,))
            result = self.cursor.fetchone()
            catid = result[0]
            self.cursor.execute(f"UPDATE categories SET {botcity}='yes' WHERE id={catid}")
            return

    def get_catgoods(self, catid):
        with self.connection:
            self.cursor.execute('SELECT id, name, type FROM subcatgoods WHERE categoryid=%s ORDER BY id ASC', (catid,))
            result = self.cursor.fetchall()
            return result

    def get_subcatgoods(self, subcatid):
        with self.connection:
            self.cursor.execute('SELECT id, name FROM subcatgoods WHERE subcatid=%s ORDER BY id ASC', (subcatid,))
            result = self.cursor.fetchall()
            return result

    def get_catname(self, catid):
        with self.connection:
            self.cursor.execute('SELECT name FROM categories WHERE id=%s', (catid,))
            result = self.cursor.fetchone()
            return result[0]

    def get_citiescat(self, catid):
        with self.connection:
            self.cursor.execute('SELECT vladimir, skolkovo, vidnoe, sovhoz, miti, domod, moscow, pavelec, visota FROM categories WHERE id=%s', (catid,))
            result = self.cursor.fetchone()
            return result

    def get_citiessubcat(self, subcatid):
        with self.connection:
            self.cursor.execute('SELECT price_vladimir, price_skolkovo, price_vidnoe, price_sovhoz, price_miti, price_domod, price_moscow, price_pavelec, price_visota FROM subcatgoods WHERE id=%s', (subcatid,))
            result = self.cursor.fetchone()
            return result

    def updatecitycat(self, catid, city):
        with self.connection:
            self.cursor.execute(f"SELECT {city} FROM categories WHERE id={catid}")
            result = self.cursor.fetchone()
            if result[0] == 'no':
                self.cursor.execute(f"UPDATE categories SET {city}='yes' WHERE id={catid}")
            elif result[0] == 'yes':
                self.cursor.execute(f"UPDATE categories SET {city}='no' WHERE id={catid}")
            return

    def delcat(self, catid):
        with self.connection:
            self.cursor.execute('DELETE FROM subcatgoods WHERE categoryid=%s', (catid,))
            self.cursor.execute('DELETE FROM categories WHERE id=%s', (catid,))
            return

    def add_goodcat(self, catid, name, desc, price, photo):
        with self.connection:
            self.cursor.execute(f"INSERT INTO subcatgoods (categoryid, name, subcatid, type, description, photo, price_{botcity}) VALUES ({catid}, '{name}', 0, 'good', '{desc}', '{photo}', '{price}')")
            return

    def add_goodsubcat(self, subcatid, name, desc, price, photo):
        with self.connection:
            self.cursor.execute(f"INSERT INTO subcatgoods (name, subcatid, type, description, photo, price_{botcity}) VALUES ('{name}', {subcatid}, 'good', '{desc}', '{photo}', '{price}')")
            return

    def get_goodadm(self, goodid):
        with self.connection:
            self.cursor.execute('SELECT name, description, photo FROM subcatgoods WHERE id=%s', (goodid,))
            result = self.cursor.fetchone()
            return result

    def getcities_good(self, goodid):
        with self.connection:
            self.cursor.execute('SELECT price_vladimir, price_skolkovo, price_vidnoe, price_sovhoz, price_miti, price_domod, price_moscow, price_pavelec, price_visota FROM subcatgoods WHERE id=%s', (goodid,))
            result = self.cursor.fetchone()
            return result
    
    def delcity_good(self, goodid, city):
        with self.connection:
            self.cursor.execute(f"UPDATE subcatgoods SET price_{city}='0' WHERE id={goodid}")
            return

    def addcity_good(self, goodid, city, price):
        with self.connection:
            self.cursor.execute(f"UPDATE subcatgoods SET price_{city}='{price}' WHERE id={goodid}")
            return
    
    def delgood(self, goodid):
        with self.connection:
            self.cursor.execute('DELETE FROM subcatgoods WHERE id=%s', (goodid,))
            return
    
    def add_subcat(self, catid, name):
        with self.connection:
            self.cursor.execute(f"INSERT INTO subcatgoods (categoryid, name, subcatid, type, price_{botcity}) VALUES ({catid}, '{name}', 0, 'subcat', '1')")
            return

    def get_subcatname(self, subcatid):
        with self.connection:
            self.cursor.execute('SELECT name FROM subcatgoods WHERE id=%s', (subcatid,))
            result = self.cursor.fetchone()
            return result[0]

    def del_subcat(self, subcatid):
        with self.connection:
            self.cursor.execute('DELETE FROM subcatgoods WHERE subcatid=%s', (subcatid,))
            self.cursor.execute('DELETE FROM subcatgoods WHERE id=%s', (subcatid,))
            return
    
    def changecitysubcat(self, subcatid, city):
        with self.connection:
            self.cursor.execute(f"SELECT price_{city} FROM subcatgoods WHERE id={subcatid}")
            result = self.cursor.fetchone()
            if result[0] == '0':
                self.cursor.execute(f"UPDATE subcatgoods SET price_{city}='1' WHERE id={subcatid}")
            else:
                self.cursor.execute(f"UPDATE subcatgoods SET price_{city}='0' WHERE id={subcatid}")
            return

    def get_usercats(self):
        with self.connection:
            self.cursor.execute(f"SELECT id, name FROM categories WHERE {botcity}='yes'")
            result = self.cursor.fetchall()
            return result

    def get_usercatgoods(self, catid):
        with self.connection:
            self.cursor.execute(f"SELECT id, name, type FROM subcatgoods WHERE categoryid={catid} AND price_{botcity} != '0'")
            result = self.cursor.fetchall()
            return result

    def get_usersubcatgoods(self, subcatid):
        with self.connection:
            self.cursor.execute(f"SELECT id, name, type FROM subcatgoods WHERE subcatid={subcatid} AND price_{botcity} != '0'")
            result = self.cursor.fetchall()
            return result

    def get_gooduser(self, goodid):
        with self.connection:
            self.cursor.execute(f"SELECT name, description, photo, price_{botcity} FROM subcatgoods WHERE id={goodid}")
            result = self.cursor.fetchone()
            return result

    def add_box(self, user_id, goodid):
        with self.connection:
            self.cursor.execute('INSERT INTO box (user_id, goodid) VALUES (%s, %s)', (user_id, goodid))
            return

    def get_userbox(self, user_id):
        with self.connection:
            self.cursor.execute('SELECT goodid FROM box WHERE user_id=%s', (user_id,))
            result = self.cursor.fetchall()
            return result

    def clearbox(self, user_id):
        with self.connection:
            self.cursor.execute('DELETE FROM box WHERE user_id=%s', (user_id,))
            return
