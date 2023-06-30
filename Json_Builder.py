import os
import sys
import pandas as pd
import openpyxl
from trip_object import Trip
# 
#  ------ VARIABLES ------------------------------------
# Auszufüllen
name_of_json_file = "Test"
journey_key = "Test_Short_Trip_Flora"
id_base = "flora-"
version = "v"+str(25)
write_beginning = True
write_ending = True
etappe = 1
startnumber = 1 
excel_path_or_name = "Jsons/Excels/01_Templates/Json_Excel_Template3.3.xlsx"

# --------- EXCEL ---------

# Load the Excel file
workbook = openpyxl.load_workbook(excel_path_or_name)
sheet = workbook.active

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

trip = Trip(df, id_base, version, write_beginning, write_ending, journey_key)
questions_array = trip.all_questions_array


# -------- WRITE FILE -------------------------------------

with open(os.path.join(sys.path[0], name_of_json_file+".json"), 'w+') as file:
    file.write(trip.json)


printie = ('''JIPIIEE - 
ITS DONE''')
print(printie)