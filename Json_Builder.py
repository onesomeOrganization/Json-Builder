import os
import sys
from content_block_functions import *
from question_block_functions import *
from question_object import Question
import pandas as pd
from tests import do_tests
from progress import check_for_progress_type,create_progress, create_etappen_array
import openpyxl
# 
#  ------ VARIABLES ------------------------------------
# Auszufüllen
name_of_json_file = "Test"
journey_key = "Test_Short_Trip_Flora"
id_base = "flora-v"
version = str(15)
write_beginning = True
write_ending = True
etappe = 1
startnumber = 1 # 1 if it should start from beginning
excel_path_or_name = "Jsons/Excels/Kick-Off Begleitung.xlsx"

# -------- EXPLANATIONS ----------
# type: CONTENT, OPTION_QUESTION, OPEN_QUESTION, SCALA_SLIDER, ITEM_LIST_EXPANDABLE (T OR C as answeroption), ITEM_LIST_SINGLE_CHOICE (R)
# content: P = Paragraph, R = Referenz, I = Image, A = Audio, M = More Information Expandable -> Titel ist immer dabei
# answer_option: R = Radio Button, C = Checkbox, T = Text_Field_Expandable
# next_logic_type: NEXT, NEXT_OPTION, REF_KEY_INSIGHT
# next_logic_options: N = option with next
# question_array = [Question('CONTENT','AM'),Question('SCALA_SLIDER','PRPM'), Question('OPTION_QUESTION','PRP'), Question('CONTENT'), Question('CONTENT'), Question('OPEN_QUESTION','PRP'), Question('SCALA_SLIDER'), Question('CONTENT','PR'), Question('OPEN_QUESTION','PRP'), Question('OPTION_QUESTION'), Question('CONTENT'), Question('CONTENT'), Question('CONTENT')]

# TODO: Progress bei mehreren verästelungen

# ---------- HELPER ----------
def create_id(reference_id_excel):
    id_numbers = reference_id_excel.split('.')
    new_id = id_base + version + '-'+ id_numbers[0]+'-'+ id_numbers[1]
    return new_id

def get_number_etappen(questions_array):
    number_etappen = set()
    for question in questions_array:
        if question.id.split('.')[0].isdigit():
            number_etappen.add(question.id.split('.')[0])
        else:
            question.progress = None
    return number_etappen

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
elif information[0] == 'Kurztrip' or information[0] == 'kurztrip':
    information[0] = 'SHORT_TRIP'
    information[1] = 'null'

# Test Aufruf
if information[0] == 'WORLD' and information[4] == 'Beginne deinen Kurztrip':
    raise Exception ('Aufruf passt nicht zur Reise')
elif information[0] == 'SHORT_TRIP' and information[4] == 'Etappenweise zum Ziel':
    raise Exception ('Aufruf passt nicht zum Kurztrip')

# drop the first two columns
df = df.drop(df.columns[[0, 1]], axis=1)

# convert all entries to strings
df = df.astype(str)

# save always two arrays into the Question object with structure and texts respectively
questions_array = []
for i in range(0, len(df.columns), 2):
    questions_array.append(Question(id_base, version, df.iloc[:, i], df.iloc[:, i+1], df.columns[i]))

# ------ CLEAN OF NONE QUESTIONS ---------
none_questions = []
    # Test: delete empty questions
for question in questions_array:
    all_none = all(element == 'None' for element in question.structure)
    if question.structure.size == 0 or all_none:
        none_questions.append(question)

questions_array = [question for question in questions_array if question not in none_questions]


# ---------- INTER QUESTION DEPENDENCIES ----------

# add next question references
# loop through and add reference backward
for i, question in enumerate(questions_array):
    for x, struct in enumerate(question.structure):
        # check if structure has reference
        if struct == 'REFERENCE':
            # check if key insight reference
            if question.texts[x].isupper():
                # add to question before
                questions_array[i-1].reference_of_next_question = question.texts[x]
                questions_array[i-1].next_logic_type = 'REF_KEY_INSIGHT'


# -------- TESTS --------

do_tests(df, information, questions_array)


# ---------- TEXT FORMATIERUNG ---------

for question in questions_array:
    for i, text in enumerate(question.texts):
        if not pd.isnull(text):
            # find " and replace with \"
            # find breaks and delete them
            question.texts[i] = text.replace('"', '\\"').replace('\n', '').replace("_x000B_", "")

# ---------- PROGRESS -------

new_array = []
for et in get_number_etappen(questions_array):
    etappen_array = create_etappen_array(et, questions_array)
    type, splitscreen_number, number_questions_until_letzter_screen, count_branch, connectionscreen_number = check_for_progress_type(etappen_array)
    etappen_questions_array = create_progress(etappen_array, type, splitscreen_number, number_questions_until_letzter_screen, count_branch, connectionscreen_number)
    new_array.extend(etappen_questions_array)

# copy progress to actually array
for q1 in questions_array:
    for q2 in new_array:
        if q1.id == q2.id:
            q1.progress = q2.progress
   

# -------- WRITE FILE -------------------------------------

with open(os.path.join(sys.path[0], name_of_json_file+".json"), 'w+') as file:

    # BEGINNING
    if write_beginning:    
        file.write(create_beginning(id_base, version, journey_key, information))

    count = 0
    for i, question in enumerate(questions_array): 
        # set back count for Neue Etappe
        if question.type ==  'Neue Etappe':
            count = -1
            etappe += 1
        
        # calculate id base
        question_id = id_base+version+"-"+str(etappe)+"-"+str(startnumber+count)
        id_base_next_question = '"'+id_base+version+"-"+str(etappe)+"-"+str(startnumber+count+1)+'"'   

        # WRITE & NEXT_QUESTION_ID & REMOVE COMMA
        # Option A - weiter mit screen
        if 'weiter mit Screen' in question.structure:
            id_base_next_question = '"'+create_id(question.texts[np.where(question.structure == 'weiter mit Screen')][0])+'"'
            if i == (len(questions_array)-1) or (i < (len(questions_array)-1) and questions_array[i+1].type == 'Neue Etappe'):
                file.write(create_question(question, id_base, count, write_beginning, id_base_next_question, question_id, version, etappe)[:-1])
            else:
                file.write(create_question(question, id_base, count, write_beginning, id_base_next_question, question_id, version, etappe))

        # Option B - letzter Screen
        elif 'letzter Screen' in question.structure:
            id_base_next_question = 'null'
            if i == (len(questions_array)-1) or (i < (len(questions_array)-1) and questions_array[i+1].type == 'Neue Etappe'):
                file.write(create_question(question, id_base, count, write_beginning, id_base_next_question, question_id, version, etappe)[:-1])
            else:
                file.write(create_question(question, id_base, count, write_beginning, id_base_next_question, question_id, version, etappe))

        # Option C - keins von beiden
        else: 
            if i == (len(questions_array)-1) or (i < (len(questions_array)-1) and questions_array[i+1].type == 'Neue Etappe'):
                id_base_next_question = 'null'
                file.write(create_question(question, id_base, count, write_beginning, id_base_next_question, question_id, version, etappe)[:-1])
            else:
                file.write(create_question(question, id_base, count, write_beginning, id_base_next_question, question_id, version, etappe))
        
        # increase count
        count += 1

    # ENDING
    if write_ending:   
        file.write('''
      ],
      "questionLoops": []
    }
  ]
}
        '''
        )


printie = ('''JIPIIEE - 
ITS DONE''')
print(printie)