import pandas as pd
import numpy as np

def convertMoney(x):
    money = 0
    try:
        splittedX = x.split(" ")
    except AttributeError:
        print(x)
        return
    
    if splittedX[0] == 'US':
        money = float(splittedX[1].strip('$/ea'))
        #print(money)

    elif splittedX[0] == 'GBP':
        money = float(splittedX[1].strip('$/ea')) * 1.27

    elif splittedX[0] == 'C':
        money = float(splittedX[1].strip('$/ea')) * 0.74

    elif splittedX[0] == 'AU':
        money = float(splittedX[1].strip('$/ea')) * 0.66
    
    return money


def removeSold(data):
    try:
        cleanedData = data.strip(" sold")
        #print(cleanedData)
        cleanedData = cleanedData.replace(',', '')
        #print(cleanedData)
        return int(cleanedData)
    except AttributeError:
        return



df = pd.read_csv("socks_database.csv")

dfNoDup = df.drop_duplicates()
print(dfNoDup.info())
moneyColumn = dfNoDup["price"]
moneyColumn = moneyColumn.apply(convertMoney)
dfNoDup["price"] = moneyColumn
availabityColumn = dfNoDup['availability']
availabityColumn = availabityColumn.apply(removeSold)
dfNoDup["availability"] = availabityColumn

dfNoDup.to_csv("socks_database_no_duplicates.csv")