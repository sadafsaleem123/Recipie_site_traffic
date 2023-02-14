# create new dataframe for changing values and columns
# remove all recipes with null values in calories, carbohydrate, sugar and protein columns
# df2 = df[df['calories'].notna()]
df2 = df[list(df)]
# df["value"] = df.groupby(["category","servings"]).transform(lambda x: x.fillna(x.mean()))
for name in nutritional: 
    df2[name] = df2[name].fillna(df.groupby(["category","servings"])[name].transform('mean'))
df2.info()


'''
* The groupby method is used to group data based on one or more columns in a DataFrame. This creates groups of rows with the same values in the specified columns.
In the given project code, df.groupby(["category","servings"]) groups the data by two columns, "category" and "servings". This means that the data will be divided
into separate groups based on the unique combinations of values in these two columns. 
* In the code fillna(df.groupby(["category","servings"])[name]), name is used to specify which column to select from the grouped DataFrame. df.groupby(["category","servings"]) 
groups the original DataFrame df by the category and servings columns. This returns a grouped DataFrame object that has each unique combination of category and servings 
as its index. [name] then selects the specific column from the grouped DataFrame that we want to fill missing values for. This allows us to calculate the mean of each 
name column for each group of category and servings, and then use that mean to fill in the missing values for that name column within that group.
* The transform method applies a function to each group and returns a 
DataFrame with the same shape as the original, but with the missing values filled with the result of the function. In this case, the transform method is used 
to fill in missing values in the nutritional columns with the mean value of the corresponding column within each group (defined by the unique combinations of 
"category" and "servings"). The resulting DataFrame, df2, has the same shape as the original df, but with the missing values in the nutritional columns filled 
in with the mean value for each group.
'''
df2.groupby(['servings'])['category'].count()

'''
In the given code df2.groupby(['servings'])['category'].count(), we are using the groupby method of pandas dataframe.
Here, we are grouping the data in df2 by the values in the 'servings' column.
Then we are selecting the 'category' column of this grouped data, and counting the number of rows for each unique value in the 'servings' column.
So the output will be a pandas Series object where the index will be unique values in the 'servings' column, and the corresponding values will be the count of rows for
each unique 'servings' value.
'''
df2['servings'] = df2['servings'].replace({"4 as a snack": '4', "6 as a snack": '6'}).astype('int')
df2.groupby(['servings'])['recipe'].count()

'''
In the df2.groupby(['servings'])['recipe'].count() code, the first set of brackets ['servings'] indicates the column or columns that we want to group our data by. 
In this case, we want to group the data based on the unique values in the 'servings' column.
The second set of brackets ['recipe'] indicates the specific column that we want to perform an operation on. In this case, we want to count the number of entries in 
the 'recipe' column for each unique value in the 'servings' column.
So, the resulting output will be a count of how many times each value in the 'servings' column appears in the 'recipe' column.
'''

df2['high_traffic'].fillna("Low", inplace = True)

'''
In the Pandas library, the fillna() method is used to replace any missing or null values in a dataframe with a specified value.
The inplace parameter is an optional argument that is used to specify whether to modify the original dataframe or return a new dataframe with the changes.
When inplace = True, the method will modify the original dataframe and the changes will be saved to the same dataframe. If inplace = False or is not provided, 
then the method will return a new dataframe with the changes and the original dataframe will remain unchanged.
So in the given code, df2['high_traffic'].fillna("Low", inplace = True) will replace any missing values in the 'high_traffic' column with the string "Low" and the 
changes will be saved to the original dataframe, df2.
'''
# added new columns: nutritional components in all servings, not per one

for name in nutritional:
    df2[name + '_1'] = df2[name] * df2['servings'] 
'''
In the given project, nutritional is a list containing the names of nutritional components such as calories, carbohydrate, sugar, and protein. These components are 
provided per serving in the original dataset. However, it may be useful to have the nutritional values for the entire recipe, rather than just per serving.
To get the total nutritional values for a recipe, we need to multiply the values per serving by the number of servings. This is what the above code does - it creates 
new columns for each nutritional component, where the value is the original value for that component multiplied by the number of servings. For example, calories_1 is 
the total number of calories for the entire recipe (rather than just per serving).
'''

sns.countplot(df2, x="servings", hue="high_traffic")
'''
In sns.countplot, hue is a parameter that allows you to specify a categorical variable to group the data by and display the count of each category as separate bars.
'''

