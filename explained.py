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

fig, axes = plt.subplots(1, 3, figsize=(15,5))
sns.countplot(x=df2['servings'], color='gray', ax=axes[0]).set(title='Count of servings')
sns.countplot(x=df2['category'], color='lightgreen', ax=axes[1]).set(title='Count of category')
sns.countplot(x=df2['high_traffic'], color='lightblue', ax=axes[2]).set(title='Count of high_traffic')
for ax in fig.axes:
    plt.sca(ax)
    plt.xticks(rotation=90);
    
'''
plt.sca(ax) stands for "set current axis" and it is a function in the matplotlib library.
In the given code, fig, axes = plt.subplots(1, 3, figsize=(15,5)) creates a figure object and 3 subplot axes. The first argument to subplots is the number of rows and 
the second argument is the number of columns, so 1, 3 means there is one row and three columns of subplots.
'''

def diff_for_numerical(df2, name):
    df2_high_agg = pd.pivot_table(df2[df2['high_traffic'] == 'High'], index=["category"], columns=["servings"], values=name, aggfunc=np.mean) # 

    df2_low_agg = pd.pivot_table(df2[df2['high_traffic'] == 'Low'], index=["category"], columns=["servings"], values=name, aggfunc=np.mean)

    df2_diff = df2_high_agg.subtract(df2_low_agg)
    
    f, ax = plt.subplots(figsize=(5, 6))
    sns.heatmap(df2_diff, annot=True, fmt=".1f", linewidths=.5, ax=ax, cmap="coolwarm_r", center=0) # "coolwarm" ["pink","lightgreen"] # cmaplist
    plt.title('Difference between means... for {0}'.format(name))
    plt.show()
    
    return df2_diff

for name in nutritional_1:
    diff_for_numerical(df2, name)
    
'''
The diff_for_numerical function is defined to create a heatmap that shows the difference between the average nutritional components of recipes with high traffic and 
those with low traffic. It takes two arguments: the dataset df2 and the name of the nutritional component.

First, the function uses the pd.pivot_table function to create two new dataframes, df2_high_agg and df2_low_agg, which group the recipes based on their categories and 
servings and calculate the average of the specified nutritional component for each group. One of the dataframes only contains recipes with high traffic and the other 
only contains recipes with low traffic.

Next, the function creates a new dataframe, df2_diff, by subtracting the nutritional component averages for the low traffic recipes from the averages for the high 
traffic recipes.

Then, the function creates a heatmap using sns.heatmap, which displays the difference between the average nutritional components of the high and low traffic recipes. 
The heatmap shows the nutritional component values for each category and serving size, with blue colors indicating a lower average value for high traffic recipes, and red colors indicating a higher average value for high traffic recipes.

Finally, the function returns the df2_diff dataframe so that it can be used later if necessary. The function is called in a loop to create a heatmap for each of the 
nutritional components in the nutritional_1 list.

* sns.heatmap(df2_diff, annot=True, fmt=".1f", linewidths=.5, ax=ax, cmap="coolwarm_r", center=0)
This line of code generates a heatmap plot using Seaborn library. 
* fmt=".1f": This parameter specifies the format string for the annotations. The .1f format means to display each value with one decimal place. In the Seaborn heatmap, 
the fmt parameter is used to format the annotations that appear on the heatmap. It is short for "format", and the value of fmt is a string that determines how the 
annotations will be displayed. The string should contain a format specifier that defines the layout of the annotations. In general, fmt is used to control the 
precision and format of the values that are displayed on the heatmap.
* linewidths=.5: This parameter sets the width of the lines that separate each cell in the heatmap.
* ax=ax: This parameter specifies the matplotlib Axes object where the heatmap should be drawn.
* cmap="coolwarm_r": This parameter sets the color map used for the heatmap. In this case, it uses the "coolwarm_r" color map, which ranges from blue (negative values) to red (positive values), with white being the center point (i.e., zero difference between high and low traffic mean values).
center=0: This parameter sets the center point of the color map. In this case, it is set to 0 to indicate no difference between high and low traffic mean values.
* An annotation refers to adding additional information, such as text or labels, to a plot or chart to help convey more meaning or context to the viewer. 
'''
sns.heatmap(df2_diff, annot=True, fmt=".1f", linewidths=.5, ax=ax, cmap="coolwarm_r", center=0)
'''
If you don't specify the ax parameter when creating a heatmap with sns.heatmap, the function will create its own figure and axis, and plot the heatmap on that axis. 
This is useful if you want to quickly visualize the heatmap without having to create the figure and axis objects yourself.
'''

# df = data_pv.pivot(index='category', columns='gender', values='no_show_prop')
num_pivot_df = pd.pivot_table(df2, index=["high_traffic"], values=nutritional_1, aggfunc=np.mean) # values=name, 
num_pivot_df.plot(kind='bar')

'''
pivot_table is a function in pandas that allows you to create a new table by aggregating and reshaping an existing table of data. 
The function is useful for summarizing and analyzing data by grouping it in different ways.
'''

grid = {
    "C": np.logspace(-3, 3, 7), # from -0.001 to 1000 by 7 steps
    "penalty": ["l1", "l2", "elasticnet", None],
    "multi_class": ["auto", "ovr", "multinomial"]
}
logreg = LogisticRegression()
logreg_cv = GridSearchCV(logreg, grid, cv=10)
logreg_cv.fit(X_train, y_train)

print("Tuned hyperparameters:", logreg_cv.best_params_)

'''
* GridSearchCV is used to find the best combination of hyperparameters for a given model by trying all possible combinations. 
It is a brute-force approach that trains the model on all possible hyperparameter combinations and selects the combination that gives the best results.


'''
grid = {
    "C": np.logspace(-3, 3, 7), # from -0.001 to 1000 by 7 steps
    "penalty": ["l1", "l2", "elasticnet", None],
    "multi_class": ["auto", "ovr", "multinomial"]
}

'''
* The penalty parameter specifies the type of regularization. Regularization is a technique used in machine learning to prevent overfitting of models. 
It involves adding a penalty term to the loss function of a model to discourage complex models that may fit the training data too closely and not generalize well to
new, unseen data. Regularization techniques, such as L1 regularization (lasso) and L2 regularization (ridge), can help to reduce the complexity of a model by shrinking
the values of the model parameters towards zero, thus avoiding overfitting.
* C is the inverse of the regularization strength, which means that smaller values of C lead to stronger regularization, and larger values of C lead to weaker 
regularization. It controls the regularization strength, with smaller values of C indicating stronger regularization.
* multi_class is a hyperparameter that specifies the strategy to use for multi-class classification. The options for this hyperparameter are:
auto: The strategy is determined based on the nature of the problem.
ovr: One-vs-Rest strategy creates one binary model for each class and then makes a prediction based on which model has the highest probability.
multinomial: The model builds a single classifier that can predict the probabilities of each of the possible classes.
'''






