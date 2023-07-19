import os
import pandas as pd
import openpyxl
from trip_object import Trip
# 
#  ------ VARIABLES ------------------------------------
# Fill in:
name_of_json_file = "Test" # name with which you want to save the Json
journey_key = "Test_Short_Trip_Flora" # test key or Key of Journey
id_base = "flora-" # id base -> for testing e.g. your name, for the app the journey_key in small letters
version = "v"+str(34) # version of the json
write_beginning = True # False if you want to add to an existing json
write_ending = True # False if you want to add to an existing json
etappe = 1 # usually 1 except you want to add to an existing json in a different etappe
startnumber = 1 # usually 1 except you want to add to an existing json at a different screen number
excel_path_or_name = "Jsons/Excels/01_Templates/features/Json_Excel_Template_questionloops2.xlsx" # path to the exel template
save_directory = '/Users/FloraValentina/Library/Mobile Documents/com~apple~CloudDocs/Dokumente/Arbeit/Onesome/Coding/Jsons/Created' # path where you want to save the jsons
english_translation = False

# --------- EXCEL ---------

# check if path exists
if not os.path.exists(excel_path_or_name):
    raise Exception ('Excel path does not exist')

# Load the Excel file
workbook = openpyxl.load_workbook(excel_path_or_name)
sheet = workbook.worksheets[0]

# Convert the sheet data to a list of lists
data = sheet.values
data_list = list(data)

# Create a DataFrame from the list of lists
df = pd.DataFrame(data_list)

# set first row as heading
df.columns = df.iloc[0]
df = df.iloc[1:].reset_index(drop=True)

# convert all entries to strings
df = df.astype(str)


# ---------- CREATE QUESTIONS -----------------

trip = Trip(df, id_base, version, write_beginning, write_ending, journey_key, english_translation)

# -------- WRITE FILE -------------------------------------

with open(os.path.join(save_directory, name_of_json_file+".json"), 'w+') as file:
    file.write(trip.json)


printie = ('''JIPIIEE - 
ITS DONE''')
print(printie)