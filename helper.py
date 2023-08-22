import re

content_length_dict = {'REFERENCE': 1, 'PARAGRAPH': 1, 'AUDIO': 2, 'IMAGE': 2, 'SMALL_IMAGE': 2, 'MORE_INFORMATION_EXPANDED': 1, 'MORE_INFORMATION': 1, 'SUB_TITLE': 1, 'REFERENCE': 1, 'PDF_DOWNLOAD': 2}
need_answer_option = ('BUTTON', 'ITEM(Single)', 'ITEM(Multiple)', 'ANSWER OPTION', 'SEVERAL ANSWER OPTIONS', 'SCALA')

nextLogic_patterns = {
   'VALUE': r'(\d+\.\d+)\s*\(\s*wenn\s*(\w+)\s*([><=]=?)\s*(\d+)\)',
   'REF_VALUE': r'(\d+\.\d+(?:x)?)\s*\(\s*wenn\s*(\d+\.\d+(?:x)?|scala|Scala)\s*([><=]=?)\s*(\d+(\.\d+)?(?:x)?|(\d+,)+\d+)\)',
   'REF_COUNT': r'(\d+\.\d+)\s*\(\s*wenn\s*(\d+\.\d+)\s*([=><]=?|!=)\s*(\d+)\s*(Antwort(en)?|antwort(en)?)\)',
   'REF_OPTION': r'(\d+\.\d+)\s*\(\s*wenn\s*(\d+\.\d+)\s*=\s*(.*?)\)'
}


def create_id (object, reference_id_excel):
    reference_id_excel = reference_id_excel.strip()
    id_numbers = reference_id_excel.split('.')
    new_id = object.id_base + 'v'+ object.version + '-'+ id_numbers[0]+'-'+ id_numbers[1]
    return new_id

def get_one_id_higher(id):
  splits = id.split('-')
  if 'x' in id:
     one_higher = '-'.join(splits[:-1] + [str(int(splits[-1][:-1]) + 1)])
  else:
    one_higher = '-'.join(splits[:-1] + [str(int(splits[-1]) + 1)])
  return one_higher

def get_one_excel_id_higher(excel_id):
  splits = excel_id.split('.')
  if 'x' in excel_id:
     one_higher = splits[0] + '.' + str(int(splits[-1][:-1]) + 1)
  else:
    one_higher = splits[0] + '.' + str(int(splits[-1]) + 1)
  return one_higher

# check if a reference is like 1.3
def normal_screen_reference(text):
  pattern = r"^\d+\.\d+(?:x)?$"
  it_is_screen_ref = bool(re.match(pattern, text))
  return it_is_screen_ref

def get_content_length(structure):
    length = 0
    answer_option_length_is_considered = False
    for entry in structure:
      if entry in content_length_dict:
        length+=content_length_dict[entry]
      if entry in need_answer_option and not answer_option_length_is_considered:
         length+=1
         answer_option_length_is_considered = True
    return length

def increase_order_id(order, id, about = 1):
  order += about
  id = '-'.join(id.split('-')[:-1] + [str(order)])
  return order, id

def add_quotation_mark(text):
  text = '"'+text+'"'
  return text

def find_nodes_before(graph, node):
    befores = []
    for n, neighbors in graph.items():
        if node in neighbors:
            befores.append(n)
    return befores

def delete_last_number_from_id(id):
  splits = id.split('-')
  new_id = ('-').join(splits[:-1])
  return new_id

def create_condition_dict(text, type):
  if type == 'REF_OPTION':
      matches = re.findall(nextLogic_patterns['REF_OPTION'], text)
      result_dict = {}
      for item in matches:
          main_key, sub_key, values = item
          values_list = [value.strip() for value in values.split('oder')]
          if main_key not in result_dict:
              result_dict[main_key] = [sub_key, values_list]
      return result_dict
  if type == 'VALUE':
      matches = re.findall(nextLogic_patterns['VALUE'], text)
      condition_dict = {}
      for item in matches:
        id, _ , operator, value = item
        values = value.split(',')
        for i, value in enumerate(values):
            values[i] = int(value.strip())
        condition_dict[id] = [operator, values]
      return condition_dict
  if type == 'REF_COUNT':
    matches = re.findall(nextLogic_patterns['REF_COUNT'], text, re.IGNORECASE)
    condition_dict = {}
    for match in matches:
        main_key, sub_key, operator, value, _, _, _ = match
        condition_dict[main_key] = [sub_key, operator, int(value)]
    return condition_dict
  if type == 'REF_VALUE':
    matches = re.findall(nextLogic_patterns['REF_VALUE'], text)
    result_dict = {}
    for item in matches:
        key, variable, operator, value, indicator, _ = item
        if indicator == '':
          comparison = False
        else:
          comparison = True
        values = value.split(',')
        if not normal_screen_reference(values[0]):
          for i, value in enumerate(values):
              values[i] = int(value.strip())
        result_dict[key] = [variable, operator, values, comparison]
    return result_dict
         

def create_excel_id(id_string):
   splits = id_string.split('-')
   excel_id = splits[-2]+'.'+splits[-1][:-1]
   return excel_id

def get_number_and_type_for_value_option(scala_min, scala_max, sign, values):
  type = ''
  number = 0
  secondNumber = 'null'
  if sign == '=' and values[0] == scala_min:
    number = max(values)+1
    type = 'VALUE_LT'
  elif sign == '=' and values[-1] == scala_max:
    number = min(values)
    type = 'VALUE_GTE'
  elif sign == '=':
    number = min(values)-1 
    secondNumber = max(values)+1
    type = 'VALUE_BETWEEN'
  elif sign == '>':
    number = values[0]+1 
    type = 'VALUE_GTE'
  elif sign == '<':
    number = values[0]
    type = 'VALUE_LT'
  elif sign == '<=':
    number = values[0]+1
    type = 'VALUE_LT'
  elif sign == '>=':
    number = values[0] 
    type = 'VALUE_GTE'
  return type, number, secondNumber
   
