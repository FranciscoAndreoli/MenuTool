"""class CocaColaUpdates:
    def __init__(self):
        pass

    def slot_baseModifications(self,datos):
        pass

    def slot_concidenceSearcher(self,datos):
        for i in range(0,len(datos["MenuSections"])):
            for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                itemName = datos["MenuSections"][i]["MenuItems"][k]["Name"]
                itemDescription = datos["MenuSections"][i]["MenuItems"][k]["Description"]

                if ("Coca" in itemName or "Coke" in itemName) and ("Zero" not in itemName and "Diet" not in itemName):
                    datos["MenuSections"][i]["MenuItems"][k]["Name"] = "Coca-Cola Original"

                if ("Coca" in itemName or "Coke" in itemName) and ("Zero" in itemName):
                    datos["MenuSections"][i]["MenuItems"][k]["Name"] = "Coca-Cola Zero Sugar"

                if ("Coca" in itemName or "Coke" in itemName) and ("Diet" in itemName):
                    datos["MenuSections"][i]["MenuItems"][k]["Name"] = "Diet Coke"

                if "Sprite" in itemName:
                    datos["MenuSections"][i]["MenuItems"][k]["Name"] = "Sprite"

                if "Fanta" in itemName and ("Orange" in itemName or "Orange" in itemDescription):
                    datos["MenuSections"][i]["MenuItems"][k]["Name"] = "Fanta Orange"

                if "Fanta" in itemName and ("Lemon" in itemName or "Lemon" in itemDescription):
                    datos["MenuSections"][i]["MenuItems"][k]["Name"] = "Fanta Lemon"

                if "Fanta" in itemName and ("Straw" in itemName or "Straw" in itemDescription):
                    datos["MenuSections"][i]["MenuItems"][k]["Name"] = "Fanta Strawberry"

                if ("Coca" in itemName or "Coke" in itemName) and ("Diet" in itemName):
                    datos["MenuSections"][i]["MenuItems"][k]["Name"] = "Diet Coke" """

"""                    for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                        for os in datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"]:
                            for osi in datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems']:
                                osi['TaxRateId'] = newTaxRateId

                for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                    for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'])):
                        if SSitems[j] == datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Name']:
                            datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['TaxRateId'] = newTaxRateId
"""
