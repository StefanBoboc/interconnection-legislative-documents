import os
import sys

year = "2017"
folder_path = rf"C:\Users\xxxxx\Desktop\interconnection_legislative_documents\prod\complete_mentions\{year}"

# Check if the folder doesn't exist already
if not os.path.exists(folder_path):
    # Create the folder
    os.makedirs(folder_path)
    print(f"Folder '{folder_path}' created successfully.")
else:
    print(f"Folder '{folder_path}' already exists.")
    sys.exit(1)

for month in range(1, 13):
    month_folder = os.path.join(folder_path, str(month).zfill(2))
    os.makedirs(month_folder)
