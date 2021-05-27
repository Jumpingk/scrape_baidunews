# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

# 建表语句
'''
CREATE TABLE baidunews_info(  
    id int NOT NULL primary key AUTO_INCREMENT comment 'primary key',
    title VARCHAR (100) COMMENT 'title',
    link VARCHAR (100) COMMENT 'link'
) AUTO_INCREMENT=1;
'''

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymysql


class BaidunewsPipeline:
    def process_item(self, item, spider):
        # content太大，只存储title和link
        conn = pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            passwd='766766',
            db='baidunews',
            use_unicode='True'
            # charset='utf-8'
        )
        cursor = conn.cursor()
        for i in range(0, len(item['title'])):
            title = item['title'][i]
            print(title)
            link = item['link']
            sql = f'insert into baidunews_info(title, link) values("{title}", "{link}")'
            # print(sql)
            try:
                cursor.execute(sql)
                conn.commit()
            except Exception as e:
                print('sql语句错误', e)
                conn.rollback()
        conn.close()
        return item
