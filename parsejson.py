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

        def get_tax(TaxRateId):
            if TaxRateId == None:
                return 0
            elif TaxRateId in tax_dict:
                return tax_dict[TaxRateId]


        if len(datos["TaxRates"]) != 0:
            tax_dict = {tax_rate["TaxRateId"]: tax_rate["Rate"] for tax_rate in datos["TaxRates"]}
            print(tax_dict)
            # Output example: {
            #                   20505431: 5,
            #                   20505432: 6,
            #                   20505422: 7
            #                 }
        else:
            pass

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

                taxValue = get_tax(item["TaxRateId"])
                booleano = False if item["TaxRateId"] is None else True

                new_item = {
                    "caption": item['Name'],
                    "enabled": item['IsAvailable'],
                    "id": generate_UUID(),
                    "notes": item["Description"],
                    "overrides": [],
                    "pricingProfiles": [ {
                        "collectionPrice": item['Price'],
                        "collectionTax": taxValue,
                        "collectionTaxable": booleano,
                        "deliveryPrice": item['Price'],
                        "deliveryTax": taxValue,
                        "deliveryTaxable": booleano,
                        "dineInPrice": item['Price'],
                        "dineInTax": taxValue,
                        "dineInTaxable": booleano,
                        "priceBandId": "cc4efdb0-78a1-11ed-a7b2-713c0ffdd9d3",
                        "takeawayPrice": item['Price'],
                        "takeawayTax": taxValue,
                        "takeawayTaxable": booleano
                    }],
                        "modifierMembers": [],
                }

                new_category["items"].append(new_item)

            my_dict["categories"].append(new_category)

        print(json.dumps(my_dict, indent=2))

        # specify the path to save the file, including the desired name
        path = os.path.expanduser("~/Desktop/my_POS_JSON.json")

        # open the file for writing, and save the dictionary as JSON
        with open(path, 'w') as outfile:
            json.dump(my_dict, outfile)




