import re
import numpy as np

def are_all_information_there(information, information_en, english_translation):
    # Check if all information fields are there
    for i,info in enumerate(information):
        if i > 15:
            break
        if info == 'None':
            raise Exception('There is some starting information missing')
        
    # Test Oase zuordnung
    if information[1] == 'None':
          raise Exception ('OASE Zuordnung missing')
    
    if english_translation:
        for i in range(2,5):
            if information_en[i] == 'None':
                raise Exception('Some englisch Information missing')
    
def test_aufruf(information, information_en, english_translation):
    # Test Aufruf
    if information[0] == 'WORLD' and information[4] == 'Beginne deinen Kurztrip':
        raise Exception ('Aufruf passt nicht zur Reise')
    elif information[0] == 'SHORT_TRIP' and information[4] == 'Etappenweise zum Ziel':
        raise Exception ('Aufruf passt nicht zum Kurztrip')
    
    if english_translation:
        if information[0] == 'WORLD' and information_en[4] == 'Start your short trip':
            raise Exception ('Englischer Aufruf passt nicht zur Reise')
        elif information[0] == 'SHORT_TRIP' and information[4] == 'Step-by-step towards your goal':
            raise Exception ('Englischer Aufruf passt nicht zum Kurztrip')
        
def do_scala_test(question):
    # Define the regular expression pattern
    pattern = r"(\d+)\s*\((\w+\s*\w+)\)\s*-\s*(\d+)\s*\((\w+\s*\w+)\)"
    if 'SCALA' in question.structure and not re.match(pattern, question.texts[np.where(question.structure == 'SCALA')][0]):
        raise Exception ('Scala Text is not correct: ', question.texts[np.where(question.structure == 'SCALA')][0])
    if question.english_translation:
        if 'SCALA' in question.structure and not re.match(pattern, question.texts_en[np.where(question.structure == 'SCALA')][0]):
            raise Exception ('English Scala Text is not correct: ', question.texts_en[np.where(question.structure == 'SCALA')][0])

def test_for_all_english_translations(trip):
    english_translation_needed = ['SUB_TITEL','PARAGRAPH','AUDIO', 'IMAGE', 'SMALL_IMAGE', 'MORE_INFORMATION', 'MORE_INFORMATION_EXPANDED', 'ITEM(Single)', 'ITEM(Multiple)','SCALA', 'Etappen-Titel']
    for q, question in enumerate(trip.all_questions_array):
        for i, struc in enumerate(question.structure):
            text = question.texts_en[i]
            if struc in english_translation_needed and (not isinstance(text, str) or (isinstance(text, str) and text == 'None')):
                raise Exception ('English translation missing at question: ', q+1)


def do_tests(df, information, questions_array):

    # Flag declarations
    is_formatted = False

    # Test nummeration
    nummeration = []
    pattern = '^\d+\.\d+$'
    for column in df.columns:
        if column == None:
            break
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
                    is_formatted = True
        
        # Test empty Text
        needs_text_array = ['SUB_TITEL','PARAGRAPH','AUDIO', 'IMAGE', 'SMALL_IMAGE', 'MORE_INFORMATION', 'MORE_INFORMATION_EXPANDED', 'ITEM(Single)', 'ITEM(Multiple)','SCALA', 'REFERENCE', 'Etappen-Titel','Zeit min','Zeit max', 'KEY INSIGHT (optional)','KEY INSIGHT (verpflichtend)']
        for i,text in enumerate(question.texts):
            # if nan
            # check if text is str
            if not isinstance(text, str) or (isinstance(text, str) and text == 'None'):
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
            raise Exception ('It is not possible to a create a neue etappe in a Short trip. Around position: ', q_count+1)
        
        # test "sonst" und "und" in einer ref
        for text in question.texts:
            if "sonst" in text and "und" in text:
                raise Exception('"und" and "sonst" not possible in one reference at question: ', q_count+1)

        
    if not is_formatted:
        raise Exception ('Text not formatted')
