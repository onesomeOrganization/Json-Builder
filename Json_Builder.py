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
etappe = "-1-"
startnumber = 1 # 1 if it should start from beginning
excel_path_or_name = "Jsons/Json Builder/Templates/23_05_08_Json_Excel_Template_Refs.xlsx"

# -------- EXPLANATIONS ----------
# type: CONTENT, OPTION_QUESTION, OPEN_QUESTION, SCALA_SLIDER, ITEM_LIST_EXPANDABLE (T OR C as answeroption), ITEM_LIST_SINGLE_CHOICE (R)
# content: P = Paragraph, R = Referenz, I = Image, A = Audio, M = More Information Expandable -> Titel ist immer dabei
# answer_option: R = Radio Button, C = Checkbox, T = Text_Field_Expandable
# next_logic_type: NEXT, NEXT_OPTION, REF_KEY_INSIGHT
# next_logic_options: N = option with next

# --------- TO DO --------------
# DONE: neue Etape brauch immer Etappenbeschreibung un dZeit min und Zeit max
# DONE: Etappenweise zum ziel /Starte deinen Kurztrip
# DONE: topicID
# DONE: shorttrip/world
# DONE: Bei kurztrip keine "neue Etappe" möglich
# DONE: Aus den tests ausnehmen
# TODO: Remove komma for last entry in etappe
# TODO: Count überlegen

# question_array = [Question('CONTENT','AM'),Question('SCALA_SLIDER','PRPM'), Question('OPTION_QUESTION','PRP'), Question('CONTENT'), Question('CONTENT'), Question('OPEN_QUESTION','PRP'), Question('SCALA_SLIDER'), Question('CONTENT','PR'), Question('OPEN_QUESTION','PRP'), Question('OPTION_QUESTION'), Question('CONTENT'), Question('CONTENT'), Question('CONTENT')]


# --------- EXCEL ---------

df = pd.read_excel(excel_path_or_name)


# get first informations and set defaults
information = df.iloc[:, 1]
if information[0] == 'Reise' or information[0] == 'reise':
    information[0] = 'WORLD'
    information[1] = '"'+information[1]+'"'
elif information[0] == 'Kurztrip' or information[0] == 'kurztrip':
    information[0] = 'SHORT_TRIP'
    information[1] = 'null'


# drop the first two columns
df = df.drop(df.columns[[0, 1]], axis=1)

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
    if not question.structure[0] == 'SUB_TITEL' or 'Neue Etappe':
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
    needs_text_array = ['SUB_TITEL','PARAGRAPH','AUDIO', 'IMAGE', 'MORE_INFORMATION', 'MORE_INFORMATION_EXPANDED', 'ITEM(Single)', 'ITEM(Multiple)','SCALA', 'Etappen-Titel','Zeit min','Zeit max']
    for i,text in enumerate(question.texts):
        # if nan
        if not isinstance(text, str):
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
        
    # Test Short trip and Neue etappe
    if 'Neue Etappe' in question.structure and information[0] == 'SHORT_TRIP':
        raise Exception ('It is not possible to a create a neue etappe at: ', q_count+1)
    
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

    for count, question in enumerate(questions_array): 
        id_base = id+version+etappe+str(startnumber+count)
        id_base_next_question = id+version+etappe+str(startnumber+count+1)   

        # WRITE & remove comma for the last entry
        if count == (len(questions_array)-1):
            file.write(create_question(question, id_base, count, write_beginning, id_base_next_question, id, version, etappe)[:-1])
        else:
            file.write(create_question(question, id_base, count, write_beginning, id_base_next_question, id, version, etappe))

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