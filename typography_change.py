import pandas as pd
import openpyxl

excel_path_or_name = "Jsons/Tests/Test.xlsx"
df = pd.read_excel(excel_path_or_name)

wb = openpyxl.load_workbook('Jsons/Tests/Test.xlsx')

# ---------- FUNCTIONS ------------
# Define a function to check if a cell's text is bold
def is_bold(cell):
    return cell.font_weight == 'bold'

def modify_text(cell):
    text = cell.value
    # Split the text into words
    words = text.split()
    # Loop through each word and check if it is bold
    for word in words:
        new_words = []
        if word.font.bold:
            new_words.append('<strong>' + word + '</strong>')
        else:
            new_words.append(word)
    cell.value = ' '.join(new_words)


# Get the first sheet of the workbook
sheet = wb.active
# go throughh all cells
for row in sheet.iter_rows():
    # Loop through each cell in the row
    for cell in row:
        modify_text(cell)

# Save the changes to the workbook
wb.save('modified.xlsx')

print('Done')
