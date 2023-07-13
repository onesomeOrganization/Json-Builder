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