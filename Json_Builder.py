import os
import sys
from content_block_functions import *
from question_block_functions import *
from question_object import *
import pandas as pd
import re
# 
#  ------ VARIABLES ------------------------------------
# Auszufüllen
name_of_json_file = "Test"
journey_key = "Test_Short_Trip_Flora"
id = "flora-v"
version = str(12)
write_beginning = True
write_ending = True
etappe = 1
startnumber = 1 # 1 if it should start from beginning
excel_path_or_name = "Jsons/Json Builder/Templates/23_05_09_Json_Excel_Template_screenrefs.xlsx"

# -------- EXPLANATIONS ----------
# type: CONTENT, OPTION_QUESTION, OPEN_QUESTION, SCALA_SLIDER, ITEM_LIST_EXPANDABLE (T OR C as answeroption), ITEM_LIST_SINGLE_CHOICE (R)
# content: P = Paragraph, R = Referenz, I = Image, A = Audio, M = More Information Expandable -> Titel ist immer dabei
# answer_option: R = Radio Button, C = Checkbox, T = Text_Field_Expandable
# next_logic_type: NEXT, NEXT_OPTION, REF_KEY_INSIGHT
# next_logic_options: N = option with next
# question_array = [Question('CONTENT','AM'),Question('SCALA_SLIDER','PRPM'), Question('OPTION_QUESTION','PRP'), Question('CONTENT'), Question('CONTENT'), Question('OPEN_QUESTION','PRP'), Question('SCALA_SLIDER'), Question('CONTENT','PR'), Question('OPEN_QUESTION','PRP'), Question('OPTION_QUESTION'), Question('CONTENT'), Question('CONTENT'), Question('CONTENT')]

# TODO: Nummerierung kontrollieren

# --------- EXCEL ---------
df = pd.read_excel(excel_path_or_name)

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
    questions_array.append(Question(df.iloc[:, i], df.iloc[:, i+1]))


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
                questions_array[i-1].next_question_reference = question.texts[x]
                questions_array[i-1].next_logic_type = 'REF_KEY_INSIGHT'


# -------- TESTS --------

# Test nummeration
nummeration = []
pattern = '^\d+\.\d+$'
for column in df.columns:
    if re.match(pattern, column):
        nummeration.append(column)

for i, number in enumerate(nummeration):
    if i == len(nummeration)-1:
        break
    splits = number.split('.')
    # first number has to be the same and second counting or first number counting and second a 1
    if splits[0] == nummeration[i+1].split('.')[0] and int(splits[1])+1 == int(nummeration[i+1].split('.')[1]):
        continue
    elif int(splits[0])+1 == int(nummeration[i+1].split('.')[0]) and nummeration[i+1].split('.')[1] == '1':
        continue
    else:
        raise Exception ('Nummeration is wrong somwhere around position: ', i+1)

# Check if all information fields are there
for i,info in enumerate(information):
    if i > 8:
        break
    if pd.isna(info):
        raise Exception('There is some starting information missing')
    
formatting_flag = 0
    # Test: delete empty questions
for question in questions_array:
    if question.structure.size == 0:
        questions_array.remove(question)

for q_count, question in enumerate(questions_array):
    # Test: immer mit subtitle starten
    if not question.structure[0] == 'SUB_TITEL' and not question.structure[0] == 'Neue Etappe':
        raise Exception ('SUB_TITEL is missing for question ',q_count+1)
    # Test: kein item single und item multiple in einer frage 
    if 'ITEM(Multiple)' in question.structure and 'ITEM(Single)' in question.structure:
        raise Exception ('ITEM(Single) und ITEM(Multiple) gemischt in Frage: ', q_count+1)
    # Test more Information:
    if 'MORE_INFORMATION' in question.structure and not '_' in question.texts[np.where(question.structure == 'MORE_INFORMATION')][0]:
        raise Exception ('More information field is missing a title in Question:', q_count+1)
    # Test formatting
    for text in question.texts:
        if isinstance(text, str):
            if '<br>' in text or '<strong>' in text:
                formatting_flag = 1
    # Test empty Text
    needs_text_array = ['SUB_TITEL','PARAGRAPH','AUDIO', 'IMAGE', 'MORE_INFORMATION', 'MORE_INFORMATION_EXPANDED', 'ITEM(Single)', 'ITEM(Multiple)','SCALA', 'REFERENCE', 'Etappen-Titel','Zeit min','Zeit max']
    for i,text in enumerate(question.texts):
        # if nan
        # check if text is str
        if not isinstance(text, str) or (isinstance(text, str) and text == 'nan'):
                # if it needs some text
                if question.structure[i] in needs_text_array: #and not isinstance(question.structure[i], str):
                    raise Exception ('There is a text field missing at question: ', q_count+1)
    # Test Neue Etappe
    if 'Neue Etappe' in question.structure:
        if not 'Etappen-Titel' in question.structure:
            raise Exception ('Etappen-Titel missing at question: ', q_count+1)
        elif not 'Zeit min' in question.structure:
            raise Exception ('Zeit min missing at question: ', q_count+1)
        elif not 'Zeit max' in question.structure:
            raise Exception ('Zeit max missing at question: ', q_count+1)
        
    # Test References only for key insights
#    if 'REFERENCE' in question.structure and not question.texts[np.where(question.structure == 'REFERENCE')][0].isupper():
#        raise Exception ('Key Insight key missing or incorrect in Reference of question', q_count+1)
        
    # Test Short trip and Neue etappe
    if 'Neue Etappe' in question.structure and information[0] == 'SHORT_TRIP':
        raise Exception ('It is not possible to a create a neue etappe in a Short trip. Around position: ', q_count+1)
    
if formatting_flag == 0:
    raise Exception ('Not formatted')



# ---------- TEXT FORMATIERUNG ---------
for question in questions_array:
    for i, text in enumerate(question.texts):
        if not pd.isnull(text):
            # find " and replace with \"
            # find breaks and delete them
            question.texts[i] = text.replace('"', '\\"').replace('\n', '')

# ---------- PROGRESS -------
number_questions = len(questions_array)
progress_steps = round(90/number_questions)
progress = progress_steps
for question in questions_array:
    question.progress = progress
    progress += progress_steps


# -------- WRITE FILE -------------------------------------

with open(os.path.join(sys.path[0], name_of_json_file+".json"), 'w+') as file:

    # BEGINNING
    if write_beginning:    
        file.write(create_beginning(id, version, journey_key, information))

    count = 0
    for i, question in enumerate(questions_array): 
        # set back count for Neue Etappe
        if question.type ==  'Neue Etappe':
            count = -1
            etappe += 1
        
        # calculate id base
        id_base = id+version+"-"+str(etappe)+"-"+str(startnumber+count)
        id_base_next_question = '"'+id+version+"-"+str(etappe)+"-"+str(startnumber+count+1)+'"'   

        # WRITE & remove comma for the last entry
        if i == (len(questions_array)-1):
            id_base_next_question = 'null'
            file.write(create_question(question, id_base, count, write_beginning, id_base_next_question, id, version, etappe)[:-1])
        elif i < (len(questions_array)-1):
            if questions_array[i+1].type == 'Neue Etappe':
                id_base_next_question = 'null'
                file.write(create_question(question, id_base, count, write_beginning, id_base_next_question, id, version, etappe)[:-1])
            else:
                file.write(create_question(question, id_base, count, write_beginning, id_base_next_question, id, version, etappe))
        
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