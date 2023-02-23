import json
import uuid
import os

class parsejson:
    def __init__(self):
        pass

    def slot_generateNewJSON(self, datos):

        def generate_UUID(): #Universally Unique Identifier
            return str(uuid.uuid4())

        def name_section(): #gets menu section name
            for i in range(0, len(datos['MenuSections'])):
                yield datos['MenuSections'][i]['Name']

        def enable_section(): #gets if menu section is enabled or not
            for i in range(0, len(datos['MenuSections'])):
                yield datos['MenuSections'][i]['IsAvailable']

        def store_name(): #gets store name
            if datos["Name"] == None:
                return None
            else:
                return datos['Name']

        def notes_sections(): #gets description of menu sections
            for i in range(0, len(datos["MenuSections"])):
                if datos["MenuSections"][i]["Description"] == None or datos["MenuSections"][i]["Description"] == "":
                    yield None
                else:
                    yield datos["MenuSections"][i]["Description"]

        listNameSection = list(name_section())
        listEnableSections = list(enable_section())
        listNotes = list(notes_sections())


        my_dict = {
                    "franchisorId": generate_UUID(),
                    "id": generate_UUID(),
                    "type": "Store",
                    "name": store_name(),
                    "notes": None,
                    "categories": [

                    ],
                    "modifiers": []
                }


        for i in range(0, len(datos['MenuSections'])):
            new_category = {
                "id": "",
                "caption": "",
                "enabled": None,
                "backgroundColor": None,
                "foregroundColor": None,
                "selectedBackgroundColor": None,
                "selectedForegroundColor": None,
                "notes": None,
                "items": [],
                "overrides": []
            }

            new_category["id"] = generate_UUID()
            new_category["caption"] = listNameSection[i]
            new_category["enabled"] = listEnableSections[i]
            new_category["notes"] = listNotes[i]

            my_dict["categories"].append(new_category)

        #print(json.dumps(my_dict, indent=2))

        # specify the path to save the file, including the desired name
        path = os.path.expanduser("~/Desktop/my_POS_JSON.json")

        # open the file for writing, and save the dictionary as JSON
        with open(path, 'w') as outfile:
            json.dump(my_dict, outfile)


