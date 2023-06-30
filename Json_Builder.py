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
startnumber = 1 # 1 if it should start from beginning
excel_path_or_name = "Jsons/Excels/01_Templates/Json_Excel_Template3.3.xlsx"

# -------- OLD EXPLANATIONS ----------
# type: CONTENT, OPTION_QUESTION, OPEN_QUESTION, SCALA_SLIDER, ITEM_LIST_EXPANDABLE (T OR C as answeroption), ITEM_LIST_SINGLE_CHOICE (R)
# content: P = Paragraph, R = Referenz, I = Image, A = Audio, M = More Information Expandable -> Titel ist immer dabei
# answer_option: R = Radio Button, C = Checkbox, T = Text_Field_Expandable
# next_logic_type: NEXT, NEXT_OPTION, REF_KEY_INSIGHT
# next_logic_options: N = option with next
# question_array = [Question('CONTENT','AM'),Question('SCALA_SLIDER','PRPM'), Question('OPTION_QUESTION','PRP'), Question('CONTENT'), Question('CONTENT'), Question('OPEN_QUESTION','PRP'), Question('SCALA_SLIDER'), Question('CONTENT','PR'), Question('OPEN_QUESTION','PRP'), Question('OPTION_QUESTION'), Question('CONTENT'), Question('CONTENT'), Question('CONTENT')]


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
#df.drop(index=df.index[0], axis=0)
df = df.iloc[1:].reset_index(drop=True)

# get first informations and set defaults
information = df.iloc[:, 1]
if information[0] == 'Reise' or information[0] == 'reise':
    information[0] = 'WORLD'
    # Test oase missing
    if not isinstance(information[1], str):
        raise Exception ('OASE Zuordnung missing')
    information[1] = '"'+information[1]+'"'
    # Test cardDisplayImageName
    if not isinstance(information[15], str):
        raise Exception ('cardDisplayImageName Zuordnung missing')
    information[15] = '"'+information[15]+'"'
elif information[0] == 'Kurztrip' or information[0] == 'kurztrip':
    information[0] = 'SHORT_TRIP'
    information[1] = 'null'
    information[15] = 'null'

# Test Aufruf
if information[0] == 'WORLD' and information[4] == 'Beginne deinen Kurztrip':
    raise Exception ('Aufruf passt nicht zur Reise')
elif information[0] == 'SHORT_TRIP' and information[4] == 'Etappenweise zum Ziel':
    raise Exception ('Aufruf passt nicht zum Kurztrip')

# convert all entries to strings
df = df.astype(str)

# ---------- CREATE QUESTION -----------------

# save always two arrays into the Question object with structure and texts respectively
# trip object has an all_questions array = questions_array + etappen start end screens array etc.
trip = Trip(df, id_base, version, write_beginning, write_ending, journey_key, information)
questions_array = trip.all_questions_array


# -------- WRITE FILE -------------------------------------

with open(os.path.join(sys.path[0], name_of_json_file+".json"), 'w+') as file:
    file.write(trip.json)


printie = ('''JIPIIEE - 
ITS DONE''')
print(printie)