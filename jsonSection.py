import json
import math
#ejemplo git lens
class jsonSection:
    def __init__(self):
        pass

    def openJson(self,selectedFile):
       with open(selectedFile, encoding="utf-8") as archivoJson:
            datos = json.load(archivoJson)
       return datos

#sends the tax rates available to the mainwindow
    def slot_mostrarTax(self,datos):
        taxes = list()
        for tax in datos['TaxRates']:
            taxes.append(tax['Name']+ " " + str(tax['Rate'])+ "%")
        return taxes

#sends the sections available to the mainwindow
    def slot_mostrarSecciones(self,datos):
        secciones = list()
        for section in datos['MenuSections']:   

            secciones.append(section['Name'])

        return secciones

#shows a list of the os on the menu
    def slot_mostrarOS(self,datos):
        os = list()
        os1 = None
        for i in range(0,len(datos["MenuSections"])):
            for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                    if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False:
                        os1 = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["Name"]
                    if len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"]) == 0:
                        pass
                    elif os1 in os:
                        pass
                    else:
                        os.append(os1)
        return os

#shows a list of the items on the menu and in which sections you can find them
    def slot_mostrarItems(self,datos):
        items = list()
        for i in range(0,len(datos["MenuSections"])):
            section = datos["MenuSections"][i]['Name']
            if len(datos["MenuSections"][i]["MenuItems"]) == 0:
                pass
            elif section in items:
                pass
            else:
                items.append(section)
                for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                    item = datos["MenuSections"][i]["MenuItems"][k]['Name']
                    items.append(item)
        return items

#checks if any item inside an OS is empty
    def find_empty_values(self,datos):

        emptyValues = []
        seccion = ""
        item = ""
        optionSetTitle = ""
        flag = False
        for section in datos["MenuSections"]:
            for items in section["MenuItems"]:
                for optionSets in items["MenuItemOptionSets"]:
                    for optionSetItems in optionSets["MenuItemOptionSetItems"]:
                        if optionSetItems["Name"] == "" or optionSetItems["Name"] == None:

                            seccion = section["Name"]
                            item = items["Name"]
                            optionSetTitle = optionSets["Name"]
                            flag = True
                            emptyValues.append((seccion, item, optionSetTitle))
                            print(emptyValues)

                            return emptyValues, flag
#Checks if there are linking codes
    def find_link_codes(self, datos):
        linkCodes = []
        seccion = ""
        item = ""
        optionSetTitle = ""
        flag = False
        for section in datos["MenuSections"]:
            for items in section["MenuItems"]:
                for optionSets in items["MenuItemOptionSets"]:
                    for optionSetItems in optionSets["MenuItemOptionSetItems"]:
                        if optionSetItems["NextMenuItemOptionSetId"] != None:
                            seccion = section["Name"]
                            item = items["Name"]
                            optionSetTitle = optionSets["Name"]
                            flag = True
                            linkCodes.append((seccion, item, optionSetTitle))

                            return linkCodes, flag

#changes the taxes for the selected sections (only items for now)
    def slot_changeTaxSelectedSections(self,datos,secciones,tax):
        newTaxRateId = 0
        for i in range (0,len(datos['TaxRates'])):
            if i == tax:
                newTaxRateId = datos['TaxRates'][i]['TaxRateId']
        for j in range(0,len(secciones)):
            for i in range(0,len(datos["MenuSections"])):
                section = datos["MenuSections"][i]["Name"]
                if section == secciones[j] or secciones[j] == "Change All":
                    for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                        for item in datos["MenuSections"][i]["MenuItems"]:
                            item['TaxRateId'] = newTaxRateId
                            for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                                for os in datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"]:
                                    for osi in datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems']:
                                        osi['TaxRateId'] = newTaxRateId


