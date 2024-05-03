import re
import numpy as np
from helper import add_quotation_mark, normal_screen_reference, nextLogic_patterns, key_insight_pattern, referencable_structure_content

# ------- TRIP TESTS ----------------

def are_all_information_there(information, information_en, english_translation):
    lengths_of_infos_every_trip_needs = 14
    lengths_of_infos_only_worlds_need = 25
    # Check if all information fields are there
    for i,info in enumerate(information):
        if information[0] == 'Kurztrip' or information[0] == 'kurztrip' and i > lengths_of_infos_every_trip_needs:
            break
        if i > lengths_of_infos_only_worlds_need:
            break
        if info == 'None':
            raise Exception('There is some starting information missing in the first column')
        
    # Test Oase zuordnung
    if information[1] == 'None':
          raise Exception ('OASE Zuordnung missing')
    
    if english_translation:
        for i in range(2,5):
            if information_en[i] == 'None':
                raise Exception('Some englisch Information is missing in the first column')
        if information[0] == 'Reise' or information[0] == 'reise':
            for i in range(16,25):
                if information_en[i] == 'None':
                    raise Exception('Some englisch Information is missing in the first column')
    
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
        print('WARNING: The questions have no formating at all - is this correct?')

def test_nummeration(questions_array):
    nummeration = []
    
    for question in questions_array:
        if 'x' in question.excel_id:
            print('''
-----------------------------------------------------------------------------------------------------------------------
|  !!!! WARNING !!!! - x in Nummeration: Wurde auf korrekte Verknüpfung davor und danach geachtet (weiter mit Screen)? |
-----------------------------------------------------------------------------------------------------------------------
                    ''')    
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
        
def test_for_text_without_structure(question):
    for i, text in enumerate(question.texts):
        if text != 'None':
            if question.structure[i] == 'None':
                raise Exception ('There is a structure field missing at question: ', question.excel_id)

    
def do_tests_on_questions(question):
    test_subtitle(question)
    test_kein_item_multiple_and_single(question)
    test_more_information_title(question)
    test_empty_text(question)
    test_for_arrows_in_text(question)
    test_neue_etappe(question)
    test_sonst_und_in_ref(question)
    test_scala(question)
    test_nextLogics_texts(question)
    test_english_translation(question)
    test_for_added_information_english(question)
    test_if_ref_id_exists(question)
    test_for_correct_structure_type(question)
    test_for_key_insight_and_optional(question)
    test_for_arrow_missing_at_button_text(question)
    test_for_only_one_button(question)
    test_for_old_version_mistakes(question)


def test_subtitle(question):
    if not question.structure[0] == 'SUB_TITLE' and not question.structure[0] == 'Neue Etappe':
        raise Exception ('SUB_TITLE is missing for question ',question.excel_id)

def test_kein_item_multiple_and_single(question):
    if 'ITEM(Multiple)' in question.structure and 'ITEM(Single)' in question.structure:
        raise Exception ('ITEM(Single) und ITEM(Multiple) gemischt in Frage: ', question.excel_id)

def test_more_information_title(question):
    if 'MORE_INFORMATION' in question.structure:
        indices = np.where(question.structure == 'MORE_INFORMATION')[0]
        if not all(question.texts[i].count('_') == 2 for i in indices):
            raise Exception ('More information field is missing a title or an underline in Question:', question.excel_id)
        if question.english_translation:
            if not all(question.texts_en[i].count('_') == 2 for i in indices):
                raise Exception ('English More information field is missing a title or an underline in Question:', question.excel_id)
    if 'MORE_INFORMATION_EXPANDED' in question.structure:
        indices = np.where(question.structure == 'MORE_INFORMATION_EXPANDED')[0]
        if not all(question.texts[i].count('_') == 2 for i in indices):
            raise Exception ('More information field is missing a title or an underline in Question:', question.excel_id)
        if question.english_translation:
            if not all(question.texts_en[i].count('_') == 2 for i in indices):
                raise Exception ('English More information field is missing a title or an underline in Question:', question.excel_id)

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
    pattern = r"(\d+)\s*\(([^)]+)\)\s*-\s*(\d+)\s*\(([^)]+)\)"
    if 'SCALA' in question.structure and not re.match(pattern, question.texts[np.where(question.structure == 'SCALA')][0]):
        raise Exception ('Scala Text is not correct at question ', question.excel_id)
    if question.english_translation:
        if 'SCALA' in question.structure and not re.match(pattern, question.texts_en[np.where(question.structure == 'SCALA')][0]):
            raise Exception ('English Scala Text is not correct at question: ', question.excel_id)
            
