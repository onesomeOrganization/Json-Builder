class Question:
    def __init__(self, type, content='P', answer_option = None, next_logic_type='NEXT', next_logic_options=None):
        self.type = type
        self.content = content
        self.answer_option = answer_option
        self.next_logic_type = next_logic_type
        self.next_logic_options = next_logic_options