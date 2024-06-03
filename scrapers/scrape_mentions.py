import datetime
import json
import logging
import os
import random
import sys
import time
from math import ceil

import requests
from bs4 import BeautifulSoup
import re

JOB_DIR = r"C:\Users\xxxxx\Desktop\interconnection_legislative_documents\prod\mentions"
OUTPUT_PATH = JOB_DIR + r"\{}\{}\{}_mentions.json"
MILE_STONE_DELTA = 2000

# Create new logging file
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logging_filename = JOB_DIR + f"\scrape_mentions_{timestamp}.log"
logging.basicConfig(filename=logging_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')


def find_positions(big_text, strings_list):
    positions = []

    for string in strings_list:
        pattern = re.escape(string)
        matches = re.finditer(pattern, big_text)

        for match in matches:
            start_position, end_position = match.span()
            positions.append((start_position, end_position - 1))

    return positions


def get_doc_title(_html_content):
    return _html_content.find('span', class_='S_DEN').get_text()


def get_content(_html_content):
    return " ".join(_html_content.stripped_strings)


def get_mentions_list(_html_content, contents):
    index = 0
    mentions = []
    not_found = 0

    # Walk through every hyperlink inside the html document
    hyperlink_elements = _html_content.find_all("a", href=True)
    for hyperlink in hyperlink_elements:
        mention = hyperlink.get_text()
        href = hyperlink.get("href")

        start_index = contents.find(mention, index)
        if start_index == -1:
            logging.warning(f"Mention index not found: {mention}")
            not_found += 1
            continue
        end_index = start_index + len(mention)

        dict = {"mention": mention, "start_index": start_index, "end_index": end_index, "href": href,
                "href_title": None}
        mentions.append(dict)

        index = end_index

    if not_found > 0:
        logging.info(f"Mentions not found for the current document: {not_found}")

    return mentions


if __name__ == '__main__':
    years_range = [2019, 2018, 2017]
    # year = 2023
    TOTAL_MENTIONS = 0
    milestone = 2000

    for year in years_range:
        folder_path = rf"C:\Users\xxxxx\Desktop\interconnection_legislative_documents\prod\links\{year}"
        # Walk through every month of the year
        for month in range(1, 13):
            month_folder = os.path.join(folder_path, str(month).zfill(2))
            files = os.listdir(month_folder)

            file_count = 0

            # Walk through every file for the current month
            for src_file_name in files:
                if "elaws" not in src_file_name and "blaws" not in src_file_name:
                    print(src_file_name)
                    date_count = 0
                    logging.info(f"Process mentions for file: {src_file_name}")

                    mentions_curr_date_jsons = {}
                    date = src_file_name[:8]
                    nbr_link_visited = 0

                    # Walk through every link from the file
                    src_file = open(os.path.join(month_folder, src_file_name))
                    links = src_file.readlines()
                    for link in links:
                        stripped_link = link.strip()
                        logging.info(f"Search for mentions in link: {stripped_link}")
                        try:
                            url = f"https://legislatie.just.ro{stripped_link}"
                            response = requests.get(url)
                            response.raise_for_status()
                            doc_soup = BeautifulSoup(response.content, "html.parser")

                        except requests.exceptions.RequestException as e:
                            logging.error(f"The current page could not be opened: {stripped_link}")
                            print(e)
                            continue

                        except Exception as e:
                            logging.error(str(e))
                            sys.exit(1)

                        try:
                            target_div = doc_soup.find('div', id='div_Formaconsolidata')
                        except AttributeError as e:
                            logging.error(f"'div_Formaconsolidata' was not found")
                            continue
                        except Exception as e:
                            logging.error(str(e))
                            sys.exit(1)

                        nbr_link_visited += 1

                        # Create an ID for the document
                        doc_id = f"{date}{str(nbr_link_visited).zfill(3)}"

                        # Get the title of the document
                        try:
                            title = get_doc_title(target_div)
                        except AttributeError as e:
                            logging.error(f"Title was not found")
                            continue
                        except Exception as e:
                            logging.error(str(e))
                            sys.exit(1)

                        # Get the content/text of the document
                        try:
                            contents = get_content(target_div)
                        except AttributeError as e:
                            logging.error(f"Content was not found")
                            continue
                        except Exception as e:
                            logging.error(str(e))
                            sys.exit(1)

                        # Get the mentions from the content
                        try:
                            mentions = get_mentions_list(target_div, contents)
                        except AttributeError as e:
                            logging.error(f"Mentions were not found")
                            continue
                        except Exception as e:
                            logging.error(str(e))
                            sys.exit(1)

                        mentions_count = len(mentions)
                        date_count += mentions_count
                        TOTAL_MENTIONS += mentions_count

                        # Every document/law has its own json with its attributes
                        curr_law_json = {
                            "doc_title": title,
                            "url": url,
                            "text": contents,
                            "mentions": mentions
                        }

                        # Add the json for the current document/law with its ID to the json for the date in progress
                        mentions_curr_date_jsons[doc_id] = curr_law_json

                        # print(f"Titlu: \n{title}")
                        # print(f"Url : \n{url}")
                        # print(f"Content: \n{contents}")
                        # print(f"Mentiuni: \n{mentions}")
                        # print(f"HTML: \n{target_div}")
                        # print(json)
                        # print("===============")

                    logging.info(f"Mentions found in date '{date}': {date_count}")

                    # Serializing json
                    json_object = json.dumps(mentions_curr_date_jsons, indent=4)

                    # Path where the json with the mentions for all laws for current date are stored
                    dst_file = OUTPUT_PATH.format(src_file_name[:4], src_file_name[4:6], date)
                    with open(dst_file, "w+") as outfile:
                        outfile.write(json_object)

                    logging.info("==================================================")

                    # For every 2 days of laws processed, a sleep between 30 and 60 seconds is offered
                    file_count += 1
                    if file_count >= 2:
                        sleep_time = random.randint(30, 60)
                        print(f"Mentions got until now: {TOTAL_MENTIONS}")
                        print(f"Sleep {sleep_time} seconds...")
                        file_count = 0
                        time.sleep(sleep_time)

        logging.info(f"TOTAL_MENTIONS on {month}: {TOTAL_MENTIONS}")

