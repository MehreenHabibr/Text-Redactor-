import argparse  # For parsing command line arguments
import glob  # For retrieving a list of files that match a specified pattern
import spacy  # For natural language processing
import re  # For working with regular expressions
import sys  # For interacting with the system and reading/writing files
import ntpath  # For working with file paths on Windows systems
import os  # For interacting with the operating system and file system
import en_core_web_sm  # Pre-trained small English language model for spacy
import en_core_web_md  # Pre-trained medium English language model for spacy
from spacy.matcher import (
    Matcher,
)  # For matching linguistic patterns in text using spacy

global final_data  # Declares a global variable named 'final_data' that can be accessed and modified from anywhere in the code.


def get_files(args):
    files = []  # Initialize an empty list to store file paths
    if not args.input:  # Check if input argument is not provided
        print("No file to redact.", file=sys.stderr)  # Print error message to stderr
        sys.exit(1)  # Exit with status code 1
    for input_path in args.input:  # Loop through input paths
        input_files = glob.glob(
            input_path
        )  # Get a list of files that match the pattern
        if not input_files:  # Check if no files are found
            print(
                f"No text file found for input{input_path}", file=sys.stderr
            )  # Print error message to stderr
            sys.exit(1)  # Exit with status code 1

        for file in input_files:  # Loop through input files
            if file.endswith((".txt", ".md")) and not file.endswith(
                "requirements.txt"
            ):  # Check if file has a .txt or .md extension and does not end with requirements.txt
                files.append(file)  # Append the file path to the list of files
    return files  # Return the list of file paths


def read_text_file(file_to_read):
    try:
        with open(file_to_read, "r", encoding="utf-8") as file:
            text = file.read()
    except IOError:
        print(f"Unable to open file: {file_to_read}")
        text = ""
    return text


def unicode_char(word):
    return "\u2588" * len(word)


def redact_names(text):
    names = {}
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    name_entity = ["PERSON", "ORG"]
    prop_noun = ["NOUN", "PROPN"]
    count = 0
    for ent in doc.ents:
        if ent.label_ in name_entity and ent.root.pos_ in prop_noun:
            count += 1
            # redacted_name = "█" * len(ent.text)
            text = text.replace(ent.text, unicode_char(ent.text))
            names[ent.text] = ent.label_
    return text, names, count


def redact_dates(text):
    date_types = r"\d{1,2}[-\./\s]\d{1,2}[-\./\s]\d{2,4}|\d{2}[./\s]\d{1}[./\s]\d{2}|\d{2}[./\s]\d{1}[-\./\s]\d{2}|\d{1}[-\./\s]\d{2}[-\./\s]\d{2}|\d{1,2}[-\./\s]\d{1,2}[-\./\s]\d{2,4}|\d{2,4}[-\./\s]\d{1,2}}[-\./\s]\d{1,2}|\d{1,2}\s+(?:January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[\s,]*\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[th]*[\s,]*\d{2,4}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}[th]*|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{1,2}|(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)|\d{1,2}[th]*[\s,]*(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{2,4}|\d{1,2}[\s,]*(?:January|February|March|April|May|June|July|August|September|October|November|December|Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Sept|Oct|Nov|Dec)[\s,]*\d{2,4}"
    dates = [date for date in re.findall(date_types, text)]
    count = 0
    redacted_text = text
    for date in dates:
        redacted_date = unicode_char(str(date))
        if redacted_date != str(date):
            count += len(re.findall(str(date), text))
            redacted_text = redacted_text.replace(str(date), redacted_date)
    return redacted_text, dates, count


def redact_phones(text):
    phones = []
    #    phone_number = r'(?:\()?(\d{3})(?:\))?[-.\s]?(\d{3})[-.\s]?(\d{4})'
    phone_number = r"\(?\d{3}\)?\s?[-.\s]?\s?\d{3}\s*[-.\s]?\s?\d{4}"
    redacted_text, count = re.subn(
        phone_number, lambda match: unicode_char(match.group()), text
    )
    phones = re.findall(phone_number, text)
    return redacted_text, phones, count


