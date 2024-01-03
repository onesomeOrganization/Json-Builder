# Json-Builder

# How to:

1. clone repo
2. import libraries if needed (There is no requirements file, however, you should not need much more than pandas and numpy)
3. create a folder where you want to save the created jsons
4. copy path to save_directory in Json_Builder.py
5. Add all other demanded information in the json_builder.py top
6. Excel should look like the most recent template here: https://onesome.sharepoint.com/sites/produktentwicklung/Shared%20Documents/Forms/AllItems.aspx?id=%2Fsites%2Fproduktentwicklung%2FShared%20Documents%2FTech%20%26%20Data%2FJson%2F06%5FJson%20Builder&viewid=58b5c59a%2Db0cb%2D4cbe%2Dbafe%2Ddc3ae00b1f6c 
7. run file and find json in the save_directory with the name of the name_of_json_file variable
   -> If you want to have the latest changes use the dev branch. If you want to have a version which might be older but working for sure, use the main branch.

# Explanations / Debugging tipps

A trip (can be world/journey or short-trip) contains an array of Question objects.
Each question object consists of the following components:

- content (e.g. paragraph, reference, image etc.)
- answer options (e.g. radio buttons, checkbox, textfields)
- next logic options
- ref logic options

Each object has a create json method. Usually create_json is evoked during initialisation except for the question object -> see trip.py
