import pandas as pd
import ast
import random
import serial



def treeselector():
#reads csv files
    df = pd.read_csv("trees.csv",)
    dt = pd.read_csv("microbitmoisture.csv",)

#reads microbit data
    soilmoisture = dt["Moisture"].iloc[99]
    print("There is a soil moisture reading of:",soilmoisture)
    #soilmoisture = 30
    temp = dt["Temperature"].iloc[99]
    #temp = 10

#Converts column from string into a list - '[10,5]' -> [10,5]
#seperates the value within the column [10,5] -> 10 , 5
#Gets the average of the two numbers (10 + 5) / 2
    df['Avg_Yearly_Temp_C']= df['Avg_Yearly_Temp_C'].apply(ast.literal_eval)
    df[['minpref','maxpref']]= pd.DataFrame(df['Avg_Yearly_Temp_C'].tolist(),index = df.index)
    df['Avg_Yearly_Temp_C'] = (df['minpref'] + df['maxpref']) / 2
    Avg_temp = df['Avg_Yearly_Temp_C']
#print(Avg_temp)

    df['Ideal_Soil_Moisture_pct']= df['Ideal_Soil_Moisture_pct'].apply(ast.literal_eval)
    df[['minpref','maxpref']]= pd.DataFrame(df['Ideal_Soil_Moisture_pct'].tolist(),index = df.index)
    df['moisturepref'] = (df['minpref'] + df['maxpref']) / 2
    moisturepref = df['moisturepref']


#temp = df['Avg_Yearly_Temp_C']
#compares list of temp and reported temp
#Takes lowest diffrence and records index
    def closest_temp(Avg_temp, temp):
        temp_diffs = (temp - Avg_temp).abs()
        #print(temp_diffs)
        min_diff = temp_diffs.min()
        return temp_diffs[temp_diffs == min_diff].index
#Takes index from function and compares it to column 'trees' to select the tree best suited
    trees = df['Tree_Species']
    treetemppref = [trees[i] for i in closest_temp(Avg_temp,temp)]
    print('Tree(s) suited to the temperature are:')
    print(treetemppref)


    def closest_moisture(pref, soilmoisture):
        diffs = (soilmoisture - pref).abs()
        min_diff = diffs.min()
        return diffs[diffs == min_diff].index
    trees = df['Tree_Species']
    treepref = [trees[i] for i in closest_moisture(moisturepref,soilmoisture)]
    print('Tree(s) suited to the soil are:')
    print(treepref)

    carbonabsorbsion_temp = df['Average_CO2_Absorption_kg_per_year']
    suitabletrees_temp = [carbonabsorbsion_temp[i] for i in closest_temp(Avg_temp,temp)]
    mostcarbon_temp = max(suitabletrees_temp)
    #findindex_temp = suitabletrees_temp.index(mostcarbon_temp)
    indices = closest_temp(Avg_temp, temp)
    #print(indices)
    findindex_temp = max(indices, key=lambda i: carbonabsorbsion_temp[i])

    carbonabsorbsion = df['Average_CO2_Absorption_kg_per_year']
    suitabletrees = [carbonabsorbsion[i] for i in closest_moisture(moisturepref,soilmoisture)]
    mostcarbon = max(suitabletrees)
    #findindex = suitabletrees.index(mostcarbon)
    indices = closest_moisture(moisturepref, soilmoisture)
    #print(indices)
    findindex = max(indices, key=lambda i: carbonabsorbsion[i])
 
 
    print(trees[findindex_temp],'is the tree best suited to the temperature, with its average carbon absorbsion of',mostcarbon_temp,'kg per year')
    print('However based on your soil',trees[findindex],'would be a good pick, due to its average carbon absorption of',mostcarbon,'kg per year')


#finds the second optimal factor of the best trees
    #suitedtemp = df.iloc[findindex_temp]["Avg_Yearly_Temp_C"]
    suitedtemp = 60
#print(df['moisturepref'])
    optimalmoisture_list = df['moisturepref'].index[findindex]
    treemoisturepref = df['Ideal_Soil_Moisture_pct'][optimalmoisture_list]
    moistureoftree = sum(treemoisturepref) / len(treemoisturepref)

#compares two best trees shown previously and selects tree with higher carbon absorbsion
#Based on the tree selected it will look at the other value and look at what it needs to meet its optimal condition
#Gives advice on how to change enviromental conditions
    if mostcarbon_temp > mostcarbon:
        print(trees[findindex_temp], "should be planted")
        if soilmoisture < moistureoftree:
            print("Irrigation is advised to reach optimum soil moisture for", trees[findindex_temp])
        elif soilmoisture == moistureoftree:
            print("Optimal conditions achieved")
        else:
            print("Less watering required")
    elif mostcarbon_temp < mostcarbon:
        print(trees[findindex],"should be planted")
        if temp > suitedtemp:
            print("Tree should be planted with cover decreasing temperature")
        elif temp == suitedtemp:
            print("Optimal temperature has been reached")
        else:
            print("Heater needs to be added for optimal temperature to be reached")
    else:
        print("Either tree is suitable")



treeselector()


