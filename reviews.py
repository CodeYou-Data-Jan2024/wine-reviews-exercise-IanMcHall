import zipfile
import pandas as pd

#pd.read_csv parses the given csv file into the program.
#compression='zip' clarifies that the file is in the zip fromat so python/pandas knows to unzip it
#The 'r' outside the file indicates the string is a 'raw string', meaning it will ignore the \ character.
df = pd.read_csv(r'data\winemag-data-130k-v2.csv.zip', compression='zip')


#'df['count'] =' allows me to add a new column to the dataframe. In this case, it is called 'count'
#'df.gropuby('country)' creates a GroupBy object, which contains the information on each instance of countries in the 'country' column.
#'['country'].transform('count)' then tells the program to count each instance of the country column in each group previously created and return those values as a new column.
df['count'] = df.groupby('country')['country'].transform('count')

#here I am creating a new dataframe stored in a variable called 'average_points'
#'df.groupby('country')['points']' first groups all same value countries together, then it gathers the points (from the points column) in each unique group.
#then the .mean() method is applied to the total points for each individual group to find average of the points.
#finally, the .round(1) method is applied on top of this to round the mean to the tenth place.
average_points = df.groupby('country')['points'].mean().round(1)

#this drops every listed column from the dataframe.
df = df.drop(columns=['Unnamed: 0', 'description', 'points', 'designation', 'price', 'province', 'region_1', 'region_2', 'taster_name', 'taster_twitter_handle', 'title', 'variety', 'winery'])

#This drops duplicates values in the 'country' column, leaving me with only one instance of each country.
df = df.drop_duplicates('country')

#This merges the original dataframe with the 'averag_points' dataframe, essentially just adding 'average_points' to df.
#the 'average_points' column is renamed 'points' when it is added to df.
#'on='country'' merges the two dataframes with the 'country' column as the key, as both dataframes have already this information.
df = df.merge(average_points.rename('points'), on='country')

#this prints the dataframe as a string to the terminal, but excludes the index column.
print(df.to_string(index=False))

#Finally, this writes the dataframe to an external csv file.
df.to_csv(r'data\reviews-per-country.csv')