def test_nextLogics_texts(question):                 
    # REF_OPTION # REF_VALUE # REF_COUNT # VALUE
    if 'weiter mit Screen' in question.structure:
        text = question.texts[np.where(question.structure == 'weiter mit Screen')][0]
        if 'wenn' in text or 'Wenn' in text:
            if not re.match(nextLogic_patterns['REF_OPTION'], text) and not re.match(nextLogic_patterns['VALUE'], text) and not re.match(nextLogic_patterns['REF_COUNT'], text) and not re.match(nextLogic_patterns['REF_VALUE'], text) :
                raise Exception ('Weiter mit Screen text wrong at question: ', question.excel_id)
    
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
        if (struc == 'ITEM(Single)' and '->' in question.texts[num]) or (struc == 'ITEM(Multiple)' and '->' in question.texts[num] and question.maxNumber == '1') or (struc == 'BUTTON' and '->' in question.texts[num]):
            ref_id = question.texts[num].split('->')[1].strip()
            if not ref_id in question.trip.all_ids:
                raise Exception ('Reference id does not exist in this excel from question: ', question.excel_id)
        if struc == 'REFERENCE' and not ('sonst' in question.texts[num] or 'und' in question.texts[num]):
            ref_id = question.texts[num]
            if normal_screen_reference(ref_id) and not ref_id in question.trip.all_ids:
                raise Exception ('Reference id does not exist in this excel from question: ', question.excel_id)
        if struc == 'weiter mit Screen' and not 'wenn' in question.texts[num]:
            ref_id = question.texts[num]
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
        
            
def test_for_correct_structure_type(question):
    for num, struc in enumerate(question.structure):
        if struc == 'PARAGRAPH' and re.match(r'(\d+\.\d+)', question.texts[num]):
            print('''
                    --------------------------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! --- Should this really be a Paragraph at question %s containing a Reference? |
                    --------------------------------------------------------------------------------------------------
                    '''%(question.excel_id))
        if (struc == 'IMAGE' or struc == 'SMALL_IMAGE' or struc == 'AUDIO' or struc == 'PDF_DOWNLOAD') and len(question.texts[num].split(' '))>1:
            print('''
                    ---------------------------------------------------------------------------
                    |  !!!! WARNING !!!! --- Structure might be missplaced at question  %s |
                    ---------------------------------------------------------------------------
                    '''%(question.excel_id))
            
    if np.count_nonzero(question.structure == 'SUB_TITLE') > 1:
        raise Exception ('Two Subtitles at question: ', question.excel_id)
    
def test_for_key_insight_and_optional(question):
    if 'OPTIONAL' in question.structure and 'KEY INSIGHT (verpflichtend)' in question.structure:
        raise Exception ('A KEY INSIGHT (verpflichtend) should not be optional at question: ', question.excel_id)
    
def test_for_arrow_missing_at_button_text(question):
    if 'BUTTON' in question.structure:
        button_texts = question.texts[np.where(question.structure == 'BUTTON')]
        if not all('->' in text for text in button_texts):
            raise Exception (' Arrow in Button missing at question: ', question.excel_id)
    
def test_for_only_one_button(question):
    if np.sum(question.structure == "BUTTON") == 1:
        raise Exception ('Question has only one Button: ', question.excel_id)
    
def test_for_old_version_mistakes(question):
    for struc in question.structure:
        if struc == 'ANSWER OPTIONS FROM REFERENCE':
            raise Exception ('You are using an outdated json builder template. ANSWER OPTIONS FROM REFERENCE is outdated it must be ANSWER OPTIONS FROM REFERENCE (Single Choice) or ANSWER OPTIONS FROM REFERENCE (Multiple Choice) at question: ', question.excel_id)
    
            
# ------------ SONSTIGE TESTS ----------------

def test_if_any_scala_condition_is_missing(self, scala_condition_dict):
    test_array = [x for x in range(int(self.question.scala_min), int(self.question.scala_max) + 1)]
    for key in scala_condition_dict:
        if scala_condition_dict[key][0] == '=':
            test_array = [num for num in test_array if num not in scala_condition_dict[key][1]]
        if scala_condition_dict[key][0] == '>=':
            test_array = [num for num in test_array if num < scala_condition_dict[key][1][0]]
        if scala_condition_dict[key][0] == '<=':
            test_array = [num for num in test_array if num > scala_condition_dict[key][1][0]]
        if scala_condition_dict[key][0] == '>':
            test_array = [num for num in test_array if num <= scala_condition_dict[key][1][0]]
        if scala_condition_dict[key][0] == '<':
            test_array = [num for num in test_array if num >= scala_condition_dict[key][1][0]]
    if len(test_array) != 0:
        raise Exception ('Scala is missing some conditions at question ', self.question.excel_id, '; for value: ', test_array)
    

def test_for_escape_option_at_question_loop(exist_arrows, self):
    if not any(item[0] for item in exist_arrows) and 'Start Questionloop' in self.structure:
        raise Exception ('Escape option missing at question loop at question: ', self.question.excel_id)
    
def test_if_ref_question_is_optional(contentComponent):
    ref_id = contentComponent.refQuestionId
    questions_before = contentComponent.content.question.questions_before
    for q in questions_before:
        if add_quotation_mark(q.id) == ref_id and q.answer_required == 'false':
            print('''
                    --------------------------------------------------------------------------------
                    |  !!!! WARNING !!!! --- 'Referenz of an optional screen (%s) at question:    %s |
                    --------------------------------------------------------------------------------
                    '''%(q.excel_id, contentComponent.content.question.excel_id))
            
def test_if_question_has_something_to_reference(contentComponent):
    ref_id = contentComponent.refQuestionId
    questions_before = contentComponent.content.question.questions_before
    for q in questions_before:
        if add_quotation_mark(q.id) == ref_id:
            for struc in q.structure:
                if struc in referencable_structure_content:
                    return
            raise Exception ('Referenz of a screen which has nothing to reference (%s) at question: %s'%(q.excel_id, contentComponent.content.question.excel_id))
            
        
def test_if_button_texts_are_the_same(id, button_texts):
    if len(button_texts) != len(set(button_texts)):
        raise Exception ('Same Button texts at question: ', id)
    
def test_if_key_ref_exists(key, question):
    if not key in question.trip.all_ids:
        raise Exception ('Reference id ("%s") does not exist in this excel used in the "weiter mit Screen" from question: '%(key), question.excel_id)
    
def test_for_correct_key_insight(question, text):
   if not bool(re.match(key_insight_pattern, text.strip())):
    raise Exception ('Key insight is wrong at question %s. Maybe a typo?'%(question.excel_id))

