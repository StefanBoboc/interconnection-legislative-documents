# interconnection-legislative-documents

## General Dataset Statistics
- Number of unique mentions: 229,503
- Total number of titles (unique): 42,761
- Titles with the top k most mentions:

| TITLE | MENTIONS NBR. TO IT | TOP | 
|----------|-------------------|-----|
| CONSTITUTION*) from November 21, 1991 (\*republished\*) | 184,210 | 1 |
| PageCouldNotBeOpened | 57,671 | 2 |
| LAW no. 47 from May 18, 1992 (\*\*republished\*\*) | 53,615 | 3 |
| CODE OF CRIMINAL PROCEDURE from July 1, 2010 | 40,157 | 4 |
| CODE OF CIVIL PROCEDURE from July 1, 2010 (\*\*republished\*\*) | 32,409 | 5 |
| LAW no. 77 from April 28, 2016 | 32,174 | 6 |
| PENAL CODE from July 17, 2009 | 20,806 | 7 |
| LAW no. 334 from July 17, 2006 (\*\*republished\*\*) | 18,733 | 8 |
| FISCAL CODE from September 8, 2015 | 18,118 | 9 |
| EMERGENCY ORDINANCE no. 57 from July 3, 2019 | 15,510 | 10 |

- Average length of mentions (~34), longest (1247) and shortest (1)
- Average length in words of the documents (TBA)

## Particulary Dataset Statistics

### PRD_DOCUMENT - Initial form of the documents dataset

- Scanned legislative documents: 64,249
- Documents with unique titles: 60,797
- Documents with identical titles: 1,533 (3,452 duplicate titles)
- Number of scanned documents per year

| YEAR | DOCUMENTS COUNT |
|------|-----------------|
| 2017 | 7,802           |
| 2018 | 7,898           |
| 2019 | 8,312           |
| 2020 | 9,908           |
| 2021 | 10,633          |
| 2022 | 10,022          |
| 2023 | 9,674           |

- No NULL values in any column

- Unique links: 63,618. This means we have duplicate links: 64,249 (total) - 63,618 (unique) = 631 (duplicates). There is only the occurrence of the same link twice (scraping error???), which accounts for some of the duplicate titles.

### PRD_MENTION - Initial form of the mentions dataset
- Total mentions: 1,449,027
- Total unique mentions: 229,503

### UNIQUE_DOCUMENT - After removing duplicates
- Total processed documents: 63,618
- Unique titles: 60,797
- Unique URLs: 63,618

### UNIQUE_MENTION - After removing duplicates based on FK(doc_id)
- Total mentions found: 1,440,242
- Total unique mentions: 229,503
- Mentions that could not be accessed (9,957 unique links)
    - PageCouldNotBeOpened: 57,671 (9,914 unique links)
        - Wrong link casting: 1,131 (unique links)
        - MailTo: 6,486 (unique links)
        - Error 502: 2,297 (unique links)
    - TitleNotFound: 295 (Act in process, Act is repealed!) (43 unique links)
