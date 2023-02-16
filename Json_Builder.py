import os
import sys
from content_block_functions import *
from question_block_functions import *
from question_object import *
# 
#  ------ VARIABLES ------------------------------------
# Auszufüllen
name_of_json_file = "Nein_Sagen_weitere_Screens"
journey_key = "Test_Short_Trip_Flora"
id = "flora-v"
version = str(5)
write_beginning = False
write_ending = False
# CONTENT, OPTION_QUESTION, OPEN_QUESTION, SCALA_SLIDER, ITEM_LIST_EXPANDABLE (T or C as answeroption), ITEM_LIST_SINGLE_CHOICE (type needed)
# + CONTEN_BLOCK: P = Paragraph, R = Referenz, I = Image, A = Audio, M = More Information Expandable -> Titel ist immer dabei
# + ANSWER_OPTION_BLOCK: R = Radio Button, C = Checkbox, T = Text_Field_Expandable
# + NEXT_LOGIC_TYPE: NEXT, NEXT_OPTION
# + NEXT_LOGICS: N = option with next
# TODO: Scala Slider with next statt value
question_array = [Question('ITEM_LIST_SINGLE_CHOICE')]
etappe = "-1-"
startnumber = 0 # 0 if it should start from beginning

# -------- TESTS --------

for question in question_array:
    # check for questions which need certain configurations
    if question.type == 'ITEM_LIST_EXPANDABLE' and question.answer_option == None:
        raise Exception("Sorry, ITEM_LIST_EXPANDABLE needs a Checkbox (C) or Textfield_expandable (T)")   

    # TODO: Gibt es ein ITEM_LIST_SINGLE_CHOICE ohne answer_options? 

    # check if next_option that there are options     
    if question.next_logic_type == 'NEXT_OPTION' and question.next_logic_options == None:
        raise Exception("Sorry, a NEXT_OPTION logic needs next_options e.g. 'N'")   

    # check for missspellings
    if question.type not in ["CONTENT", "OPTION_QUESTION", "OPEN_QUESTION", "SCALA_SLIDER", "ITEM_LIST_EXPANDABLE", "ITEM_LIST_SINGLE_CHOICE"]:
        raise Exception("Sorry, there is a missspelling in " + question.type)



# -------- WRITE FILE -------------------------------------

with open(os.path.join(sys.path[0], name_of_json_file+".json"), 'w+') as file:

    # BEGINNING
    if write_beginning:    
        file.write(create_beginning(id, version, journey_key))

    for count, question in enumerate(question_array): 
        id_base = id+version+etappe+str(startnumber+count)       

        # WRITE & remove comma for the last entry
        if count == (len(question_array)-1):
            file.write(create_question(question.type, id_base, count, write_beginning, question.content, question.answer_option, question.next_logic_options, question.next_logic_type)[:-1])
        else:
            file.write(create_question(question.type, id_base, count, write_beginning, question.content, question.answer_option, question.next_logic_options, question.next_logic_type))

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