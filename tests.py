import re
import numpy as np
import pandas as pd

def do_tests(df, information, questions_array):

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
