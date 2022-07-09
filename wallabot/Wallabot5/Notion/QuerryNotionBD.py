import requests, json

def GetNotionUnicode(url):

  Wallabot5 = "https://api.notion.com/v1/databases/b398530f7e314a8d913d3d4a2fc4efe6/query"

  Filtre = {
      "filter": {
      "property": "url",
      "rich_text": { "equals": str(url) }
      }
  }

  token = 'secret_zHFKdJEJSvG9SzzUI7CucOXvaZ0ZCSy3oQIYhlHspTv'
  headers = {
      "Authorization": "Bearer " + token,
      "Content-Type": "application/json",
      "Notion-Version": "2021-08-16"
  }

  NotionId = requests.request("POST", Wallabot5, json=Filtre, headers=headers).json()["results"][0]["id"]   

  return(NotionId) 

def CreatePageNotion(Params):
	
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
    "item_title": {
      "id": "Jd%3Fe",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "item_images": {
      "id": "%3BQ_j",
      "type": "number",
      "number": 00
    },
    "seller_details": {
      "id": "M%40Vc",
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
      "type": "number",
      "number": 00
    },
    "item_description": {
      "id": "%60KF%5B",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "item_price": {
      "id": "%7CZ%3BM",
      "type": "number",
      "number": 00
    },
    "url": {
      "id": "title",
      "type": "title",
      "title": [{ "text": {"content": ""}}]
    }
  }
    }
    
    url = 'https://api.notion.com/v1/pages'
     
    JsonBody["parent"]["database_id"] = "b398530f7e314a8d913d3d4a2fc4efe6"
    JsonBody["properties"]["item_title"]["rich_text"][0]["text"]["content"] = Params["item_title"]
    JsonBody["properties"]["item_images"]["number"] = Params["item_images"]
    JsonBody["properties"]["seller_details"]["rich_text"][0]["text"]["content"] = Params["seller_details"]
    JsonBody["properties"]["distance"]["number"] = Params["distance"]
    JsonBody["properties"]["modification_date"]["number"] = Params["modification_date"]
    JsonBody["properties"]["item_description"]["rich_text"][0]["text"]["content"] = Params["item_description"]
    JsonBody["properties"]["item_price"]["number"] = Params["item_price"]
    JsonBody["properties"]["url"]["title"][0]["text"]["content"] = Params["url"]

    res = requests.request("POST", url, headers=headers, data=json.dumps(JsonBody))
    print(res.text)
def UpdatePageNotion(page_id,Params):

	
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
    "item_title": {
      "id": "Jd%3Fe",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "item_images": {
      "id": "%3BQ_j",
      "type": "number",
      "number": 00
    },
    "seller_details": {
      "id": "M%40Vc",
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
      "type": "number",
      "number": 00
    },
    "item_description": {
      "id": "%60KF%5B",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "item_price": {
      "id": "%7CZ%3BM",
      "type": "number",
      "number": 00
    },
    "url": {
      "id": "title",
      "type": "title",
      "title": [{ "text": {"content": ""}}]
    }
  }
    }

    url = 'https://api.notion.com/v1/pages/'+page_id
     
    JsonBody["parent"]["database_id"] = "b398530f7e314a8d913d3d4a2fc4efe6"
    JsonBody["properties"]["item_title"]["rich_text"][0]["text"]["content"] = Params["item_title"]
    JsonBody["properties"]["item_images"]["number"] = Params["item_images"]
    JsonBody["properties"]["seller_details"]["rich_text"][0]["text"]["content"] = Params["seller_details"]
    JsonBody["properties"]["distance"]["number"] = Params["distance"]
    JsonBody["properties"]["modification_date"]["number"] = Params["modification_date"]
    JsonBody["properties"]["item_description"]["rich_text"][0]["text"]["content"] = Params["item_description"]
    JsonBody["properties"]["item_price"]["number"] = Params["item_price"]
    JsonBody["properties"]["url"]["title"][0]["text"]["content"] = Params["url"]

    res = requests.request("PATCH", url, headers=headers, data=json.dumps(JsonBody))
    return (res)

aaaaaaa = GetNotionUnicode("sss")
print(aaaaaaa)

token = 'secret_zHFKdJEJSvG9SzzUI7CucOXvaZ0ZCSy3oQIYhlHspTv'
page_id = aaaaaaa
url = "https://api.notion.com/v1/pages/"+page_id
headers = {
    "Authorization": "Bearer " + token,
    "Content-Type": "application/json",
    "Notion-Version": "2021-08-16"
}

response = requests.request("GET", url, headers=headers)

print(response.text)
# Params = {
# 	"item_title": "pimmaa",
# 	"item_images": 1111,
# 	"seller_details": "bbb",
# 	"distance": 2222,
# 	"modification_date": 3333,
# 	"item_description": "ccc",
# 	"item_price": 4444,
# 	"url": "Adeuuu",
# 	}
# xxx = CreatePageNotion(Params)

# print(xxx)

# UpdatePageNotion("9a6467a3-1902-496d-baa6-87499bb8c2e7",Params)