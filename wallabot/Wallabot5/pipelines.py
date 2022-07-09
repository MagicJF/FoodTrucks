# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3, requests, json
from pymongo import MongoClient
from pymongo import ReturnDocument



class WallabotV4Sqlite3:
    def __init__(self):
        self.con = sqlite3.connect('Results/EmptyDatabase.db')
        self.cur = self.con.cursor()
        self.create_table()

    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS products
                        (
                            ItemUrl text PRIMARY KEY, 
                            item_title text, 
                            item_price real, 
                            item_distance real, 
                            item_web_slug text, 
                            item_description text,
                            item_modification_date text,
                            item_images real,
                            seller_details text
                            )""")

    def process_item(self, item, spider):

        self.cur.execute("INSERT OR IGNORE INTO products VALUES (:ItemUrl, :item_title, :item_price, :distance, :web_slug, :item_description, :modification_date, :item_images, :seller_details)", 
        {
            'ItemUrl': item['ItemUrl'], 
            'item_title': item['item_title'], 
            'item_price': item['item_price'],
            'distance': item['distance'],
            'web_slug': item['web_slug'],
            'item_description': item['item_description'],
            'modification_date': item['modification_date'],
            'item_images': item["item_images"],
            'seller_details': str(item['seller_details'])
            })
        
        self.con.commit()

        return item


class MongoPipeline:
    def __init__(self):
        client = MongoClient( 
                'mongo',
                port = 27017)

        self.db=client['wallabot5']
        self.col = self.db['ScrapedItems']

    def process_item(self, item, spider):
        res = self.col.find_one_and_update(
            {   "_id": item["ItemUrl"],
                "item_title": item["item_title"],
                "item_price": item["item_price"],
                "distance": item["distance"],
                "web_slug": item["web_slug"],
                "item_description": item["item_description"],
                "modification_date": item["modification_date"],
                "item_images": item["item_images"]},
            {'$set': {
                "item_title": item["item_title"],
                "item_price": item["item_price"],
                "distance": item["distance"],
                "web_slug": item["web_slug"],
                "item_description": item["item_description"],
                "modification_date": item["modification_date"],
                "item_images": item["item_images"],
                "seller_details": item["seller_details"]}},
            upsert=False)

        if res is None:
            print("<<<<>>>>")            
            print("DOTHIS, update or insert")
            print("joooan")
            print("<<<<>>>>")
            self.col.find_one_and_update(
                        {'_id': item['ItemUrl']},
                        {'$set': {
                            "item_title": item['item_title'],
                            "item_price": item['item_price'],
                            "distance": item['distance'],
                            "web_slug": item['web_slug'],
                            "item_description": item['item_description'],
                            "modification_date": item['modification_date'],
                            "item_images": item["item_images"],
                            "seller_details": item['seller_details']}},
                        upsert=True)
            Params = {
                "title": item['item_title'],
                "images": item["item_images"],
                "Ssales": item['seller_details']["user_sales"],
                "Srating": item['seller_details']["user_rating"],
                "SreportedTimes": item['seller_details']["user_reportedTimes"],
                "Skind": item['seller_details']["user_kind"],
                "SRedFlag": item['seller_details']["user_RedFlag"],
                "distance": item['distance'],
                "modification_date": item['modification_date'],
                "description": item['item_description'],
                "price": item['item_price'],
                "url": item['ItemUrl'],
                }
            self.CreatePageNotion(Params)

        return item

    def CreatePageNotion(self,Params):
      
        token = 'secret_zHFKdJEJSvG9SzzUI7CucOXvaZ0ZCSy3oQIYhlHspTv'
        headers = {
            "Authorization": "Bearer " + token,
            "Content-Type": "application/json",
            "Notion-Version": "2021-08-16"
        }
        JsonBody = {
      "object": "page",
      "parent": {
        "type": "database_id",
        "database_id": ""
      },
      "properties": {
        "title.": {
          "id": "Jd%3Fe",
          "type": "rich_text",
          "rich_text": [{ "text": {"content": ""}}]
        },
        "images": {
          "id": "%3BQ_j",
          "type": "number",
          "number": 00
        },
        "Ssales": {
          "id": "M%40Vc",
          "type": "number",
          "number": 00
        },
        "Srating": {
          "id": "QDrs",
          "type": "number",
          "number": 00
        },
        "SreportedTimes": {
          "id": "w%5BZz",
          "type": "number",
          "number": 00
        },
        "SRedFlag": {
          "id": "%3BQ_j",
          "type": "rich_text",
          "rich_text": [{ "text": {"content": ""}}]
        },
        "Skind": {
          "id": "J%7BpE",
          "type": "rich_text",
          "rich_text": [{ "text": {"content": ""}}]
        },
        "distance": {
          "id": "%7Buso",
          "type": "number",
          "number": 00
        },
        "modification_date": {
          "id": "%7CGFa",
          "type": "date",
          "date": {"start": ""}
        },
        "description": {
          "id": "%60KF%5B",
          "type": "rich_text",
          "rich_text": [{ "text": {"content": ""}}]
        },
        "price": {
          "id": "%7CZ%3BM",
          "type": "number",
          "number": 00
        },
        "link": { 
          "id": "uWyZ", 
          "type": "url", 
          "url": "" },

        "url": {
          "id": "title",
          "type": "title",
          "title": [{ "text": {"content": ""}}]
        }
      }
        }
        
        url = 'https://api.notion.com/v1/pages'
        
        JsonBody["parent"]["database_id"] = "b398530f7e314a8d913d3d4a2fc4efe6"
        JsonBody["properties"]["title."]["rich_text"][0]["text"]["content"] = Params["title"]
        JsonBody["properties"]["images"]["number"] = Params["images"]

        JsonBody["properties"]["distance"]["number"] = Params["distance"]
        JsonBody["properties"]["modification_date"]["date"]["start"] = Params["modification_date"]
        JsonBody["properties"]["description"]["rich_text"][0]["text"]["content"] = Params["description"]
        JsonBody["properties"]["price"]["number"] = Params["price"]
        JsonBody["properties"]["url"]["title"][0]["text"]["content"] = Params["url"]

        JsonBody["properties"]["Ssales"]["number"] = Params["Ssales"]
        JsonBody["properties"]["Srating"]["number"] = Params["Srating"]
        JsonBody["properties"]["SreportedTimes"]["number"] = Params["SreportedTimes"]
        JsonBody["properties"]["Skind"]["rich_text"][0]["text"]["content"] = Params["Skind"]
        JsonBody["properties"]["SRedFlag"]["rich_text"][0]["text"]["content"] = Params["SRedFlag"]

        JsonBody["properties"]["link"]["url"] = Params["url"]

        res = requests.request("POST", url, headers=headers, data=json.dumps(JsonBody))
        print(res.text)


    


