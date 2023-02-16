# Json-Builder

# How to:

1. Add all information in the json_builder.py top
2. run file

# Explanations:

A question contains:

- question block
- content block
- answer options
- next logic options

Question block:
Outline for the question -> the type of the question.
Examples: ONTENT, OPTION_QUESTION, OPEN_QUESTION, SCALA_SLIDER,

Content block:
Content of the question.
Examples: P = Paragraph, R = Referenz, I = Image, A = Audio, M = More Information Expandable -> Titel ist immer dabei

Answer options:
Possible Answer Options, where the user can type in their answers.
Examples: R = Radio Button, C = Checkbox, T = Text_Field_Expandable

Next logic options:
Links the screen to the next screen with some logic.
Examples: NEXT_LOGIC_TYPE: NEXT, NEXT_OPTION
NEXT_LOGICS: N = option with next