#changes the taxes for the selected items
    def slot_changeTaxSelectedItems(self,datos,itemSelected,tax):
        newTaxRateId = 0
        for i in range (0,len(datos['TaxRates'])):
            if i == tax:
                newTaxRateId = datos['TaxRates'][i]['TaxRateId']
        for j in range(0,len(itemSelected)):
            for h in range(0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][h]["MenuItems"])):
                    item = datos["MenuSections"][h]["MenuItems"][k]['Name']
                    if "Change All" in itemSelected[j] or item in itemSelected[j]:
                        datos["MenuSections"][h]["MenuItems"][k]['TaxRateId'] = newTaxRateId
                        for l in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"])):
                            for os in datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"]:
                                for osi in datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems']:
                                    osi['TaxRateId'] = newTaxRateId

#changes the taxes for the selected os options
    def slot_changeTaxSelectedOS(self,datos,osSelected,os,tax):
        newTaxRateId = 0
        for i in range (0,len(datos['TaxRates'])):
            if i == tax:
                newTaxRateId = datos['TaxRates'][i]['TaxRateId']
        for j in range(0,len(osSelected)):
            for i in range(0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                    for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                        for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'])):
                            osName = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["Name"]
                            if osSelected[j] == "Change All":
                                for osi in datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems']:
                                    if osName == os[j]:
                                        osi['TaxRateId'] = newTaxRateId
                            elif osSelected[j] == datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Name']:
                                datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['TaxRateId'] = newTaxRateId

#changes the taxes for the selected items with SS options
    def slot_changeTaxSelectedSS(self,datos,SSitems,text,tax):
        newTaxRateId = 0
        for i in range (0,len(datos['TaxRates'])):
            if i == tax:
                newTaxRateId = datos['TaxRates'][i]['TaxRateId']
        for t in range(0,len(text)):
            for j in range(0,len(SSitems)):
                for i in range(0,len(datos["MenuSections"])):
                    for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                        if SSitems[j] == datos["MenuSections"][i]["MenuItems"][k]["Name"]:
                            datos["MenuSections"][i]["MenuItems"][k]['TaxRateId'] = newTaxRateId
                            for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                                for os in datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"]:
                                    for osi in datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems']:
                                        osi['TaxRateId'] = newTaxRateId

                        for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                            for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'])):
                                if SSitems[j] == datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Name']:
                                    datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['TaxRateId'] = newTaxRateId


#changes the taxes for all sections (only items for now)
    def slot_changeTaxAllSections(self,datos,tax):
        newTaxRateId = 0
        for i in range (0,len(datos['TaxRates'])):
            if i == tax:
                newTaxRateId = datos['TaxRates'][i]['TaxRateId']
            for i in range (0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                    for item in datos["MenuSections"][i]["MenuItems"]:
                        item['TaxRateId'] = newTaxRateId
                        for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                            for os in datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"]:
                                for osi in datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems']:
                                    osi['TaxRateId'] = newTaxRateId

#remove the taxes for all sections (only items for now)
    def slot_RemoveTaxAllItems(self,datos,tax):
        newTaxRateId = tax
        for i in range (0,len(datos['TaxRates'])):
            #if i == tax:
                #newTaxRateId = datos['TaxRates'][i]['TaxRateId']
            for i in range (0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                    for item in datos["MenuSections"][i]["MenuItems"]:
                        item['TaxRateId'] = newTaxRateId
                        for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                            for os in datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"]:
                                for osi in datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems']:
                                    osi['TaxRateId'] = newTaxRateId

#overwrites the json file with the updated one
    def save_json(self,datos,selectedFile):
        with open(selectedFile, 'w') as archivo_nuevo:
            json.dump(datos, archivo_nuevo)

#######################################################################################################################
#######################################################################################################################
##################### PRICE MODIFICATIONS #############################################################################

#changes the prices for the selected sections by percentaje
    def slot_changePricePercentajeSelectedSections(self,datos,secciones,price,MO,SO):
        price = float(price)/100
        for j in range(0,len(secciones)):
            for i in range(0,len(datos["MenuSections"])):
                section = datos["MenuSections"][i]["Name"]
                if section == secciones[j] or secciones[j] == "Change All":
                    for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                            original_price = datos["MenuSections"][i]["MenuItems"][k]["Price"]
                            increased_price = float(original_price) * float(price)
                            new_price = float(increased_price) + float(original_price)
                            if float(new_price) >= 0:
                                datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                            for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                                if (datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                    for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                        increased_price = 0
                                        original_price = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                        increased_price = float(original_price) * float(price)
                                        new_price = float(increased_price) + float(original_price)
                                        if float(new_price) >= 0:
                                            datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))


#changes the prices for the selected sections by Fixed Amount
    def slot_changePriceFixedAmountSelectedSections(self,datos,secciones,price,MO,SO):
        for j in range(0,len(secciones)):
            for i in range(0,len(datos["MenuSections"])):
                section = datos["MenuSections"][i]["Name"]
                if section == secciones[j] or secciones[j] == "Change All":
                    for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                        if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"] == []:
                            original_price = datos["MenuSections"][i]["MenuItems"][k]["Price"]
                            new_price = float(price) + float(original_price)
                            if float(new_price) >= 0:
                                datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                        else:
                            original_price = datos["MenuSections"][i]["MenuItems"][k]["Price"]
                            new_price = float(price) + float(original_price)
                            if float(new_price) >= 0:
                                if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][0]["IsMasterOptionSet"] != True:
                                    datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                            for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                                if (datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                    for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                        if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] != 0:
                                            original_price = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                            new_price = float(price) + float(original_price)
                                            if float(new_price) >= 0:
                                                datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))

