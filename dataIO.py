import json

def readGPIOMapping():
  with open('data/GPIO_Mapping.json', 'r' ) as inFile:
    json_object = json.load(inFile)
    print(json_object)
    return json_object

def saveGPIOMapping(dictionary):
  json_string = json.dumps(dictionary, indent=4)
   # Writing to sample.json
  with open("data/GPIO_Mapping.json", "w") as outFile:
    outFile.write(json_string)