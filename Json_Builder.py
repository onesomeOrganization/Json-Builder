import os
import sys
from content_block_functions import *
from question_block_functions import *
from question_object import *
# 
#  ------ VARIABLES ------------------------------------
# Auszufüllen
name_of_json_file = "Resilienz_weitere_screens"
journey_key = "Test_Short_Trip_Flora"
id = "flora-v"
version = str(6)
write_beginning = False
write_ending = False
# type: CONTENT, OPTION_QUESTION, OPEN_QUESTION, SCALA_SLIDER, ITEM_LIST_EXPANDABLE (T OR C as answeroption), ITEM_LIST_SINGLE_CHOICE (R)
# content: P = Paragraph, R = Referenz, I = Image, A = Audio, M = More Information Expandable -> Titel ist immer dabei
# answer_option: R = Radio Button, C = Checkbox, T = Text_Field_Expandable
# next_logic_type: NEXT, NEXT_OPTION, REF_KEY_INSIGHT
# next_logic_options: N = option with next
# TODO: Scala Slider with next statt value und between als zusätzliche option
# question_array = [Question('CONTENT','AM'),Question('SCALA_SLIDER','PRPM'), Question('OPTION_QUESTION','PRP'), Question('CONTENT'), Question('CONTENT'), Question('OPEN_QUESTION','PRP'), Question('SCALA_SLIDER'), Question('CONTENT','PR'), Question('OPEN_QUESTION','PRP'), Question('OPTION_QUESTION'), Question('CONTENT'), Question('CONTENT'), Question('CONTENT')]
question_array = [Question('CONTENT', next_logic_type='REF_KEY_INSIGHT')]
etappe = "-2-"
startnumber = 17 # 0 if it should start from beginning

# -------- TESTS --------

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
    



# -------- WRITE FILE -------------------------------------

with open(os.path.join(sys.path[0], name_of_json_file+".json"), 'w+') as file:

    # BEGINNING
    if write_beginning:    
        file.write(create_beginning(id, version, journey_key))

    for count, question in enumerate(question_array): 
        id_base = id+version+etappe+str(startnumber+count)       

        # WRITE & remove comma for the last entry
        if count == (len(question_array)-1):
            file.write(create_question(question.type, id_base, count, write_beginning, question.content, question.answer_option, question.next_logic_option, question.next_logic_type)[:-1])
        else:
            file.write(create_question(question.type, id_base, count, write_beginning, question.content, question.answer_option, question.next_logic_option, question.next_logic_type))

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