##changes the full prices for the selected sections
    def slot_changePriceSelectedSections(self,datos,secciones,price,MO,SO):
        for j in range(0,len(secciones)):
            for i in range(0,len(datos["MenuSections"])):
                section = datos["MenuSections"][i]["Name"]
                if section == secciones[j] or secciones[j] == "Change All":
                    for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                        if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"] == []:
                            datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(price))
                        else:
                            for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                                if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][0]["IsMasterOptionSet"] != True:
                                    datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(price))
                                if (datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                    for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                        datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(price))

##rounding up
    def round_up(self,n, decimals = 0):
         multiplier = 10 ** decimals
         return math.ceil(n * multiplier) / multiplier

##rounding down
    def round_down(self,n, decimals = 0):
         multiplier = 10 ** decimals
         return math.floor(n * multiplier) / multiplier

    def round_up99(self,valor):
        partedecimal:float  = valor % 1
        print("Parte decimal:", partedecimal, "- valor: ",valor)
        nuevovalor = valor - partedecimal
        print("Nuevovalor: ", nuevovalor)
        newValue = nuevovalor + 0.99
        print(newValue)
        return newValue

    def round_up5(self,n):
        if "." in str(n):
            if str(n)[-2] != ".":
                if float(str(n)[-2]) != 9 or (float(str(n)[-2]) == 9 and float(str(n)[-1]) < 5):
                    n = n * 10
                    if float(str(n)[-1]) > 5:
                        return math.ceil(n) / 10
                    elif float(str(n)[-1]) < 5 and float(str(n)[-1]) >=1:
                        n = n* 10
                        nstring = str(int(n))
                        nstring = nstring[:-1]
                        nstring = nstring + "5"
                        n = float(nstring) / 100
                        return float(n)
                    else:
                        return n/10
                else:
                    n = n * 10
                    return math.ceil(n) / 10
            else:
                return n

#changes the prices for the selected sections by percentaje
    def slot_roundPricesSelectedSections(self,datos,secciones,price,MO,SO):
        increased_price = float()
        new_price = float()
        for j in range(0,len(secciones)):
            for i in range(0,len(datos["MenuSections"])):
                section = datos["MenuSections"][i]["Name"]
                if section == secciones[j] or secciones[j] == "Change All":
                    for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                        original_price = datos["MenuSections"][i]["MenuItems"][k]["Price"]
                        if original_price != 0:
                            if price == 5:
                                increased_price = self.round_up5(self,float(original_price))
                            elif price == 10:
                                increased_price = self.round_up(self,float(original_price),1)
                            elif price == 99:
                                increased_price = self.round_up99(self,original_price)
                            elif price == 1:
                                increased_price = self.round_up(self,float(original_price),0)
                            new_price = float(increased_price)
                            if float(new_price) >= 0:
                                datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                        for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                            if (datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                    original_price = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                    if original_price != 0:
                                        if price == 5:
                                            increased_price = self.round_up5(self,float(original_price))
                                        elif price == 10:
                                            increased_price = self.round_up(self,float(original_price),1)
                                        elif price == 99:
                                            increased_price = self.round_up99(self,original_price)
                                        elif price == 1:
                                            increased_price = self.round_up(self,float(original_price),0)
                                        new_price = float(increased_price)
                                        if float(new_price) >= 0:
                                            datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))


