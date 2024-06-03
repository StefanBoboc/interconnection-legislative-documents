import json
import logging
import os
import sys
from datetime import datetime

import mysql.connector as mysql
import requests
from bs4 import BeautifulSoup

env = "prod"
years = ['2017']
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']

mydb = mysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="xxxxx",
    database="dataset"
)


DOCUMENT_ID = 0
JOB_DIR = r"C:\Users\xxxxx\Desktop\interconnection_legislative_documents\{}\database"
FILES_PATH = r"C:\Users\xxxxx\Desktop\interconnection_legislative_documents\{}\mentions\{}\{}"
CONTENT_PATH = r"C:\Users\xxxxx\Desktop\interconnection_legislative_documents\{}\database\document_content\{}\{}\{}\{}"
SQL_INSERT_DOC = "INSERT INTO prd_document (doc_id, doc_title, doc_url, doc_content, doc_date) VALUES (%s, %s, %s, %s, %s)"
SQL_INSERT_MEN = "INSERT INTO prd_mention (men_text, men_start, men_end, men_href, men_href_title, doc_id) VALUES (%s, %s, %s, %s, %s, %s)"
SQL_GET_MAX_DOC_ID = "SELECT max(doc_id) FROM prd_document"
SQL_GET_MEN_HREF_TITLE = "SELECT men_href_title FROM prd_mention WHERE men_href = %s"
# SQL_GET_DOC_ID = "SELECT doc_id FROM prd_document WHERE doc_url = %s"


# Create new logging file
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
logging_filename = JOB_DIR.format(env) + f"\create_database_{timestamp}.log"
logging.basicConfig(filename=logging_filename,
                    level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')


def run_mysql_insert(sql_statement, sql_values):
    cursor = mydb.cursor()
    cursor.execute(sql_statement, sql_values)
    mydb.commit()
    cursor.close()


def run_mysql_select(sql_statement, sql_values=None):
    cursor = mydb.cursor()
    if sql_values is None:
        cursor.execute(sql_statement)
    else:
        cursor.execute(sql_statement, sql_values)
    result = cursor.fetchall()
    cursor.close()
    return result


def get_doc_title(_html_content):
    return _html_content.find('span', class_='S_DEN').get_text()


def set_document_id():
    global DOCUMENT_ID
    result = run_mysql_select(SQL_GET_MAX_DOC_ID)
    if result[0][0] is None:
        DOCUMENT_ID = 0
    else:
        DOCUMENT_ID = result[0][0]

    print_log(DOCUMENT_ID, 0)


def make_content_file(file_path, content):
    # Get the directory path from the file path
    directory = os.path.dirname(file_path)
    print_log(f"AAAAA {directory}", 0)

    # Check if the directory exists, if not, create it
    if not os.path.exists(directory):
        os.makedirs(directory)

    # Now create the file
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(content)


def print_log(msg, err_code):
    if err_code == 0:
        print(msg)
        logging.info(msg)
    elif err_code == 1:
        print(f"ERROR - {msg}")
        logging.error(msg)


if __name__ == '__main__':
    set_document_id()
    temp_men_href_title = {}

    for year in years:
        for month in months:
            month_folder = FILES_PATH.format(env, year, month)
            file_names = os.listdir(month_folder)

            for file_name in file_names:
                print_log(f"File '{file_name}'", 0)

                # Load JSON
                file_content = open(os.path.join(month_folder, file_name), 'r', encoding='utf-8')
                documents = json.load(file_content)

                # Walk through every law document from the .json
                for document_key in documents:
                    print_log(f"Document '{document_key}'", 0)



                    # if document_key > '20190103005':
                    #     print(f"STOOOP")
                    #     exit(0)

                    print("Process it")
                    # continue
                    # exit(0)

                    document = documents[document_key]

                    #
                    # Insert Document in MySQL
                    #
                    DOCUMENT_ID += 1
                    doc_title = document['doc_title']
                    doc_url = document['url']
                    doc_content = CONTENT_PATH.format(env, document_key[0:4], document_key[4:6], document_key[6:8], f"{document_key}_content.txt")
                    make_content_file(doc_content, document['text'])
                    doc_date = document_key

                    val_insert_doc = (DOCUMENT_ID, doc_title, doc_url, doc_content, doc_date)
                    print_log(f"INSERT DOCUMENT: {val_insert_doc}", 0)
                    run_mysql_insert(SQL_INSERT_DOC, val_insert_doc)

                    #
                    # Insert Mentions for the current Document in MySQL
                    #
                    temp_men_href_title.clear()

                    mentions = document['mentions']
                    for mention in mentions:
                        men_text = mention['mention']
                        men_start = mention['start_index']
                        men_end = mention['end_index']
                        men_href = f"https://legislatie.just.ro/{mention['href'].split('../')[-1]}"
                        men_href_title = None
                        men_doc_id = DOCUMENT_ID

                        # SEARCH IN TEMP MEM.
                        print_log("Search in TEMP", 0)
                        if men_href in temp_men_href_title:
                            print_log("Href_title FOUND in TEMP", 0)
                            men_href_title = temp_men_href_title[men_href]

                        else:
                            print_log(f"Href_title NOT FOUND in TEMP. Make SELECT", 0)

                            # SEARCH IN MySQL
                            val_get_men_href_title = (men_href, )
                            print_log(f"SELECT href title from MySQL: {val_get_men_href_title}", 0)
                            result = run_mysql_select(SQL_GET_MEN_HREF_TITLE, val_get_men_href_title)

                            if not result:
                                print_log(f"Href_title not found in MySQL. Make Request.Get", 0)

                                # SEARCH BY SCRAPING
                                for dummy in ['one_step']:
                                    print("BBBBB")
                                    try:
                                        response = requests.get(men_href)
                                        response.raise_for_status()
                                        doc_soup = BeautifulSoup(response.content, "html.parser")

                                    except requests.exceptions.RequestException as e:
                                        print_log(f"The current page could not be opened: {men_href}", 1)
                                        print_log(e, 1)
                                        men_href_title = "PageCouldNotBeOpened"

                                        break

                                    except Exception as e:
                                        print_log(str(e), 1)
                                        sys.exit(1)

                                    try:
                                        target_div = doc_soup.find('div', id='div_Formaconsolidata')

                                    except AttributeError as e:
                                        print_log(f"'div_Formaconsolidata' was not found", 1)
                                        print_log(e, 1)
                                        men_href_title = "DivNotFound"

                                        break

                                    except Exception as e:
                                        print_log(str(e), 1)
                                        sys.exit(1)

                                    # Get the title of the document
                                    try:
                                        men_href_title = get_doc_title(target_div)

                                    except AttributeError as e:
                                        print_log(f"Title was not found", 1)
                                        print_log(e, 1)
                                        men_href_title = "TitleNotFound"

                                        break

                                    except Exception as e:
                                        print_log(str(e), 1)
                                        sys.exit(1)

                            else:
                                men_href_title = result[0][0]

                        val_insert_men = (men_text, men_start, men_end, men_href, men_href_title, men_doc_id)
                        print_log(f"INSERT MENTION: {val_insert_men}", 0)
                        run_mysql_insert(SQL_INSERT_MEN, val_insert_men)

                        print_log(f"Save men_href_title in TEMP", 0)
                        temp_men_href_title[men_href] = men_href_title

                        print_log(f"---", 0)

                    print_log(f"===============", 0)


