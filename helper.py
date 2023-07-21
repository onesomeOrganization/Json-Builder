import re

def create_id (object, reference_id_excel):
    reference_id_excel = reference_id_excel.strip()
    id_numbers = reference_id_excel.split('.')
    new_id = object.id_base + 'v'+ object.version + '-'+ id_numbers[0]+'-'+ id_numbers[1]
    return new_id

def get_one_id_higher(id):
  splits = id.split('-')
  one_higher = '-'.join(splits[:-1] + [str(int(splits[-1]) + 1)])
  return one_higher

# check if a reference is like 1.3
def normal_screen_reference(text):
  pattern = '^[+-]?\d+([.,]\d+)?$'
  it_is_screen_ref = bool(re.match(pattern, text))
  return it_is_screen_ref

def get_content_length(structure):
    length = 0
    for entry in structure:
      if entry == 'REFERENCE':
        length+=1
      elif entry == 'PARAGRAPH':
        length+=1
      elif entry == 'AUDIO':
        length+=2
      elif entry == 'IMAGE':
        length+=2
      elif entry == 'MORE_INFORMATION_EXPANDED':
        length+=1
      elif entry == 'MORE_INFORMATION':
        length+=1
      elif entry == 'SMALL_IMAGE':
        length += 2
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
      pattern = r'(\d+\.\d+)\s*\(wenn\s+(\d+\.\d+):\s+(.*?)\)'
      matches = re.findall(pattern, text)

      result_dict = {}
      for item in matches:
          main_key, sub_key, values = item
          values_list = [value.strip() for value in values.split('oder')]
          if main_key not in result_dict:
              result_dict[main_key] = [sub_key, values_list]
      return result_dict