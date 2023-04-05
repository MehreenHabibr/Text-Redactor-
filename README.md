**MEHREEN HABIB**
---------
> #### Project Title: CS5293, spring 2023 Project 1
####Project Description:
 **This project involves redacting sensitive information i.e. name, address, phone number, gender and dates from text file and writes the redacted data into .redacted file using Natural Language processing tools like Spacy and Nltk.**
 
 #### Installation
  ****
 >**SpaCy** - Industrial-strength Natural Language Processing (NLP) in Python.
 >**en_core_web_md** - SpaCy's English pipeline optimized for CPU.
 >**nltk** - A suite of open source tools, data sets, and tutorials for Natural Language Processing research.
 >**import en_core_web_sm** - Pre-trained small English language model for spacy
 >**import en_core_web_md** - Pre-trained medium English language model for spacy
 >**Pytest** - Testing framework that supports complex functional testing.
 >**autopep8** - Tool that automatically formats Python code 
 >**Black** - Code formatter
 >**Glob** is a python module used to return all file paths that match a specific pattern.


 #### Approach to Develope the code
---
1. `get_files(args)`
  This function gets file paths using glob based on input argument. It prints error message and exits with status 1 if no input file is provided. It appends file path to files list if the file has a .txt or .md extension and does not end with requirements.txt. Finally, it returns the list of file paths.
2. `read_text_file(file_to_read)`
   This function reads the contents of a text file and returns the contents as a string.
3. `unicode_char(Word)`
   This function takes a string as input and returns a string of Unicode full block character "U+2588" that have the same length as the input string
4. `redact_names(text)`
   This function replaces all named entities that have the label "PERSON" or "ORG" and whose root is a proper noun in the input text with Unicode block characters of the same length. 
   It also creates a dictionary of the redacted named entities and their labels and returns the redacted text, the dictionary, and the count of named entities that were redacted.
5. `redact_dates(text)`
   This function redacts dates in a given text using regular expressions to match various date formats. It then replaces each matched date with a redacted version of the same length
   using the unicode_char() function. The function returns the redacted text, the list of dates found in the text, and the count of redacted dates.
6. `redact_phones(text)`
   This function takes a string text as input and returns a tuple containing the redacted version of the input text, a list of phone numbers found in the text, 
   and the count of phone numbers redacted.
7. `redact_gender(text)`
   This code redact gender-specific words by replacing them with a Unicode character.
8. `redact_address(text)`
   The redact_address function uses spaCy, to identify geographical locations and addresses in the input text. 
   It then replaces those locations with Unicode characters using the unicode_char function.
1.  `stats(args, text, file)`
    The stats() function receives command line arguments, a text string, and a file object as input. It uses separate functions to redact sensitive information such as names, 
    dates, phones, genders, and addresses from the input text
2.  `write_tostatfile(redacted_terms, count, file, args)`
    This function writes the redacted terms and the count of redactions to a file,  then appends the count and redacted terms to the stats file.
3.  `write_stdout(redacted_terms, count)`
    This function takes in the redacted terms and their count as arguments, and prints them to the console in a specific format. 
    Specifically, it prints the count of redacted terms and the redacted values themselves. This function is used to display the
    redacted information to the user when the stats argument is set to stdout.
4.  `output(args, complete_data, files)`
    The output function is responsible for writing the redacted data to the console or a file.
5.  `main(Argparser)`
    The main function parses command line arguments using the argparse module and then calls the get_files function to get the list of files to redact. It then loops through each file,
    prints stats to the console if the stats argument is set to "stdout", calls the stats function to redact sensitive information from the file, and then calls the output function to 
    write the redacted data to a file or print it to the console depending on the output argument.


pipenv install

Packages required to run this project are kept in requirements.txt file which automatically installs during installation of pipenv in step 1.


#####python_version = "3.10"

#####pytest==7.2.2

Once, the packages are successfully installed

####The project can be executed using
pipenv run python redactor.py --input *.txt --names --dates --phones --genders --address --output 'files' --stats stdout


## Tests
---
####Pytests can run using below command
pipenv run python -m pytest


###Assumptions:
---
1. Names of people and organizations are considered as names and thus redacted if --names flag is used.
2. Accuracy and performance of this application is directly dependent on SpaCy model.
3. This tools accuracy and performance is enhanced by using regular expressions along with SpaCy but unfortunately not all cases of the entities (names, phones, genders, dates and addresses) were included as regular expressions. Thus, some information may not be redacted if they were not recognized by SpaCy model or included regular expressions.


[!]([https://github.com/MehreenHabibr/cs5293sp23-project1.1/tree/main/cs5293sp23-project1])Recording #6.gif)
