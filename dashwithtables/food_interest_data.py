# importing the os (operating system module)
import os
# using the os module to get the current working directory
# in order get the proper path for the excel file
cwd = os.getcwd()

# importing pandas module to read the excel file and extract the data
import pandas

# using pandas to read the excel file and giving the names of the columns
if cwd.endswith('/test'):
    excel_data = pandas.read_excel('../dashwithtables/ramenPhoSobaInterest.xlsx', names=["Country", "Pho", "Ramen", "Soba"])
else:
    excel_data = pandas.read_excel(cwd+'/dashwithtables/ramenPhoSobaInterest.xlsx', names=["Country", "Pho", "Ramen", "Soba"])

# removing the first line of data that contains the headers
# and returning the remating data in a list of dictionaries
data = excel_data.to_dict('records')[1:]
