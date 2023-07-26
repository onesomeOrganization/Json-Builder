import re
import numpy as np

# ------- TRIP TESTS ----------------

def are_all_information_there(information, information_en, english_translation):
    # Check if all information fields are there
    for i,info in enumerate(information):
        if i > 14:
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
        
    # Test cardDisplayImageName
    if information[15] == 'None' and information[0] == 'WORLD':
        raise Exception ('cardDisplayImageName Zuordnung missing')
    

def do_tests_for_question_array(trip):
    test_formatting(trip.all_questions_array)
    if not trip.nummeration_is_not_correct:
        test_nummeration(trip.all_questions_array)

def test_formatting(questions_array):
    # Flag declarations
    is_formatted = False

    for question in questions_array:
        for text in question.texts:
                if isinstance(text, str):
                    if '<br>' in text or '<strong>' in text:
                        is_formatted = True
    if not is_formatted:
        raise Exception('WARNING: The questions have no formating at all - is this correct?')

def test_nummeration(questions_array):
    nummeration = []
    
    for question in questions_array:
        if 'x' in question.excel_id:
            continue
        else:
            nummeration.append(question.excel_id)

    
    for i, number in enumerate(nummeration):
        if i == len(nummeration)-1:
            break
        splits = number.split('.')
        # first number has to be the same and second counting or first number counting and second a 1
        if splits[0] == nummeration[i+1].split('.')[0] and int(splits[1])+1 == int(nummeration[i+1].split('.')[1]):
            continue
        elif int(splits[0])+1 == int(nummeration[i+1].split('.')[0]) and nummeration[i+1].split('.')[1] == '0':
            continue
        else:
            raise Exception ('Nummeration is wrong after: ', number)
    

# ----------- QUESTION TESTS -----------------    

def test_if_id_exists(question):
    if question.excel_id is None:
        if len(question.questions_before) != 0:
            raise Exception ('Id missing after question with id: ', question.questions_before[-1].excel_id)  
        else:
            raise Exception ('Id missing at the first question') 

    
def do_tests_on_questions(question):
    test_subtitle(question)
    test_kein_item_multiple_and_single(question)
    test_more_information_title(question)
    test_empty_text(question)
    test_for_arrows_in_text(question)
    test_neue_etappe(question)
    test_sonst_und_in_ref(question)
    test_scala(question)
    test_wenn_condition(question)
    test_english_translation(question)
    test_for_added_information_english(question)
    test_if_ref_id_exists(question)
    test_arrow_missing(question)


def test_subtitle(question):
    if not question.structure[0] == 'SUB_TITLE' and not question.structure[0] == 'Neue Etappe':
        raise Exception ('SUB_TITLE is missing for question ',question.excel_id)

def test_kein_item_multiple_and_single(question):
    if 'ITEM(Multiple)' in question.structure and 'ITEM(Single)' in question.structure:
        raise Exception ('ITEM(Single) und ITEM(Multiple) gemischt in Frage: ', question.excel_id)

def test_more_information_title(question):
    if 'MORE_INFORMATION' in question.structure and not question.texts[np.where(question.structure == 'MORE_INFORMATION')][0].count('_') == 2:
        raise Exception ('More information field is missing a title or an underline in Question:', question.excel_id)
    if question.english_translation:
        if 'MORE_INFORMATION' in question.structure and not question.texts_en[np.where(question.structure == 'MORE_INFORMATION')][0].count('_') == 2:
            raise Exception ('English more information field is missing a title or an underline in Question:', question.excel_id)
    if 'MORE_INFORMATION_EXPANDED' in question.structure and not question.texts[np.where(question.structure == 'MORE_INFORMATION_EXPANDED')][0].count('_') >= 2:
        raise Exception ('More information field is missing a title or an underline in Question:', question.excel_id)
    if question.english_translation:
        if 'MORE_INFORMATION_EXPANDED' in question.structure and not question.texts_en[np.where(question.structure == 'MORE_INFORMATION_EXPANDED')][0].count('_') == 2:
            raise Exception ('English more information field is missing a title or an underline in Question:', question.excel_id)

def test_empty_text(question):
    needs_text_array = ['SUB_TITLE','PARAGRAPH','AUDIO', 'IMAGE', 'SMALL_IMAGE', 'MORE_INFORMATION', 'MORE_INFORMATION_EXPANDED', 'ITEM(Single)', 'ITEM(Multiple)','SCALA', 'REFERENCE', 'KEY INSIGHT (optional)','KEY INSIGHT (verpflichtend)', 'Etappen-Titel', 'Zeit min', 'Zeit max','BUTTON', 'weiter mit Screen']
    for i,text in enumerate(question.texts):
        # if nan
        # check if text is str
        if not isinstance(text, str) or (isinstance(text, str) and text == 'None'):
                # if it needs some text
                if question.structure[i] in needs_text_array: #and not isinstance(question.structure[i], str):
                    raise Exception ('There is a text field missing at question: ', question.excel_id)

