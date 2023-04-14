import os
import sys
from content_block_functions import *
from question_block_functions import *
from question_object import *
import pandas as pd
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
excel_path_or_name = "Jsons/Tests/Json_Excel_Template.xlsx"

# -------- EXPLANATIONS ----------
# type: CONTENT, OPTION_QUESTION, OPEN_QUESTION, SCALA_SLIDER, ITEM_LIST_EXPANDABLE (T OR C as answeroption), ITEM_LIST_SINGLE_CHOICE (R)
# content: P = Paragraph, R = Referenz, I = Image, A = Audio, M = More Information Expandable -> Titel ist immer dabei
# answer_option: R = Radio Button, C = Checkbox, T = Text_Field_Expandable
# next_logic_type: NEXT, NEXT_OPTION, REF_KEY_INSIGHT
# next_logic_options: N = option with next

# --------- TO DO --------------
# TODO: Scala Slider with next statt value und between als zusätzliche option
# TODO: Optional angebbar
# TODO: Einzelne Questions sind einzelne Objects die von Question erben
# TODO: Next_logic_type: Next_option -> bei nicht linearer json
        # TODO: Gibt es single choice plus expandable textfield?
        # TODO: Englisch text
        # TODO: Start titel & Infos als extra fragetyp bzw am anfang zum eintragen
        # TODO: More information title
# question_array = [Question('CONTENT','AM'),Question('SCALA_SLIDER','PRPM'), Question('OPTION_QUESTION','PRP'), Question('CONTENT'), Question('CONTENT'), Question('OPEN_QUESTION','PRP'), Question('SCALA_SLIDER'), Question('CONTENT','PR'), Question('OPEN_QUESTION','PRP'), Question('OPTION_QUESTION'), Question('CONTENT'), Question('CONTENT'), Question('CONTENT')]


# -------- TESTS --------
# TODO: Test if Item Multi together with "Antwortmöglichkiet" -> geht nur mit Mehreren Antw.
# TODO: no <strong> or <br> -> nachfragen ob formatiert wurde
# TODO: immer mit subtitle starten
# TODO: kein item single und item multiple in einer frage

'''
for question in question_array:
    # check for questions which need certain configurations
    if question.type == 'ITEM_LIST_EXPANDABLE' and question.answer_option == None:
        raise Exception("Sorry, ITEM_LIST_EXPANDABLE needs a Checkbox (C) or Textfield_expandable (T)")  

    if question.type == 'ITEM_LIST_EXPANDABLE' and 'T' in question.answer_option and 'C' in question.answer_option:
        raise Exception("Sorry, ITEM_LIST_EXPANDABLE does not work with Checkbox (C) AND Textfield_expandable (T), only one possible")  

    # TODO: Gibt es ein ITEM_LIST_SINGLE_CHOICE ohne answer_options? 

    # check if next_option that there are options     
    if question.next_logic_type == 'NEXT_OPTION' and question.next_logic_option == None:
        raise Exception("Sorry, a NEXT_OPTION logic needs next_options e.g. 'N'")   

    # check for missspellings
    if question.type not in ["CONTENT", "OPTION_QUESTION", "OPEN_QUESTION", "SCALA_SLIDER", "ITEM_LIST_EXPANDABLE", "ITEM_LIST_SINGLE_CHOICE"]:
        raise Exception("Sorry, there is a missspelling in " + question.type)
    
'''

# --------- EXCEL ---------

df = pd.read_excel(excel_path_or_name)

# save always two arrays into the Question object with structure and texts respectively
questions_array = []
for i in range(0, len(df.columns), 2):
    questions_array.append(Question(df.iloc[:, i], df.iloc[:, i+1]))


# ---------- TEXT FORMATIERUNG ---------
for question in questions_array:
    for i, text in enumerate(question.texts):
        if not pd.isnull(text):
            # find " and replace with \"
            # find breaks and delete them
            question.texts[i] = text.replace('"', '\\"').replace('\n', '')
        


# -------- WRITE FILE -------------------------------------

with open(os.path.join(sys.path[0], name_of_json_file+".json"), 'w+') as file:

    # BEGINNING
    if write_beginning:    
        file.write(create_beginning(id, version, journey_key))

    for count, question in enumerate(questions_array): 
        id_base = id+version+etappe+str(startnumber+count)
        id_base_next_question = id+version+etappe+str(startnumber+count+1)   

        # WRITE & remove comma for the last entry
        if count == (len(questions_array)-1):
            file.write(create_question(question.type, id_base, count, write_beginning, question.content, question.answer_option, question.next_logic_option, question.next_logic_type, question.texts, id_base_next_question)[:-1])
        else:
            file.write(create_question(question.type, id_base, count, write_beginning, question.content, question.answer_option, question.next_logic_option, question.next_logic_type, question.texts, id_base_next_question))

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