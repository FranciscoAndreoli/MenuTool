import json
import uuid
import os
class parsejson:
    def __init__(self):
        pass

    def slot_generateNewJSON(self, datos):

        def generate_UUID(): #Universally Unique Identifier
            return str(uuid.uuid4())

        def store_name(): #gets store name
            return datos['Name']

        my_dict = {
                "franchisorId": generate_UUID(),
                "id": generate_UUID(),
                "type": "Store",
                "name": store_name(),
                "notes": None,
                "categories": [],
                "modifiers": []
            }

        for section in datos['MenuSections']:
            new_category = {
                "id": generate_UUID(),
                "caption": section['Name'],
                "enabled": section['IsAvailable'],
                "notes": section["Description"],
                "items": [],
                "overrides": []
            }

            for item in section['MenuItems']:
                new_item = {
                    "caption": item['Name'],
                    "enabled": item['IsAvailable'],
                    "id": generate_UUID(),
                    "notes": item["Description"],
                    "overrides": [],
                    "pricingProfiles": [ {
                        "collectionPrice": item['Price'],
                        "collectionTax": 0,
                        "collectionTaxable": False,
                        "deliveryPrice": item['Price'],
                        "deliveryTax": 0,
                        "deliveryTaxable": False,
                        "dineInPrice": item['Price'],
                        "dineInTax": 0,
                        "dineInTaxable": False,
                        "priceBandId": 'cc4efdb0-78a1-11ed-a7b2-713c0ffdd9d3',
                        "takeawayPrice": item['Price'],
                        "takeawayTax": 0,
                        "takeawayTaxable": False
                    } ],
                    "modifierMembers": [],
                }

                for modifier in item['MenuItemOptionSets']:
                    new_menuOptionSet = {
                        "caption": modifier['Name'],
                        "enabled": True,
                        "modifierId": modifier['MenuItemOptionSetId'],
                        "overrides": []
                    }

                    new_item["modifierMembers"].append(new_menuOptionSet)

                new_category["items"].append(new_item)

            my_dict["categories"].append(new_category)

        for section in datos['MenuSections']:
            for item in section['MenuItems']:
                for optionSet in item['MenuItemOptionSets']:
                    new_optionSet = {
                        "canSameItemBeSelectedMultipleTimes": False,
                        "caption": optionSet['Name'],
                        "id": optionSet['MenuItemOptionSetId'],
                        "enabled": True,
                        "max": optionSet['MaxSelectCount'],
                        "min": optionSet['MinSelectCount'],
                        "position": optionSet['DisplayOrder'],
                        "overrides": [],
                        "items": []
                    }

                    for option in optionSet['MenuItemOptionSetItems']:
                        new_option = {
                            "caption": option['Name'],
                            "enabled": option['IsAvailable'],
                            "id": option['MenuItemOptionSetItemId'],
                            "overrides": [],
                            "pricingProfiles": [ {
                                "collectionPrice": option['Price'],
                                "collectionTax": 0,
                                "collectionTaxable": False,
                                "deliveryPrice": option['Price'],
                                "deliveryTax": 0,
                                "deliveryTaxable": False,
                                "dineInPrice": option['Price'],
                                "dineInTax": 0,
                                "dineInTaxable": False,
                                "priceBandId": 'cc4efdb0-78a1-11ed-a7b2-713c0ffdd9d3',
                                "takeawayPrice": option['Price'],
                                "takeawayTax": 0,
                                "takeawayTaxable": False
                            } ],
                            "modifierMembers": []
                        }

                        new_optionSet["items"].append(new_option)


                    my_dict["modifiers"].append(new_optionSet)

        #print(json.dumps(my_dict, indent=2))

        # specify the path to save the file, including the desired name
        path = os.path.expanduser("~/Desktop/my_POS_JSON.json")

        # open the file for writing, and save the dictionary as JSON
        with open(path, 'w') as outfile:
            json.dump(my_dict, outfile)