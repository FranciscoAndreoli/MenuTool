import json
import uuid
import os
from datetime import datetime, timedelta, date

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

        def get_name_option_set(name):

            if name == None or name == "":
                return "Option"
            else:
                return name

        def get_time_settings_section(section):

            timeOptions = section['MenuSectionAvailability']['AvailableTimes']
            nameSection = section['Name']

            return timeOptions, nameSection

        def get_time_settings_item(item):

            timeOptions = item['DailySpecialHours']
            nameItem = item['Name']

            return timeOptions, nameItem

        def get_days_mapping(dayOfWeek):

            weekDayMapper = {
                0: "sundayEnabled",
                1: "mondayEnabled",
                2: "tuesdayEnabled",
                3: "wednesdayEnabled",
                4: "thursdayEnabled",
                5: "fridayEnabled",
                6: "saturdayEnabled"
            }

            weekDayKey = weekDayMapper[dayOfWeek]

            return weekDayKey

        def get_hours_availability(startTimeString, periodString):

            dateNumber = date.today()
            dateString = dateNumber.strftime("%Y-%m-%d")

            timeNumber = datetime.strptime(startTimeString, "%H:%M:%S")
            periodNumber = datetime.strptime(periodString, "%H:%M:%S")

            sumTime = timeNumber + timedelta(hours=periodNumber.hour, minutes=periodNumber.minute, seconds=periodNumber.second)

            sumTimeString = sumTime.strftime(f"{dateString} %H:%M:%S")
            timeNumberWithDate = timeNumber.strftime(f"{dateString} %H:%M:%S")

            return sumTimeString, timeNumberWithDate

        def get_params_to_string(weekDayKey, dayAvailability, timeNumberWithDate, sumTimeString, names):

            paramsJson = {
                weekDayKey: dayAvailability,
                "fromTime": timeNumberWithDate,
                "toTime": sumTimeString,
                "name": names,
                "enabled": True
            }

            # paramsJsonToString = json.dumps(paramsJson)
            # return paramsJsonToString

            return paramsJson

        def get_overrides(eachTime, name):

            overrides = []
            seenTimeSettings = {}

            if eachTime != None:
                for times in eachTime:

                    if times['Period'] == "00:00:00":
                        continue

                    weekDayKey = get_days_mapping(times['DayOfWeek'])
                    sumTimeString, timeNumberWithDate = get_hours_availability(
                        times['StartTime'],
                        times['Period']
                    )

                    key = (timeNumberWithDate, sumTimeString)

                    if key in seenTimeSettings:

                        seenTimeSettings[key].append(weekDayKey)

                    else:

                        seenTimeSettings[key] = [weekDayKey]

                for timeSetting, weekDays in seenTimeSettings.items():

                    newOverride = {
                        "id": generate_UUID(),
                        "paramsJson": {
                            "fromTime": timeSetting[0],
                            "toTime": timeSetting[1],
                            "name": f"{name} - hidden",
                            "enabled": True
                        },
                        "type": "generic"
                    }

                    for day in weekDays:
                        newOverride["paramsJson"][day] = True
                    newOverride["paramsJson"] = json.dumps(newOverride["paramsJson"])

                    overrides.append(newOverride)

            return overrides

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

            timeAvailabilitySection, nameSection = get_time_settings_section(section)
            newCategory['overrides'] = get_overrides(timeAvailabilitySection, nameSection)

            for item in section['MenuItems']:

                taxValue = get_tax(item["TaxRateId"]) #item["TaxRateId"] is the tax id for the item
                booleano = False if item["TaxRateId"] is None else True

                newItem = {
                    "caption": item['Name'],
                    "enabled": item['IsAvailable'],
                    "id": generate_UUID(),
                    "notes": item["Description"],
                    "imageUrl": get_image(item["ImageUrl"]),
                    "paramsJson": {
                        "kdsConfiguration": {
                            "kdsCaption": item['Name']
                        }
                    },
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

                newItem["paramsJson"] = json.dumps(newItem["paramsJson"])

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
                        "caption": get_name_option_set(modifier['Name']),
                        "enabled": True,
                        "modifierId": modifier['MenuItemOptionSetId'],
                        "overrides": []
                    }

                    newItem["modifierMembers"].append(new_menuOptionSet)

                for optionSet in item['MenuItemOptionSets']:

                    isMasterOption = optionSet['IsMasterOptionSet'] == True and len(optionSet['MenuItemOptionSetItems']) != 0
                    newOptionSet = { # modifiers
                            "canSameItemBeSelectedMultipleTimes": False,
                            "caption": get_name_option_set(optionSet['Name']),
                            "id": optionSet['MenuItemOptionSetId'],
                            "enabled": True,
                            "max": optionSet['MaxSelectCount'],
                            "min": optionSet['MinSelectCount'],
                            "position": optionSet['DisplayOrder'],
                            "overrides": [],
                            "items": []
                        }

                    for index, osItem in enumerate(optionSet['MenuItemOptionSetItems']):

                        taxValue = get_tax(osItem["TaxRateId"]) #osItem["TaxRateId"] is the tax id for the osItem
                        booleano = False if osItem["TaxRateId"] is None else True
                        newItemInOptionSet = { # items inside modifiers
                            "caption": osItem['Name'],
                            "enabled": osItem['IsAvailable'],
                            "id": osItem['MenuItemOptionSetItemId'],
                            "paramsJson": {
                                "kdsConfiguration": {
                                    "kdsCaption": osItem['Name']
                                }
                            },
                            "overrides": [],
                            "pricingProfiles": [ {
                                "collectionPrice": osItem['Price'],
                                "collectionTax": taxValue,
                                "collectionTaxable": booleano,
                                "deliveryPrice": osItem['Price'],
                                "deliveryTax": taxValue,
                                "deliveryTaxable": booleano,
                                "dineInPrice": osItem['Price'],
                                "dineInTax": taxValue,
                                "dineInTaxable": booleano,
                                "priceBandId": 'cc4efdb0-78a1-11ed-a7b2-713c0ffdd9d3',
                                "takeawayPrice": osItem['Price'],
                                "takeawayTax": taxValue,
                                "takeawayTaxable": booleano
                            } ],
                            "modifierMembers": []
                        }

                        newItemInOptionSet["paramsJson"] = json.dumps(newItemInOptionSet["paramsJson"])

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

                timeAvailabilityItem, nameItem = get_time_settings_item(item)
                newItem['overrides'] = get_overrides(timeAvailabilityItem, nameItem)

            myDict["categories"].append(newCategory)

        # remove duplicates
        encountered_modifiers = {}

        for j, first_modifier in enumerate(myDict["modifiers"]):
            for second_modifier in myDict["modifiers"][j+1:]:


                if (first_modifier["caption"].lower() == second_modifier["caption"].lower() and
                    len(first_modifier["items"]) == len(second_modifier["items"]) and
                    first_modifier["max"] == second_modifier["max"] and
                    first_modifier["min"] == second_modifier["min"]):

                    first_modifier["items"] = sorted(first_modifier["items"], key=lambda x: x["caption"])
                    second_modifier["items"] = sorted(second_modifier["items"], key=lambda x: x["caption"])

                    flag = 0
                    for i in range(len(first_modifier["items"])):
                        if (first_modifier["items"][i]["caption"] == second_modifier["items"][i]["caption"] and
                            first_modifier["items"][i]["enabled"] == second_modifier["items"][i]["enabled"] and
                            first_modifier["items"][i]["pricingProfiles"][0]["collectionPrice"] == second_modifier["items"][i]["pricingProfiles"][0]["collectionPrice"] and
                            first_modifier["items"][i]["pricingProfiles"][0]["collectionTax"] == second_modifier["items"][i]["pricingProfiles"][0]["collectionTax"]):

                            flag += 1
                            if flag >= len(first_modifier["items"]):
                                # Remove duplicate modifier
                                id_to_remove = second_modifier["id"]
                                encountered_modifiers[id_to_remove] = first_modifier["id"]

        # Replace duplicate modifier id with the original modifier id
        for key in encountered_modifiers:

            if key in encountered_modifiers.values():
                valor = encountered_modifiers[key]
                clave = list(encountered_modifiers.keys())[list(encountered_modifiers.values()).index(key)]
                encountered_modifiers[clave] = valor

        # Remove encountered duplicate modifiers using list comprehension
        myDict["modifiers"] = [modifier for modifier in myDict["modifiers"] if modifier["id"] not in encountered_modifiers]

        if(len(encountered_modifiers) > 0):
            #example output: {51038380: 51038379,
                                #51038381: 51038379,
                                #51038386: 51038379,
                                #51038387: 51038379,
                                #51038388: 51038385}
            for categories in myDict["categories"]:
                for item in categories["items"]:
                    for modifierMember in item["modifierMembers"]:
                        if modifierMember["modifierId"] in encountered_modifiers:
                            modifierMember["modifierId"] = encountered_modifiers[modifierMember["modifierId"]]

        #print(json.dumps(myDict, indent=2))

        # specify the path to save the file, including the desired name
        path = os.path.expanduser("~/Desktop/my_POS_JSON.json")

        # open the file for writing, and save the dictionary as JSON
        with open(path, 'w') as outfile:
            json.dump(myDict, outfile)