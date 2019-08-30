import json
import urllib.request

def fetchDocument(page):
    url = "https://www.booli.se/slutpriser/ostra+goteborg/115308/?objectType=L%C3%A4genhet&page=" + str(page)
    with urllib.request.urlopen(url) as response:
        document = response.read()
    return str(document, 'utf-8')

def extractJson(document):
    startPattern = 'window.viewParameters = '
    endPattern = '\n\t\t</script>'

    return document.split(startPattern,1)[1].split(endPattern,1)[0]

def anotherPageExists(data, page):
    return page == 1 or data["pagination"]["numberOfHits"] != data["pagination"]["showingHitsTo"]

def createEntities(data):
    entities = []
    for entity in data["soldProperties"]:
        newEntity = {}
        newEntity["longitude"] = entity["longitude"] 
        newEntity["latitude"] = entity["latitude"]
        newEntity["livingArea"] = entity["livingArea"]["raw"]
        newEntity["date"] = entity["soldDate"]["raw"][:-10]
        newEntity["price"] = entity["soldPrice"]["raw"]
        entities.append(newEntity)
    return entities

def entitiesToCsv(entities):
    csv = ""
    # Create headers
    for key in entities[0]:
        csv += key+ ","

    csv = csv[:-1]
    csv += "\n"
    for entity in entities:
        for key, value in entity.items():
            csv += str(value) + ","
        csv = csv[:-1]
        csv += "\n"
    return csv

def main():
    page = 1
    f = open("data.csv", "a")
    data = {}
    entities = []
    while anotherPageExists(data, page):
        document = fetchDocument(page)
        rawJson = extractJson(document)
        data = json.loads(rawJson)
        entities += createEntities(data)
        page += 1
    

    csvData = entitiesToCsv(entities)
    f.write(csvData)

main()