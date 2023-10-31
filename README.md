# Json-Builder

# How to:

1. clone repo
2. import libraries if needed (There is no requirements file, however, you should not need much more than pandas and numpy)
3. create a folder where you want to save the created jsons
4. copy path to save_directory in Json_Builder.py
5. Add all other demanded information in the json_builder.py top
6. Excel should look like the Json_Excel_template3.3 (Stand 3.7.23: Better ask for the current template version as it is changing all the time)
7. run file and find json in the save_directory with the name of the name_of_json_file variable
   -> If you want to have the latest changes use the dev branch. If you want to have a version which might be older but working for sure, use the main branch.

# Explanations / Debugging tipps

A trip (can be world/journey or short-trip) contains an array of Question objects.
Each question object consists of the following components:

- content (e.g. paragraph, reference, image etc.)
- answer options (e.g. radio buttons, checkbox, textfields)
- next logic options
- ref logic options

Each object has create json method. Usually create_json is evoked during initialisation except for the question object -> see trip.py
