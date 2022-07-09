import json
import boto3
import requests
import time
insert = json.load(open('insert.json'))
modify = json.load(open('modify.json'))
remove = json.load(open('remove.json'))


def GetNotionUnicode(url):
  CidoDBurl = "https://api.notion.com/v1/databases/871618b2bf704cb1a751a04c7959e668/query"

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

  NotionId = requests.request("POST", CidoDBurl, json=Filtre, headers=headers).json()["results"][0]["id"]   

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
    "SistemaSeleccio": {
      "id": "%3Ajx%7C",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "WebTerminiObert": {
      "id": "%3DIbV",
      "type": "number",
      "number": 00
    },
    "Materia": {
      "id": "DEmB",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "DocsAdjunts": {
      "id": "GHSq",
      "type": "number",
      "number": 00
    },
    "WebNoConvocat": {
      "id": "QkPi",
      "type": "number",
      "number": 00
    },
    "Titulacio": {
      "id": "TOP%3A",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "Termini": {
      "id": "TUwe",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "Contracte": {
      "id": "%5EVO%60",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "Plasa": {
      "id": "blMk",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "AltresRequisits": {
      "id": "dsmm",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "Observacions": {
      "id": "n%3CB%7D",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "Organ": {
      "id": "ymEl",
      "type": "rich_text",
      "rich_text": [{ "text": {"content": ""}}]
    },
    "Control": {
      "id": "%7BNfp",
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
     
    JsonBody["parent"]["database_id"] = "871618b2bf704cb1a751a04c7959e668"
    JsonBody["properties"]["SistemaSeleccio"]["rich_text"][0]["text"]["content"] = Params["SistemaSeleccio"]
    JsonBody["properties"]["WebTerminiObert"]["number"] = Params["WebTerminiObert"]
    JsonBody["properties"]["Materia"]["rich_text"][0]["text"]["content"] = Params["Materia"]
    JsonBody["properties"]["DocsAdjunts"]["number"] = Params["DocsAdjunts"]
    JsonBody["properties"]["WebNoConvocat"]["number"] = Params["WebNoConvocat"]
    JsonBody["properties"]["Titulacio"]["rich_text"][0]["text"]["content"] = Params["Titulacio"]
    JsonBody["properties"]["Termini"]["rich_text"][0]["text"]["content"] = Params["Termini"]
    JsonBody["properties"]["Contracte"]["rich_text"][0]["text"]["content"] = Params["Contracte"]
    JsonBody["properties"]["Plasa"]["rich_text"][0]["text"]["content"] = Params["Plasa"]
    JsonBody["properties"]["AltresRequisits"]["rich_text"][0]["text"]["content"] = Params["AltresRequisits"]
    JsonBody["properties"]["Observacions"]["rich_text"][0]["text"]["content"] = Params["Observacions"]
    JsonBody["properties"]["Organ"]["rich_text"][0]["text"]["content"] = Params["Organ"]
    JsonBody["properties"]["Control"]["number"] = Params["Control"]
    JsonBody["properties"]["url"]["title"][0]["text"]["content"] = Params["url"]

    res = requests.request("POST", url, headers=headers, data=json.dumps(JsonBody))

def lambda_handler(event, context):
	print('------------------------')
	# print(event)
	#1. Iterate over each record
	try:
		for record in event['Records']:
			#2. Handle event by type
			if record['eventName'] == 'INSERT':
				handle_insert(record)
			elif record['eventName'] == 'MODIFY':
				handle_modify(record)
			elif record['eventName'] == 'REMOVE':
				handle_remove(record)
		print('------------------------')
		return "Success!"
	except Exception as e:
		print("Exception= ",e)
		print('------------------------')
		return "Error"

def handle_insert(record):
	print("Handling INSERT Event")

	#3a. Get newImage content
	newImage = record['dynamodb']['NewImage']

	#3b. Parse values
	url = newImage["url"]["S"]
	Plasa = newImage["Plasa"]["S"]

	#3c. Print it
	print ("New row added with url= "+str(url)+"    and   plasa= "+str(Plasa))
	print("Done handling INSERT Event")

	#3d. Create entry in Notion
	Params = {
	"SistemaSeleccio": "",
	"WebTerminiObert": 9999,
	"Materia": "",
	"DocsAdjunts": 9999,
	"WebNoConvocat": 9999,
	"Titulacio": "",
	"Termini": "",
	"Contracte": "",
	"Plasa": str(Plasa),
	"AltresRequisits": "",
	"Observacions": "",
	"Organ": "",
	"Control": 9999,
	"url": str(url)
	}
	
	CreatePageNotion(Params)

	#3e. Add item to Bridge_Notion_Dynamo
	Bridge_Notion_Dynamo = boto3.resource('dynamodb').Table('Bridge_Notion_Dynamo')	
	Item = {}
	Item["url"] = str(url)
	Item["NotionId"] = GetNotionUnicode(url)
	Bridge_Notion_Dynamo.put_item(Item=Item)

def handle_modify(record):
	print("Handling MODIFY Event")

	#3a. Parse oldImage and score
	oldImage = record['dynamodb']['OldImage']
	oldWebTerminiObert = oldImage["WebTerminiObert"]["N"]
	oldTermini = oldImage["Termini"]["S"]
	oldPlasa = oldImage["Plasa"]["S"]
	oldContracte = oldImage["Contracte"]["S"]
	oldurl = oldImage["url"]["S"]
	oldAltresRequisits = oldImage["AltresRequisits"]["S"]
	oldSistemaSeleccio = oldImage["SistemaSeleccio"]["S"]
	oldWebNoConvocat = oldImage["WebNoConvocat"]["N"]
	oldControl = oldImage["Control"]["N"]
	oldTitulacio = oldImage["Titulacio"]["S"]
	oldMateria = oldImage["Materia"]["S"]
	oldObservacions = oldImage["Observacions"]["S"]
	oldDocsAdjunts = oldImage["DocsAdjunts"]["N"]
	oldOrgan = oldImage["Organ"]["S"]

	#3b. Parse oldImage and score
	newImage = record['dynamodb']['NewImage']
	newWebTerminiObert = newImage["WebTerminiObert"]["N"]
	newTermini = newImage["Termini"]["S"]
	newPlasa = newImage["Plasa"]["S"]
	newContracte = newImage["Contracte"]["S"]
	newurl = newImage["url"]["S"]
	newAltresRequisits = newImage["AltresRequisits"]["S"]
	newSistemaSeleccio = newImage["SistemaSeleccio"]["S"]
	newWebNoConvocat = newImage["WebNoConvocat"]["N"]
	newControl = newImage["Control"]["N"]
	newTitulacio = newImage["Titulacio"]["S"]
	newMateria = newImage["Materia"]["S"]
	newObservacions = newImage["Observacions"]["S"]
	newDocsAdjunts = newImage["DocsAdjunts"]["N"]
	newOrgan = newImage["Organ"]["S"]

	#3c. Check for change
	if oldWebTerminiObert != newWebTerminiObert:
		print('oldWebTerminiObert=' + str(oldWebTerminiObert) + ', newWebTerminiObert=' + str(newWebTerminiObert))
	if oldTermini != newTermini:
		print('oldTermini=' + str(oldTermini) + ', newTermini=' + str(newTermini))
	if oldPlasa != newPlasa:
		print('oldPlasa=' + str(oldPlasa) + ', newPlasa=' + str(newPlasa))
	if oldContracte != newContracte:
		print('oldContracte=' + str(oldContracte) + ', newContracte=' + str(newContracte))
	if oldurl != newurl:
		print('oldurl=' + str(oldurl) + ', newurl=' + str(newurl))
	if oldAltresRequisits != newAltresRequisits:
		print('oldAltresRequisits=' + str(oldAltresRequisits) + ', newAltresRequisits=' + str(newAltresRequisits))
	if oldSistemaSeleccio != newSistemaSeleccio:
		print('oldSistemaSeleccio=' + str(oldSistemaSeleccio) + ', newSistemaSeleccio=' + str(newSistemaSeleccio))
	if oldWebNoConvocat != newWebNoConvocat:
		print('oldWebNoConvocat=' + str(oldWebNoConvocat) + ', newWebNoConvocat=' + str(newWebNoConvocat))
	if oldControl != newControl:
		print('oldControl=' + str(oldControl) + ', newControl=' + str(newControl))
	if oldTitulacio != newTitulacio:
		print('oldTitulacio=' + str(oldTitulacio) + ', newTitulacio=' + str(newTitulacio))
	if oldMateria != newMateria:
		print('oldMateria=' + str(oldMateria) + ', newMateria=' + str(newMateria))
	if oldObservacions != newObservacions:
		print('oldObservacions=' + str(oldObservacions) + ', newObservacions=' + str(newObservacions))
	if oldDocsAdjunts != newDocsAdjunts:
		print('oldDocsAdjunts=' + str(oldDocsAdjunts) + ', newDocsAdjunts=' + str(newDocsAdjunts))
	if oldOrgan != newOrgan:
		print('oldOrgan=' + str(oldOrgan) + ', newOrgan=' + str(newOrgan))

	print("Done handling MODIFY Event")

def handle_remove(record):
	print("Handling REMOVE Event")

	#3a. Parse oldImage
	oldImage = record['dynamodb']['OldImage']

	#3b. Parse values
	oldurl = oldImage["url"]["S"]
	oldPlasa = oldImage["Plasa"]["S"]

	#3c. Print it
	print ("Row removed with url= "+str(oldurl)+"    and   plasa= "+str(oldPlasa))

	print("Done handling REMOVE Event")

lambda_handler(insert,"")
