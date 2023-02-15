import os
import sys
from content_block_functions import *
from question_block_functions import *
# 
#  ------ VARIABLES ------------------------------------
# Auszufüllen
name_of_json_file = "Nein_Sagen_weitere_Screens"
journey_key = "Test_Short_Trip_Flora"
id = "flora-v"
version = str(5)
write_beginning = False
write_ending = False
# CONTENT, OPTION_QUESTION, OPEN_QUESTION, SCALA_SLIDER, ITEM_LIST_EXPANDABLE (T or C as answeroption), AUDIO, ITEM_LIST_SINGLE_CHOICE (next logic type needed)
# + CONTEN_BLOCK: P = Paragraph, R = Referenz, I = Image, A = Audio, M = More Information Expandable -> Titel ist immer dabei
# + ANSWER_OPTION_BLOCK: R = Radio Button, C = Checkbox, T = Text_Field_Expandable
# TODO: default should be NEXT
# TODO: create VALUE
# + NEXT_LOGIC_TYPE: NEXT, NEXT_OPTION, VALUE
# TODO: Next_Option should be part of nextlogic type
# + Options: N = option with next, V = option with value GTE LT
questions_array  = ["SCALA_SLIDER+PRP+VALUE+V" ] #"ITEM_LIST_SINGLE_CHOICE+P+CC+NEXT_OPTION+NN"
etappe = "-2-"
startnumber = 0 # 0 if it should start from beginning

# -------- TESTS --------

yes = {'yes','y', 'ye', ''}
no = {'no','n'}

for entry in questions_array:
    question_split = entry.split("+")

    # check for questions which need certain configurations
    if question_split[0] == 'ITEM_LIST_EXPANDABLE' and len(question_split) < 3:
        raise Exception("Sorry, ITEM_LIST_EXPANDABLE needs a Checkbox (C) or Textfield_expandable (T)")

    # check for paragraphs
    if 'P' not in question_split[1] or len(question_split) < 2:
        sys.stdout.write("Are you sure you don't want a Paragraph in " + entry + " :")
        choice = input().lower()
        if choice in yes:
            continue
        elif choice in no:
            raise Exception("You are missing a Paragraph in "+ entry)
        else:
            sys.stdout.write("Please respond with 'yes' or 'no'")

    # TODO: check for missspellings



# -------- WRITE FILE -------------------------------------

with open(os.path.join(sys.path[0], name_of_json_file+".json"), 'w+') as file:

    # BEGINNING
    if write_beginning:    
        file.write(create_beginning(id, version, journey_key))

    # CREATE QUESTION_TYPES WITH CONTENT BLOCK
    for count, entry in enumerate(questions_array):
        id_base = id+version+etappe+str(startnumber+count)

        # split into question and ref
        if "+" not in entry:
            entry = entry + "+"

        question_split = entry.split("+")
        question = question_split[0]
        contents = question_split[1]
        if len(question_split) > 2:
            answer_options = question_split[2]
        else: 
            answer_options = None
        if len(question_split) > 3:
            next_logic_type = question_split[3]
        else:
            next_logic_type = "NEXT"
        if len(question_split) > 4:
            next_logics = question_split[4]
        else: 
            next_logics = None

        # WRITE & remove comma for the last entry
        if count == (len(questions_array)-1):
            file.write(create_question(question, id_base, count, write_beginning, contents, answer_options, next_logics, next_logic_type)[:-1])
        else:
            file.write(create_question(question, id_base, count, write_beginning, contents, answer_options, next_logics, next_logic_type))

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