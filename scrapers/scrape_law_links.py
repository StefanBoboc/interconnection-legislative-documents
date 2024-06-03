import datetime
import logging
import re
import sys
import time
import random
from math import ceil

import requests
from bs4 import BeautifulSoup

# https://legislatie.just.ro/Public/RezultateCautare?rezultatePerPagina=5&titlu=*&publicatinceputtext=2020/10/12&publicatsfarsittext=2020/10/12

PAGE_TEMPLATE = "https://legislatie.just.ro/Public/RezultateCautare?page={}&rezultatePerPagina=5&titlu=*&publicatinceputtext={}&publicatsfarsittext={}"
JOB_DIR = r"C:\Users\xxxxx\Desktop\interconnection_legislative_documents\prod\links"
OUTPUT_PATH = JOB_DIR + r"\{}\{}\{}_{}laws.txt"
MILE_STONE_DELTA = 500
MAX_LAWS_PER_DAY = -1
MAX_LAWS_DATE = ""

# Create new logging file
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logging_filename = JOB_DIR + f"\scrape_links_{timestamp}.log"
logging.basicConfig(filename=logging_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')


def empty_page_log(empty_pages_nbr):
    if empty_pages_nbr % 10 == 0 and empty_pages_nbr != 0:
        logging.warning(f"Empty pages count: {empty_pages_nbr}")


def get_doc_count(html_page, date):
    try:
        global MAX_LAWS_PER_DAY, MAX_LAWS_DATE

        div_id = html_page.find("div", {"id": "textarticol"})
        div_class = div_id.find("div", {"class": "panel-footer"})
        div_class_text = div_class.text.strip()

        match = re.search(r'(\d+) document\(e\)', div_class_text)

        if match and html_page != "":
            total_laws = int(match.group(1))

            if total_laws > MAX_LAWS_PER_DAY:
                MAX_LAWS_PER_DAY = total_laws
                MAX_LAWS_DATE = date

            return total_laws

        else:
            logging.warning("Total number of laws for current date not found")
            print("Total number of laws for current date not found")
            return -1

    except Exception as e:
        logging.warning("Total number of laws for current date not found")
        logging.warning(str(e))
        return -1


if __name__ == '__main__':
    start_date = datetime.date(2015, 1, 1)
    end_date = datetime.date(2018, 12, 31)
    delta = datetime.timedelta(days=1)

    logging.info(f"START_DATE = {start_date} -> END_DATE = {end_date}")

    # Counters
    empty_pages = 0
    total_collected_laws = 0
    milestone = 500

    # Obtain links from every page from start_date until end_date
    current_date = start_date
    while current_date <= end_date:
        empty_page_log(empty_pages)

        logging.info(f"=========================")
        logging.info(f"Get links for {current_date}")

        # Hyperlink of the page using the current date
        formatted_date = current_date.strftime("%Y/%m/%d")
        print(formatted_date)
        link = PAGE_TEMPLATE.format(1, formatted_date, formatted_date)

        # Access and get the html code of the page
        try:
            response = requests.get(link)
            response.raise_for_status()
            doc_soup = BeautifulSoup(response.content, "html.parser")

        except requests.exceptions.RequestException as e:
            logging.error(f"The current page could not be opened: {link}")
            print(e)
            empty_pages += 1
            current_date += delta
            doc_soup = ""

        except Exception as e:
            logging.error(str(e))
            sys.exit(1)

        # Find total laws for the current_date and the number of pages
        curr_date_law_nbr = get_doc_count(doc_soup, current_date)
        pages = ceil(curr_date_law_nbr / 50)

        # Create the file where the hyperlinks of the current_day's laws will be written
        empty_page_tag = ''

        if curr_date_law_nbr == -1:
            logging.error(f"Bad page: {link}")
            empty_page_tag = "b"

        elif pages == 0:
            logging.warning(f"Empty page: {link}")
            empty_page_tag = "e"
            pages = -1

        path_year = current_date.year
        path_month = str(current_date.month).zfill(2)
        file_name = current_date.strftime('%Y%m%d')

        f_links = open(OUTPUT_PATH.format(path_year, path_month, file_name, empty_page_tag), 'a')

        for page_nbr in range(1, pages + 1):
            if page_nbr != 1:
                link = PAGE_TEMPLATE.format(page_nbr, formatted_date, formatted_date)

                # Access and get the html code of the page
                try:
                    response = requests.get(link)
                    response.raise_for_status()
                    doc_soup = BeautifulSoup(response.content, "html.parser")

                except requests.exceptions.RequestException as e:
                    logging.error(f"The current page could not be opened: {link} \n Page number: {page_nbr}")
                    print(e)
                    empty_pages += 1
                    current_date += delta
                    continue

                except Exception as e:
                    logging.error(str(e))
                    sys.exit(1)

            # Extract all law hyperlinks from the page
            a_tags = doc_soup.find_all("a", string="Vizualizeaza")

            # Write law hyperlinks
            for a_tag in a_tags:
                href = a_tag.get('href')
                f_links.write(href + '\n')

        f_links.close()

        logging.info(f"Got {curr_date_law_nbr} links from current page")

        # For every approx. 500 hyperlinks obtained, a sleep between 30 and 60 seconds is offered
        if curr_date_law_nbr != -1:
            total_collected_laws += curr_date_law_nbr
        if total_collected_laws > milestone or current_date == end_date:
            logging.info(f"TOTAL LINKS GOT: {total_collected_laws}")
            milestone += MILE_STONE_DELTA

            if current_date != end_date:
                sleep_time = random.randint(30, 60)
                time.sleep(sleep_time)

        current_date += delta

    logging.info(f"MAX LAWS PER DAY: {MAX_LAWS_PER_DAY}")
    print(f"MAX LAWS PER DAY: {MAX_LAWS_PER_DAY}")
    logging.info(f"MAX LAWS DATE: {MAX_LAWS_DATE}")
    print(f"MAX LAWS DATE: {MAX_LAWS_DATE}")
