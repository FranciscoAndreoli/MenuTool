import json
import uuid
import os
from datetime import datetime, timedelta

class parsejson:
    def __init__(self):
        pass

    def slot_generateNewJSON(self, datos): 

        def generate_UUID():
            '''Returns a Universally Unique Identifier'''
            return str(uuid.uuid4())

        def store_name():
            '''Returns the name of the store'''
            return datos['Name']

        def get_tax(TaxRateId):
            '''Returns the tax value of an item for a given TaxRateId'''
            if TaxRateId == None:
                return 0
            elif TaxRateId in tax_rates_dict():
                return tax_rates_dict()[TaxRateId]


        def tax_rates_dict():
            '''Returns a dictionary with the tax rates of the menu'''
            if len(datos["TaxRates"]) != 0:
                tax_dict = {tax_rate["TaxRateId"]: tax_rate["Rate"] for tax_rate in datos["TaxRates"]}
                #print(tax_dict)
                return tax_dict
            else:
                return {} #empty dictionary


        def get_mo_prices(optionSet):
            '''Returns a list with the prices of the Master Options of an item'''
            priceList = []
            for price in optionSet['MenuItemOptionSetItems']:
                priceList.append(price['Price'])

            minimumPrice = min(priceList)
            priceList = [x - minimumPrice for x in priceList]
            PriceList =  [float(str(x)[:4]) for x in priceList] #shorten the number of decimal places to two
            #print (roundedPriceList)
            return PriceList

        def get_image(imageId):
            '''Returns the URL of the image of an item'''
            if imageId == None:
                return None
            else:
                image = item["ImageUrl"]
                resizedImage = "{}?w={}&h={}".format(image, 225, 255) #resize image to 225x255
                return resizedImage

        def get_time_settings(section):
            timeOptions = section['MenuSectionAvailability']['AvailableTimes']
            return timeOptions





        myDict = {
                "franchisorId": generate_UUID(),
                "id": generate_UUID(),
                "type": "Store",
                "name": store_name(),
                "notes": None,
                "categories": [],
                "modifiers": []
            }

        for section in datos['MenuSections']:
            newCategory = {
                "id": generate_UUID(),
                "caption": section['Name'],
                "enabled": section['IsAvailable'],
                "notes": section["Description"],
                "overrides": [],
                "items": []
            }

            for item in section['MenuItems']:

                taxValue = get_tax(item["TaxRateId"]) #item["TaxRateId"] is the tax id for the item
                booleano = False if item["TaxRateId"] is None else True

                newItem = {
                    "caption": item['Name'],
                    "enabled": item['IsAvailable'],
                    "id": generate_UUID(),
                    "notes": item["Description"],
                    "imageUrl": get_image(item["ImageUrl"]),
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
                        "priceBandId": 'cc4efdb0-78a1-11ed-a7b2-713c0ffdd9d3',
                        "takeawayPrice": item['Price'],
                        "takeawayTax": taxValue,
                        "takeawayTaxable": booleano
                    } ],
                    "modifierMembers": [],
                }

                
                for masterOption in item["MenuItemOptionSets"]:
                    if masterOption["IsMasterOptionSet"] == True:
                        # if item have a master option, its price will be the minimum price of the master option.
                        newItem["pricingProfiles"][0]["collectionPrice"] = masterOption["MinPrice"]
                        newItem["pricingProfiles"][0]["deliveryPrice"] = masterOption["MinPrice"]
                        newItem["pricingProfiles"][0]["dineInPrice"] = masterOption["MinPrice"]
                        newItem["pricingProfiles"][0]["takeawayPrice"] = masterOption["MinPrice"]

                newCategory["items"].append(newItem)

                for modifier in item['MenuItemOptionSets']:

                    new_menuOptionSet = {
                        "caption": modifier['Name'],
                        "enabled": True,
                        "modifierId": modifier['MenuItemOptionSetId'],
                        "overrides": []
                    }
                    newItem["modifierMembers"].append(new_menuOptionSet)

                for optionSet in item['MenuItemOptionSets']:

                    isMasterOption = optionSet['IsMasterOptionSet'] == True and len(optionSet['MenuItemOptionSetItems']) != 0

                    newOptionSet = { # modifiers
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

                    for index, item in enumerate(optionSet['MenuItemOptionSetItems']):

                        taxValue = get_tax(item["TaxRateId"]) #item["TaxRateId"] is the tax id for the item
                        booleano = False if item["TaxRateId"] is None else True

                        newItemInOptionSet = { # items inside modifiers
                            "caption": item['Name'],
                            "enabled": item['IsAvailable'],
                            "id": item['MenuItemOptionSetItemId'],
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
                                "priceBandId": 'cc4efdb0-78a1-11ed-a7b2-713c0ffdd9d3',
                                "takeawayPrice": item['Price'],
                                "takeawayTax": taxValue,
                                "takeawayTaxable": booleano
                            } ],
                            "modifierMembers": []
                        }

                        if isMasterOption:
                            
                            priceList = get_mo_prices(optionSet)

                            newItemInOptionSet['pricingProfiles'][0]['collectionPrice'] = priceList[index]
                            newItemInOptionSet['pricingProfiles'][0]['deliveryPrice'] = priceList[index]
                            newItemInOptionSet['pricingProfiles'][0]['dineInPrice'] = priceList[index]
                            newItemInOptionSet['pricingProfiles'][0]['takeawayPrice'] = priceList[index]

                        newOptionSet["items"].append(newItemInOptionSet)

                    if isMasterOption:

                        newOptionSet['max'] = 1
                        newOptionSet['min'] = 1
                        newOptionSet['position'] = -1
                        
                    myDict["modifiers"].append(newOptionSet)
                
            timeAvailability = get_time_settings(section)

            for times in timeAvailability:
                
                weekDayMapper = {
                    0: "sundayEnabled",
                    1: "mondayEnabled",
                    2: "tuesdayEnabled",
                    3: "wednesdayEnable",
                    4: "thursdayEnable",
                    5: "fridayEnable",
                    6: "saturdayEnable"
                }

                weekDayKey = weekDayMapper[times['DayOfWeek']]

                dayAvailability = False
                
                if times['StartTime'] != "01:00:00" and times['Period'] != "23:00:00":
                    dayAvailability = True
                
                if dayAvailability == False:
                    continue

                timeString = times['StartTime']
                timeNumber = datetime.strptime(timeString, "%H:%M:%S")

                periodString = times['Period']
                periodNumber = datetime.strptime(periodString, "%H:%M:%S")

                sumTime = timeNumber + timedelta(hours=periodNumber.hour, minutes=periodNumber.minute, seconds=periodNumber.second)
                
                sumTimeString = sumTime.strftime("%H:%M:%S")


                newTimeSettingOptions = {
                    "id": generate_UUID(),
                    "paramsJson": {
                        "caption": section['Name'],
                        weekDayKey: dayAvailability,
                        "fromTime": times['StartTime'],
                        "toTime": sumTimeString,
                        "type": "generic"
                    }
                }

                newCategory['overrides'].append(newTimeSettingOptions)


            myDict["categories"].append(newCategory)

        #print(json.dumps(my_dict, indent=2))

        # specify the path to save the file, including the desired name
        path = os.path.expanduser("~/Desktop/my_POS_JSON.json")

        # open the file for writing, and save the dictionary as JSON
        with open(path, 'w') as outfile:
            json.dump(myDict, outfile)