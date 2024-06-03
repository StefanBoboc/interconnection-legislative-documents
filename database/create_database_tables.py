import mysql.connector as mysql

mydb = mysql.connect(
    host="127.0.0.1",
    user="root",
    passwd="xxxxx",
    database="dataset"
)


# mycursor = mydb.cursor()
#
# mycursor.execute("""
# DROP TABLE PRD_MENTION
# """)
#
# mycursor.execute("""
# DROP TABLE PRD_DOCUMENT
# """)
#
# mycursor.execute("""
# CREATE TABLE PRD_DOCUMENT (
#     doc_id INTEGER NOT NULL,
#     doc_title VARCHAR(500) NOT NULL,
#     doc_url VARCHAR(200) NOT NULL,
#     doc_content VARCHAR(200),
#     doc_date VARCHAR(11),
#     PRIMARY KEY (doc_id)
# )""")
#
# mycursor.execute("""
# CREATE TABLE PRD_MENTION (
#     men_id INTEGER AUTO_INCREMENT,
#     men_text VARCHAR(300) NOT NULL,
#     men_start INTEGER NOT NULL,
#     men_end INTEGER NOT NULL,
#     men_href VARCHAR(200) NOT NULL,
#     men_href_title VARCHAR(500),
#     doc_id INTEGER,
#     PRIMARY KEY (men_id),
#     FOREIGN KEY (doc_id) REFERENCES PRD_DOCUMENT(doc_id)
# )""")

# mycursor.execute("""
# CREATE TABLE DOCUMENT (
#     doc_id INTEGER AUTO_INCREMENT,
#     doc_title VARCHAR(500) NOT NULL,
#     doc_url VARCHAR(200) NOT NULL UNIQUE,
#     doc_url_code VARCHAR(100) NOT NULL UNIQUE,
#     doc_content VARCHAR(100),
#     doc_date VARCHAR(11),
#     PRIMARY KEY (doc_id)
# )""")
#
# mycursor.execute("""
# CREATE TABLE MENTION (
#     mention_id INTEGER AUTO_INCREMENT,
#     href_text VARCHAR(300) NOT NULL,
#     start_pos INTEGER NOT NULL,
#     end_pos INTEGER NOT NULL,
#     doc_id INTEGER,
#     doc_id_ref INTEGER,
#     PRIMARY KEY (mention_id),
#     FOREIGN KEY (doc_id) REFERENCES DOCUMENT(doc_id),
#     FOREIGN KEY (doc_id_ref) REFERENCES DOCUMENT(doc_id)
# )""")
