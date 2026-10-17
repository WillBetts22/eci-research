#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun May  8 22:57:31 2022

@author: aakole
"""
import pandas as pd
AnimalsandByproducts =	[1,2,3,4,5,16]
VegetablesFruitsPlants = [6,7,8,9,10,11,13,14]
FoodandPreparations =	[12,15,17,18,19,20,21,22,23,24]
EnergyDrillingandMining = [25,26,27]
Chemicals = 	[28,29]
ChemicalManufacturing =	[30,31,32,33,34,35,38]
RawManufacturing =	[37,39,40,41,42,43,46,69,68]
WoodProducts =	[44,45,47,48,49]
ClothingandAccessories =	 [61,62,63,64,65,66,67]
Textile = [50,51,52,53,54,55,56,57,58,59,60]
Metals =	 [72,73,74,75,76,77,78,79,80,81,82]
MachineryandConstruction	 = [83]
Transportation = [85,86,87,88,98]
Weapons	= [92,36]
DailyInstruments	 = [89,90,91,93,94,95]
PreciousStones = [70,71]
HighcomplexityProducts = [28,29,30,38,83,84,87,92,101,102,103,99]	
ServicesandUtilities = [99,100,107,106]

data= pd.read_csv("./Downloads/Para2013.csv")
headers = {"Animals and By-products": 0 , "Vegetables, Fruits and Plants" : 0,	"Food and Preparations":0,	"Energy Drilling and Mining":0,	"Chemicals":0,	"Chemical Manufacturing":0,	"Raw Manufacturing":0,	"Wood Products":0,"Clothing and Accessories":0	,"Textile":0,	"Metals":0, "Machinery and Construction":0,	"Transportation":0,	"Weapons":0,	"Daily Instruments":0,	"Precious Stones	":0,"High-complexity Products":0,	"Services and Utilities":0}
for i in AnimalsandByproducts:
    headers["Animals and By-products"] += data["Trade Value (US$)"][i-1]
for i in VegetablesFruitsPlants:
    headers["Vegetables, Fruits and Plants"] += data["Trade Value (US$)"][i-1]
for i in FoodandPreparations:
    headers["Food and Preparations"] += data["Trade Value (US$)"][i-1]
for i in EnergyDrillingandMining:
    headers["Energy Drilling and Mining"] += data["Trade Value (US$)"][i-1]
for i in Chemicals:
    headers["Chemicals"] += data["Trade Value (US$)"][i-1]
for i in ChemicalManufacturing:
    headers["Chemical Manufacturing"] += data["Trade Value (US$)"][i-1]
for i in RawManufacturing:
    headers["Raw Manufacturing"] += data["Trade Value (US$)"][i-1]
for i in WoodProducts:
    headers["Wood Products"] += data["Trade Value (US$)"][i-1]		
for i in ClothingandAccessories:
    headers["Clothing and Accessories"] += data["Trade Value (US$)"][i-1]
for i in Textile:
    headers["Textile"] += data["Trade Value (US$)"][i-1]
for i in Metals:
    headers["Metals"] += data["Trade Value (US$)"][i-1]
for i in MachineryandConstruction:
    headers["Machinery and Construction"] += data["Trade Value (US$)"][i-1]
for i in Transportation:
    headers["Transportation"] += data["Trade Value (US$)"][i-1]
for i in Weapons:
    headers["Weapons"] += data["Trade Value (US$)"][i-1]
for i in DailyInstruments:
    headers["Daily Instruments"] += data["Trade Value (US$)"][i-1]
for i in PreciousStones:
    headers["Precious Stones	"] += data["Trade Value (US$)"][i-1]
for i in HighcomplexityProducts:
    headers["High-complexity Products"] += data["Trade Value (US$)"][i-1]
for i in ServicesandUtilities:
    headers["Services and Utilities"] += data["Trade Value (US$)"][i-1]


print(headers.values())
  
