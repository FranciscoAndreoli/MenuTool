class VouchersAndAlcohol:
    def __init__(self):
        pass

## this slot activates the voucher or alcohol tag on the sections that are selected.
    def slot_changeVoucherAlcoholSelectedSections(self,datos,secciones,Voucher,Alcohol):
        for j in range(0,len(secciones)): #'Secciones' contiene las sections que el usuario eligió en la listita.
            for i in range(0,len(datos["MenuSections"])): #datos es el JSON
                section = datos["MenuSections"][i]["Name"]
                if section == secciones[j] or secciones[j] == "Change All":
                    for k in range(0,len(datos["MenuSections"][i]["MenuItems"])):
                        for item in datos["MenuSections"][i]["MenuItems"]:
                            if Voucher == True:
                                item['ExcludeFromVoucherDiscounting'] = True
                            if Alcohol == True:
                                item['Alcohol'] = True

## this slot activates the voucher or alcohol tag on the items that are selected.
    def slot_changeVoucherAlcoholSelectedItems(self,datos,items,Voucher,Alcohol):
        item = str()
        for j in range(0,len(items)):
            for h in range(0,len(datos["MenuSections"])): #recorre de 0 a 4
                if datos["MenuSections"][h]["Name"] in items[j]:
                    for k in range(0,len(datos["MenuSections"][h]["MenuItems"])):
                        item = datos["MenuSections"][h]["MenuItems"][k]['Name']
                        if item in items[j] or "Change All" in items[j]:
                            if Voucher == True:
                                datos["MenuSections"][h]["MenuItems"][k]['ExcludeFromVoucherDiscounting'] = True
                            if Alcohol == True:
                                datos["MenuSections"][h]["MenuItems"][k]['Alcohol'] = True
                else:
                    pass

##changes the tags for the selected items on the Smart Search
    def slot_changeVoucherAlcoholSelectedSS(self,datos,SSitems,text,Voucher,Alcohol):
        #for t in range(0,len(text)):
        for j in range(0,len(SSitems)):
            for h in range(0,len(datos["MenuSections"])):
                for k in range(0,len(datos["MenuSections"][h]["MenuItems"])):
                    if SSitems[j] == datos["MenuSections"][h]["MenuItems"][k]["Name"]:
                        if Voucher == True:
                            datos["MenuSections"][h]["MenuItems"][k]['ExcludeFromVoucherDiscounting'] = True
                        if Alcohol == True:
                            datos["MenuSections"][h]["MenuItems"][k]['Alcohol'] = True
