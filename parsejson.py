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
        
                    def getMoPrices(optionSet):
                        new_moPrices = []
        
                        if optionSet['IsMasterOptionSet'] == True:
                            for moPrices in optionSet['MenuItemOptionSetItems']:
                                new_moPrices.append(moPrices['Price'])
        
                        return new_moPrices
        
                    listMasterOptionPrices = getMoPrices(optionSet)
        
                    if listMasterOptionPrices:
                        print('antes de filtrar', listMasterOptionPrices)
                        lowestPrice =  min(listMasterOptionPrices)
                        print('el mas bajo', lowestPrice)
        
                        for priceDifference in listMasterOptionPrices:
                            newPrices = priceDifference - lowestPrice
                            print('nuevo precio', newPrices)
        
                    for option in optionSet['MenuItemOptionSetItems']:
        
                        taxValue = get_tax(option["TaxRateId"])
                        booleano = False if option["TaxRateId"] is None else True
        
                        new_option = {
                            "caption": option['Name'],
                            "enabled": option['IsAvailable'],
                            "id": option['MenuItemOptionSetItemId'],
                            "overrides": [],
                            "pricingProfiles": [ {
                                "collectionPrice": option['Price'],
                                "collectionTax": taxValue,
                                "collectionTaxable": booleano,
                                "deliveryPrice": option['Price'],
                                "deliveryTax": taxValue,
                                "deliveryTaxable": booleano,
                                "dineInPrice": option['Price'],
                                "dineInTax": taxValue,
                                "dineInTaxable": booleano,
                                "priceBandId": "cc4efdb0-78a1-11ed-a7b2-713c0ffdd9d3",
                                "takeawayPrice": option['Price'],
                                "takeawayTax": taxValue,
                                "takeawayTaxable": booleano
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