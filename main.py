'''
This is an interactive english dictionary to use from the terminal with no GUI.
The user should is asked to input a word and gets a definition of that word for return.
If the word is not in the underlying data, the dictionary tries to display a like-wise word.
'''

import json
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

    with open("data.json", "r") as file:
        global data
        data = json.load(file)

    return user_input, data


def lookup_word(word):
    """A function to find the user word in the dict"""

    if word.lower() in data:
        found_word(word)
    elif word.title() in data:
        found_word(word.title())
    elif word not in data:
        if alternate_word(word):
            pass
        else:
            sorry()
    return


def sorry():
    print("\b")
    print("Sorry, I could not find your word. Please double check it.")
    print("\b")
    return


def found_word(word):
    print("\b")
    print("The output of the dictionary is as follows: ")
    for respond in data[word]:
        print(f"* {respond}")
    print("\b")
    return


def alternate_word(word):
    """A function to search for a alternate word in the dict and propose that to the user"""
    # define patterns using the keys from the dict
    patterns = [key for key in data]

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


