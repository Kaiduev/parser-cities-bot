import psycopg2


class Database:

    def __init__(self, db_user, db_name, db_password, db_host):
        self.conn = psycopg2.connect(
            dbname=db_name, user=db_user,
            password=db_password, host=db_host
        )
        self.cursor = self.conn.cursor()

    def insert_data(self, cities) -> str:
        for city in cities:
            if len(city) != 0:
                sql = "INSERT INTO cities(name, name2, people_quantity, url) VALUES('{name}','{name2}','{people_quantity}','{url}')".format(
                    name=city.get("name", ""), name2=city.get("name2", ""),
                    people_quantity=city.get("people_quantity", ""), url=city.get("url", ""))
                self.cursor.execute(sql)
                self.conn.commit()
        return "done"

    def search_city(self, city_name):
        sql = "SELECT DISTINCT ON (name) name, id, name2, url, people_quantity FROM cities WHERE name LIKE '%{}%' or name2 LIKE '%{}%'".format(city_name, city_name)
        self.cursor.execute(sql)
        records = self.cursor.fetchall()
        return records

    def connection_close(self):
        self.conn.close()
