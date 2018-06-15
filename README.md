
# Dash with Tables Lab

## Introduction
In this lab we will practice creating data tables and other elements in Dash. We will then introduce defining callbacks and practice using one to manipulate our table's data.

## Objectives
* Create a new Dash app and add a table with data read from an excel
* Create a dropdown element that provides selections by which to sort the new table
* Add a callback function to sort the data on the table

## Reading Our Data

The first thing we need to do is read our excel file `ramenPhoSobaInterest.xlsx` and extract the data we need to populate our table in dash. To do that, we will import pandas and use the `read_excel` function, which takes at least one argument, the path to the excel file, and multiple optional arguments such as a list of the column `names`. For more information on how this function works, refer to the documentation [here](http://pandas.pydata.org/pandas-docs/version/0.20.2/generated/pandas.read_excel.html)

```python
# in the food_interest_data.py file
# importing pandas module to read the excel file and extract the data
import pandas
# using pandas to read the excel file  and giving the names of the columns
excel_data = pandas.read_excel('FILE PATH', names=["Country", "Pho", "Ramen", "Soba"])

# removing the first line of data that contains the headers
# and returning the remaining data in a list of dictionaries
data = excel_data.to_dict('records')[1:]
```

Once we have our data, which is a list of dictionaries, which each contain the country and the percentage representing how many google searches were made for Pho, Ramen, or Soba, we can import it to our `__init__.py` file where we are creating the app's layout and table.

## Creating a Data Table with Dash

Now that we have our information we can begin making our layout. 

Unlike graphs, tables are HTML elements. So, we will add a table to our layout by using the dash_html_components module. We will need to make sure we first import dash, dash_core_components, and our data from the `food_interest_data.py` file. Since we are keeping up with our package structure for our dash app, our imports for other files will follow the `from [PACKAGE NAME].[FILE NAME] import [OBJECT NAME]` format. Therefore, to import our `data` our imports will look like the following:

```python
import dash
import dash_core_components as dcc
import dash_html_components as html

from dashwithtables.food_interest_data import data
```

Then, we will instantiate our new instance of our dash app and give it a url_base_pathname of '/', as a good practice so we signal to ourselves and to other developers where we would like our dashboard to be displayed.

```python
app = dash.Dash(__name__, url_base_pathname='/')
```

Let's add our layout! We will want an `h3` tag that reads `"Interest in Pho, Ramen, and Soba by Country according to Google Search from 01/2004 - 06/2018"`, and beneath that we will want our table.

Tables are easy to instantiate. We simply use html.Table(`children=[SOMECODE]`). Tables have several rows, the first of which is the header for the rest of the table, or the name of the columns. Since each dictionary has the name of the column pointing to its value `{'Country': 'Japan', 'Pho': 0.04, 'Ramen': 0.72, 'Soba': 0.24}` we, can create a function that will create the header row for us.

Above our layout, let's define a function called `generate_table` that will create the Dash html components and rows we need for our table. We can then call this function in our layout, to, well... generate the table! We'll pass this function the `data` we imported from the `food_interest_data.py` file. Let's make this parameter a default argument. 

```python
def generate_table(table_data=data):
    return html.Tr(id='food-table', children=[html.Th(col) for col in data[0].keys()])
```

First, we create a table row (i.e. `html.Tr`). Then, we are creating the children for that first row, which will be the table headers (i.e. `html.Th`). To get each column name as a table header we can use one element from our list of data and get the keys (i.e. `data[0].keys()`). Then we use list comprehension to push each new table header into the array of children for the first row.

If we look at our table now, it should look something like the following:

> <h3>Interest in Pho, Ramen, and Soba by Country according to Google Search from 01/2004 - 06/2018</h3>
> <table>
    <tr>
        <strong><th>Country</th><th>Pho</th><th>Ramen</th><th>Soba</th></strong>
    </tr>
</table>

We made this first row somewhat manually since there is only one. However, we aren't sure how many other rows there are in total. So, we're probably better off creating a list of table rows similar to how we made the table columns, using list comprehension:

```python
# creating a table row for each dictionary in our list of data
[html.Tr(children=[somecode]) for data_dict in data]
```

We haven't yet told our table rows what they are going to contain. They aren't going to contain table headers, since they will make up the body of our table and not the first row. These table cells should have our table data (i.e. html.Td(`[somecode]`)). A first naive approach might be to do the following: 

```python
# creating a table row for each dictionary in our list of data
[html.Tr(children=[html.Td(data_dict['country']), html.Td(data_dict['Pho']), html.Td(data_dict['Ramen']), html.Td(data_dict['Soba'])]) for data_dict in data]
```

We know what our data looks like.  There are four columns and we could create four table data elements for each row and get the value from our dictionary by hardcoding the names of each key as we do above. However, what happens if our data inputs ever change?  For example, the person providing us this data could decide to change the name of a column or add or delete certain columns.  If such a scenario played out, our `generate_table` function would break.  Let's add some abstraction to make this function more flexible and reusable.

```python
# creating a table row for each dictionary in our list of data
[html.Tr(children=[html.Td(data_dict[column]) for column in data_dict.keys()]) for data_dict in data]
```

Above we are creating a dictionary keys (`dict_keys`) object and iterating over each element, which represent the name of each key in the dictionary, and using it to create a table cell with the value from each key or column with list comprehension. Now our code is more concise, and it automatically generates a table cell for each column in the table and gives it the value of that cell. 

With that process complete, we should have created all the cells we need for our table.

However, we have a headers list too.  If we keep our code as is, we will get an error since we will have our table's children attribute pointing to two separate lists. To fix this we will need to conjoin these two lists. One way of combining lists is simply adding the two together with an addition symbol (`+`).

Our completed function looks like the following:

```python
def generate_table(table_data=data):
    return html.Table(id='food-table', children=
        # create table headers (the first table row)
        [html.Tr(id='headers', children=[html.Th(col) for col in table_data[0].keys()])]
        # combine the table headers and table data lists into one list
        +
        # create more table rows containing table cells with all our data
        [html.Tr(id='row-data', children=[
            html.Td(data_dict[column]) for column in data_dict.keys()
        ]) for data_dict in table_data]
    )
```

Now when we look at our dashboard in the browser, we should have a fully filled-in table!

> <h3>Interest in Pho, Ramen, and Soba by Country according to Google Search from 01/2004 - 06/2018</h3>
> <table>
    <tr>
        <strong><th>Country</th><th>Pho</th><th>Ramen</th><th>Soba</th></strong>
    </tr>
    <tr><td>Japan</td><td>0.04</td><td>0.72</td><td>0.24</td></tr>
    <tr><td>Taiwan</td><td>0.04</td><td>0.91</td><td>0.05</td></tr>
    <tr><td>Singapore</td><td>0.16</td><td>0.74</td><td>0.1</td></tr>
    <tr><td>Hong Kong</td><td>0.14</td><td>0.75</td><td>0.11</td></tr>
    <tr><td>Philippines</td><td>0.18</td><td>0.78</td><td>0.04</td></tr>
    <tr><td>Canada</td><td>0.6</td><td>0.34</td><td>0.06</td></tr>
    <tr><td>United States</td><td>0.51</td><td>0.45</td><td>0.04</td></tr>
</table>

## Add a Callback Function to Sort Table Data

Great, we now have a table that displays countries and the percentages for which they query Google for Pho, Ramen, and Soba. What if we'd like to sort this information? 

First, we will need to add a dropdown, which is a dcc component. Our dropdown should give the user four `options` to select since we want to sort by any of the four columns in our table.  Each option should have a `label`, the text you want displayed, and a `value`, the string or other piece of data you want to use to represent that selection. In this case, our label and value will be the same because we want our dropdown labels to be the same name as the columns we wish to sort by.  Let's add our dropdown, featured below, to our `app.layout`.  Also, let's make it the first element of the children list so that it appears at the top of our web page.

```python
dcc.Dropdown(
        id='sort-by-selector',
        options=[
            {'label': 'Country', 'value': 'Country'},
            {'label': 'Pho', 'value': 'Pho'},
            {'label': 'Ramen', 'value': 'Ramen'},
            {'label': 'Soba', 'value': 'Soba'}
        ],
        value="Country"
    ),
```
Like all other elements, we give the dropdown an `id`. The `value` property will be the starting value for the dropdown.  Since we set this initial value to "country", we can expect the initial state of our table to be sorted by country in alphabetical order.

Now that we have added a dropdown to the top of our app's layout, we can interact with our table by using a callback. A callback is defined using a decorator on the app, similar to a route.

```python
@app.callback(
    # some code goes here   
)
```

Inside our callback, we decide what it should *take in* as the value we are looking to change and the *output*, or where we would like to make our change. Our dropdown is going to have the value by which we want to filter our table, and the table (id='food-table') is going to be the element we want to alter. 

First, we need to import the `Input` and `Output` modules from `dash.dependencies`. Let's update our imports at the top of the file.

```python
from dash.dependencies import Input, Output
```

Then, let's to fill in our callback function. 

```python
@app.callback(
    Output(component_id='food-table', component_property='children'),
    [Input(component_id='sort-by-selector', component_property='value')]
)
```

First we define which element is going to take the output and which attribute we are going to overwrite. Then we define the input for our callback in a list. Next, we define our function and how we would like to manipulate our data. We will call this function `sort_table` and pass it the an argument that is going to be the value from the dropdown with the id `sort-by-selector`. We can call this argument whatever we want, but let's name it `input_value` for now.

```python
def sort_table(input_value):
    # some code
```

The input value is going to be the value of whichever `option` we select in our dropdown element. So, our sorting logic will look something like this:

```python
# datum is a single dictionary
# input value represents the value we selected
# we will use this value to access the datum key's value by which we want to sort our data
sorted(data, key=lambda datum: datum[input_value])
```

Lastly, we will pass this sorted data to our `generate_table` function so that we can re-create our newly sorted table.

```python
def sort_table(input_value):
    # using global to make sure we are accessing the imported data object
    global data
    sorted_data = sorted(data, key=lambda datum: datum[input_value])
    return generate_table(sorted_data)
```

Now when we make a selection our table will sort by the selection -- the default is currently by country.

Uh oh! If we look at our terminal we can see that this callback is firing over and over! 

To fix this, we will need to change a bit how we structured things. Instead of calling `generate_table` in our app's layout, we will create a new `html.Div` element named `table-container` that will now receive the output value of our callback -- which will get invoked once when the page loads and anytime we make a selection in the dropdown. We then need to update our callback definition's output `id` to be `table-container`. Once we make both of these changes, our table's sorting feature should be functioning and our terminal.

```python
app.layout = html.Div(children=[
    dcc.Dropdown(
        id='sort-by-selector',
        options=[
            {'label': 'Country', 'value': 'Country'},
            {'label': 'Pho', 'value': 'Pho'},
            {'label': 'Ramen', 'value': 'Ramen'},
            {'label': 'Soba', 'value': 'Soba'}
        ],
        value="Country"
    ),
    html.H3('Interest in Pho, Ramen, and Soba by Country according to Google Search from 01/2004 - 06/2018'),
    html.Div(id='table-container')
])

@app.callback(
    Output(component_id='table-container', component_property='children'),
    [Input(component_id='sort-by-selector', component_property='value')]
)
def sort_table(input_value):
    global data
    sorted_data = sorted(data, key=lambda datum: datum[input_value])
    return generate_table(sorted_data)
```

## Summary

Great work! In this lab, we practiced creating a Dash app, using both Dash core components and Dash HTML components to create a table on our app's dashboard. Then, we defined a callback that programmatically sorted our app's table by the column selected from our dropdown element.
