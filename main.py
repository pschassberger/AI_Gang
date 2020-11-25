# dictionary with list object in values 
import pandas as pd
details = { 
    'Name' : ['Ankit', 'Aishwarya', 'Shaurya',  
              'Shivangi', 'Priya', 'Swapnil'], 
    'Age' : [23, 21, 22, 21, 24, 25], 
    'University' : ['BHU', 'JNU', 'DU', 'BHU', 
                    'Geu', 'Geu'], 
} 
  
# creating a Dataframe object  
df = pd.DataFrame(details, columns = ['Name', 'Age', 
                                      'University'], 
                  index = ['a', 'b', 'c', 'd', 'e', 'f']) 
  
# get names of indexes for which column Age has value >= 21 
# and <= 23 
index_names = df[ (df['Age'] >= 21) & (df['Age'] <= 23)].index 
  
# drop these given row 
# indexes from dataFrame 
df.drop(index_names, inplace = True) 
  
print(df)
