
import numpy as np

def create_etappen_array(etappe, questions_array):
    etappen_questions_array = []
    for question in questions_array:
        if question.id.split('.')[0] == etappe:
            etappen_questions_array.append(question)
    return etappen_questions_array


def create_progress(etappen_questions_array, type, number_questions_until_letzter_screen, splitscreen_number, count_branch, connectionscreen_number):
    if type == 'straight' or type == 'straight_with_insertion':
        total = len(etappen_questions_array)
        progress_steps = round(90/total)
        progress = progress_steps
        for question in etappen_questions_array:
            question.progress = progress
            progress += progress_steps

    elif type == 'two_parallels':
         # two parallel arms which do not connect 
        total = number_questions_until_letzter_screen
        progress_steps = round(90/total)
        progress = progress_steps
        for question in etappen_questions_array:
            question.progress = progress
            progress += progress_steps
            # check for "letzter Screen"
            if "letzter Screen" in question.structure:
                progress = (splitscreen_number)*progress_steps
            
    
    elif type == 'two_connecting':
        # two parallel arms which connect again
        total = number_questions_until_letzter_screen
        progress_steps = round(90/total)
        progress = progress_steps
        for question in etappen_questions_array:
            question.progress = progress
            progress += progress_steps
            # check for "letzter Screen"
            if "letzter Screen" in question.structure:
                progress = (splitscreen_number)*progress_steps
                progress_steps = round(((connectionscreen_number-splitscreen_number)*progress_steps)/count_branch)
            
    else:
        raise Exception ('Progress type not known')
    
    return etappen_questions_array

    
def check_for_progress_type(etappen_questions_array):
    # flags
    letzter_screen_flag = 0
    weiter_screen_flag = 0
    not_straight_flag = 0

    # variables
    number_questions_until_letzter_screen = 0
    splitscreen_number = 0
    count_branch = 0
    connectionscreen_number = 0
    

    # check through questions
    for num, question in enumerate(etappen_questions_array):
        for text in question.texts:
            if "->" in text:
                not_straight_flag = 1
                splitscreen_number = num+1
        if 'letzter Screen' in question.structure:
            letzter_screen_flag = 1
            number_questions_until_letzter_screen = num+1
        elif 'weiter mit Screen' in question.structure:
            weiter_screen_flag = 1
            connectionscreen_number = int(question.texts[np.where(question.structure == 'weiter mit Screen')][0].split('.')[1])

    count_branch = len(etappen_questions_array) - number_questions_until_letzter_screen
    # Type
    if not_straight_flag == 0:
        type = 'straight'
    if not_straight_flag == 1 and weiter_screen_flag == 0:
        type = 'straight_with_insertion'
    if not_straight_flag == 1 and weiter_screen_flag == 0 and letzter_screen_flag == 1:
        type = 'two_parallels'
    if not_straight_flag == 1 and weiter_screen_flag == 1 and letzter_screen_flag == 1:
        type = 'two_connecting'


    return type, number_questions_until_letzter_screen, splitscreen_number, count_branch, connectionscreen_number