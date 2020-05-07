'''
This is an interactive english dictionary to use from the terminal with no GUI.
The user should is asked to input a word and gets a definition of that word for return.
If the word is not in the underlying data, the dictionary tries to display a like-wise word.
'''

import json
import sqlalchemy
import pymysql
import os
from difflib import get_close_matches


def main():
    """This is the main function for the program logic"""
    shout_out_and_load()
    lookup_word(user_input)
    continue_question()
    return


def shout_out_and_load():
    """A function to greet the user ans ask for his word. Afterwards loading the data.json file into the dict"""

    print("Hello there! Thank you for using my english dictionary. " 
          "What word can I look up for you?")
    # don't convert the user input to lower case yet, first check if it's a noun and in the list
    global user_input
    user_input = input("Please enter a word: ")
    return user_input


def lookup_word(word):

    """A function to find the user word in the database and create the connection with the database"""
    user = os.environ['USER']
    pw = os.environ['PW']

    engine = sqlalchemy.create_engine(f'mysql+pymysql://{user}:{pw}@localhost/Dictionary')
    global connection
    connection = engine.connect()
    metadata = sqlalchemy.MetaData()
    newTable = sqlalchemy.Table('dict', metadata, autoload=True, autoload_with=engine)


    def set_query(w):
        "A function to create the query for the database"
        query = f'SELECT definition FROM DICT WHERE word="{w}";'
        result_proxy = connection.execute(query)
        global result
        result = result_proxy.fetchall()
        return result

    set_query(word)

    if len(result) > 0:
        found_word(result)
    elif len(result) == 0:
        title_word = word.title()
        set_query(title_word)
        if len(result) > 0:
            found_word(result)
        elif len(result) == 0:
            upper_word = word.upper()
            set_query(upper_word)
            if len(result) > 0:
                found_word(result)
            elif len(result) == 0:
                alternate_word(word)
    else:
        sorry()
    return result, connection


def sorry():
    print("\b")
    print("Sorry, I could not find your word. Please double check it.")
    print("\b")
    return


def found_word(result):
    print("\b")
    print("The output of the dictionary is as follows: ")
    for respond in result:
        # get rid of the ,) stuff with regex
        print(f"* {respond}")
    print("\b")
    return


def alternate_word(word):
    """A function to search for an alternate word in the dict database and propose that to the user"""

    # define patterns using the words from the database
    query = f'SELECT word FROM DICT;'
    result_proxy = connection.execute(query)
    global result
    patterns = result_proxy.fetchall()

    # get the close matches, default list length is 3
    close_list = get_close_matches(word, patterns)

    # for every word in the list: ask the user if he meant this
    ask = False
    for alt in close_list:
        print(f"Did you mean {alt}?")
        user_answer = input("Please respond with [y]es or [n]o: ")
        if user_answer == 'y':
            ask = True
            lookup_word(alt)
            break
        elif user_answer == 'n':
            ask = False
    return ask


def continue_question():
    """A function to ask the user whether to continue or quit"""

    answer = input("Do you want to look up another word or do you want to quit? "
                   "Please enter [c]ontinue or [q]uit: ")
    print("\b")
    if answer == 'c':
        main()
    elif answer == 'q':
        print("Bye bye!")
    else:
        print("Something went wrong. Please enter 'c' or 'q'.")
        continue_question()
    return


if __name__ == '__main__':
    main()

