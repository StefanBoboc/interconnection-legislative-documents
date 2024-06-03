import datetime
import json
import logging
import sys

import requests
from bs4 import BeautifulSoup
import os


JOB_DIR = r"C:\Users\xxxxx\Desktop\interconnection_legislative_documents\prod\complete_mentions"
OUTPUT_PATH = JOB_DIR + r"\{}\{}\{}_complete_mentions.json"

# Create new logging file
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logging_filename = JOB_DIR + f"\scrape_complete_mentions_{timestamp}.log"
logging.basicConfig(filename=logging_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')


def get_doc_title(_html_content):
    return _html_content.find('span', class_='S_DEN').get_text()


if __name__ == '__main__':
    # years_range = [2023, 2022, 2021]
    years_range = [2023]
    TOTAL_MENTIONS = 0
    milestone = 2000

    for year in years_range:
        folder_path = rf"C:\Users\xxxxx\Desktop\interconnection_legislative_documents\prod\mentions\{year}"
        # Walk through every month of the year
        for month in range(1, 13):
            month_folder = os.path.join(folder_path, str(month).zfill(2))
            files = os.listdir(month_folder)

            file_count = 0

            # Walk through every file for the current month
            for src_file_name in files:
                logging.info(f"src_file_name: {src_file_name}")
                print(src_file_name)
                date = src_file_name[:8]

                # Load JSON
                src_file = open(os.path.join(month_folder, src_file_name), 'r')
                law_documents = json.load(src_file)
                for law_document_key in law_documents:
                    logging.info(f"law_document_key: {law_document_key}")
                    print(law_document_key)
                    law_document = law_documents[law_document_key]
                    law_mentions = law_document['mentions']

                    for law_mention in law_mentions:
                        mention_href = law_mention['href'].strip()
                        hyperlink = f"https://legislatie.just.ro/{mention_href.split('../')[-1]}"

                        try:
                            response = requests.get(hyperlink)
                            response.raise_for_status()
                            doc_soup = BeautifulSoup(response.content, "html.parser")
                        except requests.exceptions.RequestException as e:
                            logging.error(f"The current page could not be opened: {hyperlink}")
                            print(f"The current page could not be opened: {hyperlink}")
                            print(e)
                            continue

                        except Exception as e:
                            logging.error(str(e))
                            print(str(e))
                            sys.exit(1)

                        try:
                            target_div = doc_soup.find('div', id='div_Formaconsolidata')
                        except AttributeError as e:
                            logging.error(f"'div_Formaconsolidata' was not found")
                            print(f"'div_Formaconsolidata' was not found")
                            continue
                        except Exception as e:
                            logging.error(str(e))
                            print(str(e))
                            sys.exit(1)

                        # Get the title of the document
                        try:
                            title = get_doc_title(target_div)
                        except AttributeError as e:
                            logging.error(f"Title was not found")
                            print(f"Title was not found")
                            continue
                        except Exception as e:
                            logging.error(str(e))
                            print(str(e))
                            sys.exit(1)

                        # Assign a complete hyperlink to the mention href
                        law_mention['href'] = hyperlink

                        # Assign the mention href title
                        if law_mention['href_title'] is None:
                            law_mention['href_title'] = title.strip()

                # Serializing json
                json_object = json.dumps(law_documents, indent=4)

                # Path where the json with the mentions for all laws for current date are stored
                dst_file = OUTPUT_PATH.format(date[:4], date[4:6], date)
                with open(dst_file, "w+") as outfile:
                    outfile.write(json_object)
