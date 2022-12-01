# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import sqlite3

class FranchPipeline:
    def __init__(self) -> None:
        self.create_connection()
        self.create_table()

    def create_connection(self):
        self.conn = sqlite3.connect('myitems.db')
        # self.conn = mysql.connector.connect(
        #     host = 'localhost',
        #     user = 'root',
        #     passwd = 'qwert12345',
        #     database = 'myitems'
        # )
        self.curr = self.conn.cursor()

    def create_table(self):
        self.curr.execute("""DROP TABLE IF EXISTS quotes_tb""")
        self.curr.execute("""create table quotes_tb(
                        rank text,
                        name text,
                        country text,
                        industry text,
                        url text
                    )""")
    def process_item(self, item, spider):
        print('Pipeline :' + item['name'])
        self.store_db(item)
        return item

    def store_db(self,item):
        self.curr.execute("""insert into quotes_tb values (?,?,?,?,?)""",(
            item['rank'],
            item['name'],
            item['country'],
            item['industry'],
            item['url'],
        ))
        self.conn.commit()
