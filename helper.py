import re

content_length_dict = {'REFERENCE': 1, 'PARAGRAPH': 1, 'AUDIO': 2, 'IMAGE': 2, 'SMALL_IMAGE': 2, 'MORE_INFORMATION_EXPANDED': 1, 'MORE_INFORMATION': 1, 'SUB_TITLE': 1, 'REFERENCE': 1}
need_answer_option = ('BUTTON', 'ITEM(Single)', 'ITEM(Multiple)', 'ANSWER OPTION', 'SEVERAL ANSWER OPTIONS')

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

# check if a reference is like 1.3
def normal_screen_reference(text):
  pattern = '^[+-]?\d+([.,]\d+)?$'
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

def extract_values_from_wenn_condition(text):
      pattern = r'(\d+\.\d+)\s*\(wenn\s+(\d+\.\d+)\s*=\s*([^\d+\.\d+]*)\)'
      matches = re.findall(pattern, text)

      result_dict = {}
      for item in matches:
          main_key, sub_key, values = item
          values_list = [value.strip() for value in values.split('oder')]
          if main_key not in result_dict:
              result_dict[main_key] = [sub_key, values_list]
      return result_dict


def create_scala_condition_dict(text):
    pattern = r'(\d+\.\d+)\s*\((.*?)\)'
    matches = re.findall(pattern, text)
    condition_dict = {}
    
    for match in matches:
        key = match[0]
        condition = match[1]
        if '>=' in condition:
            operator = '>='
        elif '<=' in condition:
            operator = '<='
        elif '>' in condition:
            operator = '>'
        elif '<' in condition:
            operator = '<'
        elif '=' in condition:
            operator = '='
        values = condition.split(operator)[1].split(',')
        for i, value in enumerate(values):
          values[i] = int(value.strip())
            
        condition_dict[key] = [operator, values]
    return condition_dict

def create_excel_id(id_string):
   splits = id_string.split('-')
   excel_id = splits[-2]+'.'+splits[-1][:-1]
   return excel_id