###############ITEMS##################

#changes the prices for the selected items by percentaje
    def slot_changePricePercentajeSelectedItems(self,datos,itemSelected,price,MO,SO):
        price = float(price)/100
        for j in range(0,len(itemSelected)):
            for i in range(0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                    item = datos["MenuSections"][i]["MenuItems"][k]['Name']
                    if "Change All" in itemSelected[j] or item in itemSelected[j]:
                            original_price = datos["MenuSections"][i]["MenuItems"][k]["Price"]
                            increased_price = float(original_price) * float(price)
                            new_price = float(increased_price) + float(original_price)
                            if float(new_price) >= 0:
                                datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                            for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                                if (datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                    for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                        original_price = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                        increased_price = float(original_price) * float(price)
                                        new_price = float(increased_price) + float(original_price)
                                        if float(new_price) >= 0:
                                            datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))

#changes the prices for the selected items by Fixed Amount
    def slot_changePriceFixedAmountSelectedItems(self,datos,itemSelected,price,MO,SO):
        for j in range(0,len(itemSelected)):
            for h in range(0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][h]["MenuItems"])):
                    item = datos["MenuSections"][h]["MenuItems"][k]['Name']
                    if "Change All" in itemSelected[j] or item in itemSelected[j]:
                        if datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"] == []:
                            original_price = datos["MenuSections"][h]["MenuItems"][k]["Price"]
                            new_price = float(price) + float(original_price)
                            if float(new_price) >= 0:
                                datos["MenuSections"][h]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                        else:
                            original_price = datos["MenuSections"][h]["MenuItems"][k]["Price"]
                            new_price = float(price) + float(original_price)
                            if float(new_price) >= 0:
                                if datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][0]["IsMasterOptionSet"] != True:
                                    datos["MenuSections"][h]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                            for l in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"])):
                                if (datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                    for m in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                        original_price = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                        new_price = float(price) + float(original_price)
                                        if float(new_price) >= 0:
                                           datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))

##changes the full prices for the selected items
    def slot_changePriceSelectedItems(self,datos,itemSelected,price,MO,SO):
        for j in range(0,len(itemSelected)):
            for h in range(0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][h]["MenuItems"])):
                    item = datos["MenuSections"][h]["MenuItems"][k]['Name']
                    if "Change All" in itemSelected[j] or item in itemSelected[j]:
                        if datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"] == []:
                            datos["MenuSections"][h]["MenuItems"][k]['Price'] = float("{0:.2f}".format(price))
                        else:
                            for l in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"])):
                                if datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][0]["IsMasterOptionSet"] != True:
                                    datos["MenuSections"][h]["MenuItems"][k]['Price'] = float("{0:.2f}".format(price))
                                if (datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                    for m in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                        datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(price))

