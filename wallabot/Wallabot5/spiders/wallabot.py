import scrapy
import requests, json
from Wallabot5.items import Wallabot5Item
from scrapy.loader import ItemLoader
from datetime import datetime

class WallabotSpider(scrapy.Spider):
    name = 'wallabot'
    def start_requests(self):
        Categories = {"Informatica": "15000", "Coches": "100"}
        print("pimm")
        print("Adeuuu")


        MinPrice = 144
        MaxPrice = 150
        KeyWord = "nuc i5"
        Categoria = Categories["Informatica"]

        KeyWords = KeyWord.replace(" ","+")
        start = 0
        url = "https://api.wallapop.com/api/v3/general/search?min_sale_price="+str(MinPrice)+"&user_province=Barcelona&keywords="+KeyWords+"&latitude=41.57978&start="+str(start)+"&user_region=Cataluña&user_city=Igualada&search_id=2907ad3d-2c42-4601-a1ea-13ac6aca324e&country_code=ES&items_count=0&density_type=20&filters_source=default_filters&max_sale_price="+str(MaxPrice)+"&category_ids="+str(Categoria)+"&order_by=price_low_to_high&step=0&longitude=1.61565"

        print("")
        print("")
        print(url)
        print("")
        print("")



        meta={
            "MinPrice": MinPrice,
            "MaxPrice": MaxPrice,
            "KeyWords": KeyWords,
            "Categoria": Categoria,
            "start": start
            }

        yield scrapy.Request (url=url, callback=self.parse, meta=meta)

    def ConvertTimestamp(self,ts):
        ts = int(ts[:-3])
        return(datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d'))

    def parse(self, response):
        
        MinPrice = response.meta.get('MinPrice')
        KeyWords = response.meta.get('KeyWords')
        start = int(response.meta.get('start'))+25
        MaxPrice = response.meta.get('MaxPrice')
        Categoria = response.meta.get('Categoria')        

        res = response.css('body').css('p::text').get()
        resJson = json.loads(res)

        if len(resJson["search_objects"]) == 0:
            print("FINISHEDD")
        else:
            try:
                for item in resJson["search_objects"]:
                    itemLimpio = Wallabot5Item()
                    user_RedFlag="OK"
                    seller_details = {
                        "user_sales": "",
                        "user_rating": "",
                        "user_reportedTimes": "",
                        "user_kind": "",
                        "item_images": ""
                    }
                
                    Userid = item["user"]["id"]
                    url_userinfo = "https://api.wallapop.com/api/v3/users/"+Userid+"/stats"                    
                    response = requests.get(url_userinfo).json()
                    score = response["ratings"][0]["value"]    
                    reviews = response["counters"][3]["value"]   
                    reportedTimes = response["counters"][-1]["value"]

                    seller_details["user_sales"] = reviews
                    seller_details["user_rating"] = score
                    seller_details["user_reportedTimes"] = reportedTimes
                    seller_details["user_kind"] = item["user"]["kind"]   
                            
                    if int(seller_details["user_sales"]) <= 1:
                        user_RedFlag = "DANGER"
                    seller_details["user_RedFlag"] = user_RedFlag

                    ItemUrl = "https://es.wallapop.com/item/"+str(item["web_slug"])

                    item_title = item["title"]  
                    item_price = item["price"]                                      
                    distance = item["distance"]
                    web_slug = item["web_slug"]    
                    item_description = item["description"]   
                    modification_date = item["modification_date"]   
                    item_images = len(item["images"])                                                                      
                    seller_details = seller_details

                    itemLimpio["ItemUrl"]= ItemUrl
                    itemLimpio["item_title"]= item_title
                    itemLimpio["item_price"]= int(round(item_price))
                    itemLimpio["distance"]= distance
                    itemLimpio["web_slug"]= web_slug
                    itemLimpio["item_description"]= item_description
                    itemLimpio["modification_date"]= self.ConvertTimestamp(str(modification_date))
                    itemLimpio["item_images"]= item_images
                    itemLimpio["seller_details"]= seller_details

                    yield itemLimpio

            except Exception as e:
                print("ERRRRRRROOORRR=",e)
                pass

            url = "https://api.wallapop.com/api/v3/general/search?min_sale_price="+str(MinPrice)+"&user_province=Barcelona&keywords="+KeyWords+"&latitude=41.57978&start="+str(start)+"&user_region=Cataluña&user_city=Igualada&search_id=2907ad3d-2c42-4601-a1ea-13ac6aca324e&country_code=ES&items_count=0&density_type=20&filters_source=default_filters&max_sale_price="+str(MaxPrice)+"&category_ids="+str(Categoria)+"&order_by=price_low_to_high&step=0&longitude=1.61565"           
            meta={
            "MinPrice": MinPrice,
            "MaxPrice": MaxPrice,
            "KeyWords": KeyWords,
            "Categoria": Categoria,
            "start": start
            }            
            print("")
            print("YYYYYYYYyYielding Next url")

            yield scrapy.Request(url, callback = self.parse, meta=meta)
        pass