def redact_gender(text):
    gender = {
        "he",
        "she",
        "him",
        "her",
        "his",
        "himself",
        "herself",
        "male",
        "female",
        "men",
        "women",
        "ms",
        "mr",
        "miss",
        "mr.",
        "ms.",
        "boy",
        "girl",
        "boys",
        "girls",
        "lady",
        "ladies",
        "gentleman",
        "gentlemen",
        "guy",
        "hero",
        "heroine",
        "spokesman",
        "spokeswoman",
        "boyfriend",
        "boyfriends",
        "girlfriend",
        "girlfriends",
        "brother",
        "brothers",
        "sister",
        "sisters",
        "mother",
        "father",
        "mothers",
        "fathers",
        "grandfather",
        "grandfathers",
        "grandmother",
        "grandmothers",
        "mom",
        "dad",
        "moms",
        "dads",
        "king",
        "kings",
        "queen",
        "queens",
        "aunt",
        "aunts",
        "uncle",
        "uncles",
        "niece",
        "nieces",
        "nephew",
        "nephews",
        "groom",
        "bridegroom",
        "grooms",
        "bridegrooms",
        "son",
        "sons",
        "daughter",
        "daughters",
        "waiter",
        "waitress",
    }
    gender_list = []
    for found_gender in re.findall(
        r"\b({})\b".format("|".join(gender)), text, re.IGNORECASE
    ):
        gender_list.append(found_gender)
        text = text.replace(found_gender, unicode_char(str(found_gender)))
    count = len(gender_list)
    return text, gender_list, count


def redact_address(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)
    count = 0
    address_list = []
    for ent in doc.ents:
        if ent.label_ in ["GPE", "LOC"]:
        
            count += 1
            address_list.append(ent.text)
            text = re.sub(re.escape(ent.text), unicode_char(ent.text), text)
    return text, address_list, count

def stats(args, text, file):
    final_data = text
    redaction_funcs = [
        (args.names, redact_names, "Redacted Names"),
        (args.dates, redact_dates, "Redacted Dates"),
        (args.phones, redact_phones, "Redacted Phones"),
        (args.genders, redact_gender, "Redacted Genders"),
        (args.address, redact_address, "Redacted Address"),
    ]
    for redact, func, label in redaction_funcs:
        if redact:
            final_data, data, count = func(final_data)
            if args.stats == "stdout":
                print(label)
                write_stdout(data, count)
            elif args.stats != "stderr":
                write_tostatfile(data, count, file, args)
    if args.stats == "stderr":
        print("No Error Found", file=sys.stderr)
    return final_data


def write_tostatfile(redacted_terms, count, file, args):
    # create directory for storing stats files
    stats_dir = os.path.join(os.getcwd(), str(args.stats).strip("'"))
    os.makedirs(stats_dir, exist_ok=True)

    # create stats file path
    filename = os.path.basename(file).split(".")[0] + ".stats"
    stats_file = os.path.join(stats_dir, filename)

    # write stats to file
    with open(stats_file, "a", encoding="utf-8") as f:
        f.write(f"No. of redacted terms = {count}\n")
        f.write(f"Redacted values = {redacted_terms}\n")


def write_stdout(redacted_terms, count):
    print(f"No. of redacted terms = {count}")
    print(f"Redacted values = {redacted_terms}\n")


def output(args, complete_data, files):
    if args.output == "stdout":
        print(
            f"\n============ Redacted data output from {files} file ==============\n{complete_data}"
        )
    elif args.output == "stderr":
        print("No Error Found", file=sys.stderr)
    else:
        cwd = os.getcwd()
        folder_path = os.path.join(cwd, str(args.output).strip("'"))
        os.makedirs(folder_path, exist_ok=True)
        output_file = os.path.join(folder_path, f"{os.path.basename(files)}.redacted")
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(complete_data)


def main(Argparser):
    args = Argparser.parse_args()
    for file in get_files(args):
        print(
            f"\n{'='*25} STATS AFTER REDACTING  {file.split('.')[0]} {'='*25}\n"
        ) if args.stats == "stdout" else None
        output(args, stats(args, read_text_file(file), file), file)


if __name__ == "__main__":
    Argparser = argparse.ArgumentParser()
    # Add arguments to the parser
    Argparser.add_argument(
        "--input",
        type=str,
        required=True,
        nargs="+",
        help="Patterns of input files to be redacted",
    )
    Argparser.add_argument(
        "--names", action="store_true", help="Flag to enable redaction of names"
    )
    Argparser.add_argument(
        "--dates", action="store_true", help="Flag to enable redaction of dates"
    )
    Argparser.add_argument(
        "--phones",
        action="store_true",
        help="Flag to enable redaction of phone numbers",
    )
    Argparser.add_argument(
        "--genders", action="store_true", help="Flag to enable redaction of genders"
    )
    Argparser.add_argument(
        "--address", action="store_true", help="Flag to enable redaction of addresses"
    )
    Argparser.add_argument(
        "--output",
        type=str,
        required=True,
        help="Output file path to write redacted data",
    )
    Argparser.add_argument("--stats", help="Flag to print stats after redaction")

    main(Argparser)