#round the prices for the selected items
    def slot_roundPricesSelectedItems(self,datos,itemSelected,price,MO,SO):
        for j in range(0,len(itemSelected)):
            for h in range(0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][h]["MenuItems"])):
                    item = datos["MenuSections"][h]["MenuItems"][k]['Name']
                    if "Change All" in itemSelected[j] or item in itemSelected[j]:
                        if datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"] == []:
                            original_price = datos["MenuSections"][h]["MenuItems"][k]["Price"]
                            if original_price != 0:
                                if price == 5:
                                    increased_price = self.round_up5(self,float(original_price))
                                elif price == 10:
                                    increased_price = self.round_up(self,float(original_price),1)
                                elif price == 99:
                                    increased_price = self.round_up99(self,original_price)
                                elif price == 1:
                                    increased_price = self.round_up(self,float(original_price),0)
                            new_price = float(increased_price)
                            if float(new_price) >= 0:
                                datos["MenuSections"][h]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                        else:
                            original_price = datos["MenuSections"][h]["MenuItems"][k]["Price"]
                            if original_price != 0:
                                if price == 5:
                                    increased_price = self.round_up5(self,float(original_price))
                                elif price == 10:
                                    increased_price = self.round_up(self,float(original_price),1)
                                elif price == 99:
                                    increased_price = self.round_up99(self,original_price)
                                elif price == 1:
                                    increased_price = self.round_up(self,float(original_price),0)
                                new_price = float(increased_price)
                                if float(new_price) >= 0:
                                    if datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][0]["IsMasterOptionSet"] != True:
                                        datos["MenuSections"][h]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                            for l in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"])):
                                if (datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                    for m in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                        original_price = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                        if original_price != 0:
                                            if price == 5:
                                                increased_price = self.round_up5(self,float(original_price))
                                            elif price == 10:
                                                increased_price = self.round_up(self,float(original_price),1)
                                            elif price == 99:
                                                increased_price = self.round_up99(self,original_price)
                                            elif price == 1:
                                                increased_price = self.round_up(self,float(original_price),0)
                                            new_price = float(increased_price)
                                            if float(new_price) >= 0:
                                                datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))



#changes the prices for the selected items by percentaje
    def slot_changePricePercentajeSelectedOS(self,datos,osSelected,os,price):
        price = float(price)/100
        for j in range(0,len(osSelected)):
            for h in range(0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][h]["MenuItems"])):
                    for l in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"])):
                        osName = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["Name"]
                        for m in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'])):
                            if osSelected[j] == "Change All":
                                if osName == os[j]:
                                    original_price = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                    increased_price = float(original_price) * float(price)
                                    new_price = float(increased_price) + float(original_price)
                                    if float(new_price) >= 0:
                                        datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))
                            elif osSelected[j] == datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Name']:
                                original_price = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                increased_price = float(original_price) * float(price)
                                new_price = float(increased_price) + float(original_price)
                                if float(new_price) >= 0:
                                    datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Price'] = float("{0:.2f}".format(new_price))


#changes the prices for the selected OS by Fixed Amount
    def slot_changePriceFixedAmountSelectedOS(self,datos,osSelected,os,price):
        for j in range(0,len(osSelected)):
            for h in range(0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][h]["MenuItems"])):
                    for l in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"])):
                        osName = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["Name"]
                        for m in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'])):
                            if osSelected[j] == "Change All":
                                if osName == os[j]:
                                    original_price = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                    new_price = float(price) + float(original_price)
                                    if float(new_price) >= 0:
                                        datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))
                            elif osSelected[j] == datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Name']:
                                original_price = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                new_price = float(price) + float(original_price)
                                if float(new_price) >= 0:
                                    datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Price'] = float("{0:.2f}".format(new_price))

#changes the prices for the selected OS by Fixed Amount
    def slot_roundPricesSelectedOS(self,datos,osSelected,os,price):
        increased_price = float()
        for j in range(0,len(osSelected)):
            for h in range(0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][h]["MenuItems"])):
                    for l in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"])):
                        osName = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["Name"]
                        for m in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'])):
                            if osSelected[j] == "Change All":
                                if osName == os[j]:
                                    original_price = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                    if original_price != 0:
                                        if price == 5:
                                            increased_price = self.round_up5(self,float(original_price))
                                        elif price == 10:
                                            increased_price = self.round_up(self,float(original_price),1)
                                        elif price == 99:
                                            increased_price = self.round_up99(self,original_price)
                                        elif price == 1:
                                            increased_price = self.round_up(self,float(original_price),0)
                                        new_price = float(increased_price)
                                        if float(new_price) >= 0:
                                            datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))
                            elif osSelected[j] == datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Name']:
                                original_price = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                if original_price != 0:
                                    if price == 5:
                                        increased_price = self.round_up5(self,float(original_price))
                                    elif price == 10:
                                        increased_price = self.round_up(self,float(original_price),1)
                                    elif price == 99:
                                        increased_price = self.round_up99(self,original_price)
                                    elif price == 1:
                                        increased_price = self.round_up(self,float(original_price),0)
                                    new_price = float(increased_price)
                                    if float(new_price) >= 0:
                                        datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Price'] = float("{0:.2f}".format(new_price))


