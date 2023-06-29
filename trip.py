from question_object import Question
from tests import do_tests
from progress import create_progress
import pandas as pd

def create_questions_array(self):
        questions_array = []
        for i in range(2, len(self.df.columns), 2): # start at 2 because of the information
            # Create a boolean mask to check if values are None
            mask = self.df.iloc[:, i] == 'None'
            # Check if all values in the column are None
            if mask.all():
                break
            questions_array.append(Question(self.id_base, self.version, self.df.iloc[:, i], self.df.iloc[:, i+1], self.df.iloc[:, i+2], self.df.iloc[:, i+3], self.df.columns[i], self.write_beginning, self.write_ending))
        return questions_array
'''
def check_inter_question_dependencies(self):
    # add next question references
    # loop through and add reference backward
    for i, question in enumerate(self.all_questions_array):
        for x, struct in enumerate(question.structure):
            # check if structure has reference
            if struct == 'REFERENCE':
                # check if key insight reference
                if question.texts[x].isupper():
                    # add to question before
                    self.all_questions_array[i-1].reference_of_next_question = question.texts[x]
                    self.all_questions_array[i-1].next_logic_type = 'REF_KEY_INSIGHT'
 '''               

def format_text(self):
    for question in self.all_questions_array:
        for i, text in enumerate(question.texts):
            if not pd.isnull(text):
            # find " and replace with \"
            # find breaks and delete them
                question.texts[i] = text.replace('"', '\\"').replace('\n', '').replace("_x000B_", "")
    

def get_etappen_count(self):
    etappen_count = set()
    for q in self.all_questions_array:
        etappen_count.add(q.excel_id[0])
    return len(etappen_count)

def calc_etappen_end_screens(self):
    # which screens are the last screen in an etappe
    etappen_end_screens = {}
    for etappe in range(1, self.etappen_count+1):
        biggest = 0
        for question in self.all_questions_array:
            if int(question.excel_id[0]) == etappe:
                # letzter screen is alsways end screen
                if 'letzter Screen' in question.structure:
                    etappen_end_screens[question.excel_id[0]] = question.excel_id
                    break
                # highest number and no letzter screen 
                elif int(question.excel_id[2]) > biggest:
                    biggest = int(question.excel_id[2])
                    etappen_end_screens[question.excel_id[0]] = question.excel_id
    return etappen_end_screens

def create_beginning(id, version, journey_key, information):
    beginning = '''
{
  "id": "%s",
  "key": "%s",
  "order": 10,
  "mainImageName": "%s",
  "mainImageLongName": "%s",
  "topicIconImageName": "%s",
  "mainImageLockedLongName": "%s",
  "backgroundImageName": "%s",
  "sessionImageName": "%s",
  "cardDisplayImageName": %s,
  "published": true,
  "publishedEN": false,
  "feedbackLink": null,
  "version": %s,
  "type": "%s",
  "compulsoryOrder": false,
  "topicId": %s,
  "backgroundImageLockedName": "dark_main.png",
  "translations": [
    {
      "id": "%s-DE",
      "language": "DE",
      "title": "%s",
      "subTitle": "",
      "description": null
    },
    {
      "id": "%s-EN",
      "language": "EN",
      "title": "Englisch",
      "subTitle": "",
      "description": null
    }
  ],
  "content": [
    {
      "id": "%s-cont",
      "order": 2,
      "type": "PARAGRAPH",
      "imageName": null,
      "translations": [
        {
          "id": "%s-cont-DE",
          "language": "DE",
          "title": null,
          "text": "%s"
        },
        {
          "id": "%s-cont-EN",
          "language": "EN",
          "title": null,
          "text": "Englisch"
        }
      ]
    },
    {
      "id": "%s-s1",
      "order": 4,
      "type": "SESSION_TITLE",
      "imageName": null,
      "translations": [
        {
          "id": "%s-s1-DE",
          "language": "DE",
          "title": null,
          "text": "%s"
        },
        {
          "id": "%s-s1-EN",
          "language": "EN",
          "title": null,
          "text": "Englisch"
        }
      ]
    }
  ],
  "sessions": [
    {
      "id": "%s-1",
      "order": 1,
      "durationMin": %s,
      "durationMax": %s,
      "translations": [
        {
          "id": "%s-1-DE",
          "language": "DE",
          "title": "%s"
        },
        {
          "id": "%s-1-EN",
          "language": "EN",
          "title": "Englisch"
        }
      ],
      "questions": [
        ''' % (id+version, journey_key, information[9], information[10], information[11], information[12], information[13], information[14], information[15], version[1:], information[0], information[1], id+version, information[2], id+version, id+version, id+version, information[3].replace('"', '\\"').replace('\n', '').replace("_x000B_", "")+'<br><br>', id+version, id+version, id+version, information[4], id+version, id+version, information[7], information[8], id+version, information[5], id+version)
    return beginning
    
def create_json(self):
        json = ''
        # BEGINNING
        if self.write_beginning:    
            json += create_beginning(self.id_base, self.version, self.journey_key, self.information)

        count = 0
        for i, question in enumerate(self.all_questions_array): 
            '''
            # set back count for Neue Etappe
            if question.type ==  'Neue Etappe':
                count = -1
                etappe += 1
            '''

            # WRITE & NEXT_QUESTION_ID & REMOVE COMMA
            # Option A - weiter mit screen
            if 'weiter mit Screen' in question.structure:
                if i == (len(self.all_questions_array)-1) or (i < (len(self.all_questions_array)-1) and self.all_questions_array[i+1].type == 'Neue Etappe'):
                    json += question.create_json()[:-1]
                else:
                    json += question.create_json()

            # Option B - letzter Screen
            elif 'letzter Screen' in question.structure:
                if i == (len(self.all_questions_array)-1) or (i < (len(self.all_questions_array)-1) and self.all_questions_array[i+1].type == 'Neue Etappe'):
                    json += question.create_json()[:-1]
                else:
                    json += question.create_json()

            # Option C - keins von beiden
            else: 
                # last question in array or next question is neue etappe
                if i == (len(self.all_questions_array)-1) or (i < (len(self.all_questions_array)-1) and self.all_questions_array[i+1].type == 'Neue Etappe'):
                    question.id_next_question = 'null'
                    json += question.create_json()[:-1]
                else:
                    json += question.create_json()
            
            # increase count
            count += 1

        # ENDING
        if self.write_ending:   
           json += '''
      ],
      "questionLoops": []
    }
  ]
}
        '''
        return json

class Trip:
    def __init__(self, df, id_base, version, write_beginning, write_ending, journey_key, information):
        self.df = df
        self.id_base = id_base
        self.version = version
        self.journey_key = journey_key
        self.information = information
        self.write_beginning = write_beginning
        self.write_ending = write_ending
        self.all_questions_array = create_questions_array(self)
        do_tests(self.df, self.information, self.all_questions_array)
        format_text(self)
        # create progress
        self.etappen_count = get_etappen_count(self)
        self.etappen_end_screens = calc_etappen_end_screens(self)
        create_progress(self, self.all_questions_array)

        self.json = create_json(self)

    
        

    