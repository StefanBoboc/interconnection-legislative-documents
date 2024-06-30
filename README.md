# interconnection-legislative-documents

## Dataset Overview

The dataset was obtained by scraping the Romanian Ministry of Internal Affairs platform for documents published in the Official Gazette from 2017 to 2023 (https://legislatie.just.ro/). 

The `interconnection-legislative-documents-dataset.zip` archive consists of two components:

### 1. \dataframes

Three JSON files compressed with gzip, containing a total of `1.343.705` records, each with `14 features`:

- `mention_id`: ID of the mention
- `mention_text`: Text of the mention
- `mention_url_title_id`: ID of the document title to which the mention refers
- `mention_url_title`: Title of the document to which the mention refers
- `mention_url`: URL of the document to which the mention refers
- `mention_phrase_text`: Text of the phrase in which the mention was identified (the phrase is also part of the `df['document_text']`)
- `mention_start_pos_in_phrase_text`: Position where the mention starts in the phrase
- `mention_end_pos_in_phrase_text`: Position where the mention ends in the phrase
- `mention_start_pos_in_document_text`: Position where the mention starts in the entire document text
- `mention_end_pos_in_document_text`: Position where the mention ends in the entire document text
- `document_id`: ID of the document in which the mention was identified
- `document_title`: Title of the document in which the mention was identified
- `document_text`: Path to the file containing the text of the document in which the mention was identified
- `document_url`: URL of the document in which the mention was identified

### 2. \document_content

Files containing the text of the documents where all mentions from the dataframes were identified. 

This directory has the following hierarchy: `\document_content\yyyy\mm\dd\yyyymmddxxx_content.txt`, where:

- `yyyy` represents the publication year of the document
- `mm` represents the publication month of the document
- `dd` represents the publication day of the document
- `xxx` is the document ID for that day

This path is referenced in `df['document_text']`.

***

## Loading Dataframes

Download the zip archive, extract it, and to load the 3 JSON files, run the following code:
```
import pandas as pd
import gzip

# Initialize an empty list to store loaded DataFrames
loaded_dfs = []

# Number of chunks/files
num_chunks = 3 

# Load each chunk from the gzipped JSON files
for i in range(1, num_chunks + 1):
    file_name = f'interconnection-legislative-documents_{i}.json.gz'
    with gzip.open(file_name, 'rt', encoding='utf-8') as f:
        chunk_df = pd.read_json(f, orient='records', lines=True)
        loaded_dfs.append(chunk_df)

# Concatenate all loaded DataFrames into a single DataFrame
df = pd.concat(loaded_dfs, ignore_index=True)

# Now df contains the concatenated DataFrame from all chunks/files
df.head()
```

***

## Statistics

:warning: The dataset has been reprocessed, so there may be slight discrepancies between the dataset and the following statistics :warning:

### General Dataset Statistics
- Number of unique mentions: 229,503
- Total number of titles (unique): 42,761
- Titles with the top k most mentions:

| TITLE | MENTIONS NBR. TO IT | TOP | 
|----------|-------------------|-----|
| CONSTITUȚIE*) din 21 noiembrie 1991 (\*republicată\*) | 184,210 | 1 |
| PageCouldNotBeOpened | 57,671 | 2 |
| LEGE nr. 47 din 18 mai 1992 (\*\*republicată\*\*) | 53,615 | 3 |
| CODUL DE PROCEDURĂ PENALĂ din 1 iulie 2010 | 40,157 | 4 |
| CODUL DE PROCEDURĂ CIVILĂ din 1 iulie 2010 (\*\*republicat\*\*) | 32,409 | 5 |
| LEGE nr. 77 din 28 aprilie 2016 | 32,174 | 6 |
| CODUL PENAL din 17 iulie 2009 | 20,806 | 7 |
| LEGE nr. 334 din 17 iulie 2006 (\*\*republicată\*\*) | 18,733 | 8 |
| CODUL FISCAL din 8 septembrie 2015 | 18,118 | 9 |
| ORDONANȚĂ DE URGENȚĂ nr. 57 din 3 iulie 2019 | 15,510 | 10 |

- Average length of mentions (~34), longest (1247) and shortest (1)
- Average length in words of the documents (TBA)

### Particulary Dataset Statistics

#### PRD_DOCUMENT - Initial form of the documents dataset

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

#### PRD_MENTION - Initial form of the mentions dataset
- Total mentions: 1,449,027
- Total unique mentions: 229,503

#### UNIQUE_DOCUMENT - After removing duplicates
- Total processed documents: 63,618
- Unique titles: 60,797
- Unique URLs: 63,618

#### UNIQUE_MENTION - After removing duplicates based on FK(doc_id)
- Total mentions found: 1,440,242
- Total unique mentions: 229,503
- Mentions that could not be accessed (9,957 unique links)
    - PageCouldNotBeOpened: 57,671 (9,914 unique links)
        - Wrong link casting: 1,131 (unique links)
        - MailTo: 6,486 (unique links)
        - Error 502: 2,297 (unique links)
    - TitleNotFound: 295 (Act in process, Act is repealed!) (43 unique links)