##changes the full prices for the selected OS
    def slot_changePriceSelectedOS(self,datos,osSelected,os,price):
        for j in range(0,len(osSelected)):
            for h in range(0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][h]["MenuItems"])):
                    for l in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"])):
                        osName = datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["Name"]
                        for m in range(0,len(datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'])):
                            if osSelected[j] == "Change All":
                                if osName == os[j]:
                                    datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(price))
                            elif osSelected[j] == datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Name']:
                                datos["MenuSections"][h]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Price'] = float("{0:.2f}".format(price))

#########################################################################################
#changes the prices by Fixed Amount for the selected items on the Smart Search
    def slot_changePriceFixedAmountSelectedSS(self,datos,SSitems,text,price,MO,SO):
        for t in range(0,len(text)):
            for j in range(0,len(SSitems)):
                for i in range(0,len(datos["MenuSections"])):
                    for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                        if SSitems[j] == datos["MenuSections"][i]["MenuItems"][k]["Name"]:
                            if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"] == []:
                                original_price = datos["MenuSections"][i]["MenuItems"][k]["Price"]
                                new_price = float(price) + float(original_price)
                                if float(new_price) >= 0:
                                    datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                            else:
                                original_price = datos["MenuSections"][i]["MenuItems"][k]["Price"]
                                new_price = float(price) + float(original_price)
                                if float(new_price) >= 0:
                                    datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                                for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                                    if (datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                        for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                            if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] != 0:
                                                original_price = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                                new_price = float(price) + float(original_price)
                                                if float(new_price) >= 0:
                                                    datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))
                        for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                            for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'])):
                                if SSitems[j] == datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Name']:
                                    original_price = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                    new_price = float(price) + float(original_price)
                                    if float(new_price) >= 0:
                                        datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Price'] = float("{0:.2f}".format(new_price))

#round prices for the selected items on the Smart Search
    def slot_roundPricesSelectedSS(self,datos,SSitems,text,price,MO,SO):
        increased_price = float()
        for t in range(0,len(text)):
            for j in range(0,len(SSitems)):
                for i in range(0,len(datos["MenuSections"])):
                    for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                        if SSitems[j] == datos["MenuSections"][i]["MenuItems"][k]["Name"]:
                            if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"] == []:
                                original_price = datos["MenuSections"][i]["MenuItems"][k]["Price"]
                                if original_price != 0:
                                    if price == 5:
                                        increased_price = self.round_up5(self,float(original_price))
                                    elif price == 10:
                                        increased_price = self.round_up(self,float(original_price),1)
                                    elif price == 99:
                                        increased_price = self.round_up99(self,original_price)
                                    elif price == 1:
                                        increased_price = self.round_up(self,float(original_price),0)
                                    new_price = float(increased_price)
                                    if float(new_price) >= 0:
                                        datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                            else:
                                original_price = datos["MenuSections"][i]["MenuItems"][k]["Price"]
                                if original_price != 0:
                                    if price == 5:
                                        increased_price = self.round_up5(self,float(original_price))
                                    elif price == 10:
                                        increased_price = self.round_up(self,float(original_price),1)
                                    elif price == 99:
                                        increased_price = self.round_up99(self,original_price)
                                    elif price == 1:
                                        increased_price = self.round_up(self,float(original_price),0)
                                    new_price = float(increased_price)
                                    if float(new_price) >= 0:
                                        datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                                for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                                    if (datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                        for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                            if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] != 0:
                                                original_price = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                                if original_price != 0:
                                                    if price == 5:
                                                        increased_price = self.round_up5(self,float(original_price))
                                                    elif price == 10:
                                                        increased_price = self.round_up(self,float(original_price),1)
                                                    elif price == 99:
                                                        increased_price = self.round_up99(self,original_price)
                                                    elif price == 1:
                                                        increased_price = self.round_up(self,float(original_price),0)
                                                    new_price = float(increased_price)
                                                    if float(new_price) >= 0:
                                                        datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))
                        for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                            for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'])):
                                if SSitems[j] == datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Name']:
                                    original_price = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                    if original_price != 0:
                                        if price == 5:
                                            increased_price = self.round_up5(self,float(original_price))
                                        elif price == 10:
                                            increased_price = self.round_up(self,float(original_price),1)
                                        elif price == 99:
                                            increased_price = self.round_up99(self,original_price)
                                        elif price == 1:
                                            increased_price = self.round_up(self,float(original_price),0)
                                        new_price = float(increased_price)
                                        if float(new_price) >= 0:
                                            datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Price'] = float("{0:.2f}".format(new_price))