def test_for_arrows_in_text(question):
    should_not_contain_arrows = ['SUB_TITLE','PARAGRAPH','AUDIO', 'IMAGE', 'SMALL_IMAGE', 'MORE_INFORMATION', 'MORE_INFORMATION_EXPANDED','SCALA', 'KEY INSIGHT (optional)','KEY INSIGHT (verpflichtend)', 'Etappen-Titel', 'Zeit min', 'Zeit max', 'weiter mit Screen']
    for i,text in enumerate(question.texts):
        if '->' in text and question.structure[i] in should_not_contain_arrows:
            print('''
                    ----------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! --- Arrow in textfield: might cause damage -> check question |
                    ----------------------------------------------------------------------------------
                    ''')
            print('question id :', question.excel_id)
            

def test_neue_etappe(question):
    if 'Neue Etappe' in question.structure:
        if question.trip.type == 'SHORT_TRIP':
            raise Exception ('It is not possible to a create a neue etappe in a Short trip. Around position: ',question.excel_id)
        if not 'Etappen-Titel' in question.structure:
            raise Exception ('Etappen-Titel missing at question: ', question.excel_id)
        elif not 'Zeit min' in question.structure:
            raise Exception ('Zeit min missing at question: ', question.excel_id)
        elif not 'Zeit max' in question.structure:
            raise Exception ('Zeit max missing at question: ', question.excel_id)
        
def test_sonst_und_in_ref(question):
    for text in question.texts:
        if "sonst" in text and "und" in text:
            raise Exception('"und" and "sonst" not possible in one reference at question: ', question.excel_id)
        
def test_scala(question):
    # Define the regular expression pattern
    pattern = r"(\d+)\s*\((\s*\w+(\s+\w+)*)\)\s*-\s*(\d+)\s*\((\s*\w+(\s+\w+)*)\)"

    if 'SCALA' in question.structure and not re.match(pattern, question.texts[np.where(question.structure == 'SCALA')][0]):
        raise Exception ('Scala Text is not correct at question ', question.excel_id)
    if question.english_translation:
        if 'SCALA' in question.structure and not re.match(pattern, question.texts_en[np.where(question.structure == 'SCALA')][0]):
            raise Exception ('English Scala Text is not correct at question: ', question.excel_id)
        
def test_wenn_condition(question):
    wenn_condition_pattern = r'(\d+\.\d+)\s*\(\s*wenn\s+(\d+\.\d+)\s*=\s*(.*?)\)'
    scala_condition_pattern = r'(\d+\.\d+)\s*\((.*?)\)'
    for text in question.texts:
        if '(wenn' in text or '( wenn' in text:
            if not re.match(wenn_condition_pattern, text) and not re.match(scala_condition_pattern, text):
                raise Exception ('Wenn condition is incorrect at question: ', question.excel_id)
        
def test_english_translation(question):
    if question.english_translation:
        english_translation_needed = ['SUB_TITLE','PARAGRAPH','AUDIO', 'IMAGE', 'SMALL_IMAGE', 'MORE_INFORMATION', 'MORE_INFORMATION_EXPANDED', 'ITEM(Single)', 'ITEM(Multiple)','SCALA', 'Etappen-Titel']
        for i, struc in enumerate(question.structure):
            text = question.texts_en[i]
            if struc in english_translation_needed and (not isinstance(text, str) or (isinstance(text, str) and text == 'None')):
                raise Exception ('English translation missing at question: ', question.excel_id)
        
def test_for_added_information_english(question):
    if question.english_translation:
        for i, struc in enumerate(question.structure):
            if struc == 'ITEM(Single)' or struc == 'ITEM(Multiple)':
                if ('i =' in question.texts[i] or 'i=' in question.texts[i]) and not ('i =' in question.texts_en[i] or 'i=' in question.texts_en[i]):
                    raise Exception ('"i=" information missing in english text at question: ', question.excel_id)
            

def test_if_ref_id_exists(question):
    # next option items with ->
    for num, struc in enumerate(question.structure):
        if (struc == 'ITEM(Single)' and '->' in question.texts[num]) or (struc == 'ITEM(Multiple)' and '->' in question.texts[num] and question.maxNumber == '1'):
            ref_id = question.texts[num].split('->')[1].strip()
            if not ref_id in question.trip.all_ids:
                raise Exception ('Reference id does not exist in this excel from question: ', question.excel_id)
            
def test_arrow_missing(question):
    # next option items with ->
    should_have_arrows = False
    for num, struc in enumerate(question.structure):
        if (struc == 'ITEM(Single)' and '->' in question.texts[num]) or (struc == 'ITEM(Multiple)' and '->' in question.texts[num] and question.maxNumber == '1'):
            should_have_arrows = True
    for num, struc in enumerate(question.structure):
        if (struc == 'ITEM(Single)' or struc == 'ITEM(Multiple)') and not '->' in question.texts[num] and should_have_arrows:
            raise Exception('Arrow missing at question: ', question.excel_id)