#changes the prices by percentaje for the selected items on the Smart Search
    def slot_changePricePercentajeSelectedSS(self,datos,SSitems,text,price,MO,SO):
        price = float(price)/100
        for t in range(0,len(text)):
            for j in range(0,len(SSitems)):
                for i in range(0,len(datos["MenuSections"])):
                    for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                        if SSitems[j] == datos["MenuSections"][i]["MenuItems"][k]["Name"]:
                            if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"] == []:
                                original_price = datos["MenuSections"][i]["MenuItems"][k]["Price"]
                                increased_price = float(original_price) * float(price)
                                new_price = float(increased_price) + float(original_price)
                                if new_price >= 0:
                                    datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                            else:
                                original_price = datos["MenuSections"][i]["MenuItems"][k]["Price"]
                                increased_price = float(original_price) * float(price)
                                new_price = float(increased_price) + float(original_price)
                                if float(new_price) >= 0:
                                    if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][0]["IsMasterOptionSet"] != True:
                                        datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(new_price))
                                for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                                    if (datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                        for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                            original_price = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                            increased_price = float(original_price) * float(price)
                                            new_price = float(increased_price) + float(original_price)
                                            if float(new_price) >= 0:
                                                datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(new_price))
                        for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                            for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'])):
                                if SSitems[j] == datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Name']:
                                    original_price = datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"]
                                    increased_price = float(original_price) * float(price)
                                    new_price = float(increased_price) + float(original_price)
                                    if float(new_price) >= 0:
                                        datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Price'] = float("{0:.2f}".format(new_price))

##changes the full prices for the selected items on the Smart Search
    def slot_changePriceSelectedSelectedSS(self,datos,SSitems,text,price,MO,SO):
        for t in range(0,len(text)):
            for j in range(0,len(SSitems)):
                for i in range(0,len(datos["MenuSections"])):
                    for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                        if SSitems[j] == datos["MenuSections"][i]["MenuItems"][k]["Name"]:
                            if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"] == []:
                                datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(price))
                            else:
                                if datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][0]["IsMasterOptionSet"] != True:
                                    datos["MenuSections"][i]["MenuItems"][k]['Price'] = float("{0:.2f}".format(price))
                                for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                                    if (datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == True and MO == True) or datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["IsMasterOptionSet"] == False and SO == True:
                                        for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"])):
                                            datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]["MenuItemOptionSetItems"][m]["Price"] = float("{0:.2f}".format(price))
                        for l in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"])):
                            for m in range(0,len(datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'])):
                                if SSitems[j] == datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Name']:
                                    datos["MenuSections"][i]["MenuItems"][k]["MenuItemOptionSets"][l]['MenuItemOptionSetItems'][m]['Price'] = float("{0:.2f}".format(price))
########################################################################################################################################################################
########################################################################################################################################################################

