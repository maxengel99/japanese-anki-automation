'''Starts the textbox conversation'''
import os
import easygui
from github_handler import GithubHandler
from helper import create_audio
from anki_request import AnkiRequest
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_text_file():
    '''Read in textfile from user and returns content'''

    print("Uploading text file")

    vocab_file_name = easygui.fileopenbox(
        "Please upload a textfile of the new vocabulary.")
    vocab_file_open = (
        open(vocab_file_name, 'r', encoding='utf8', errors='ignore'))

    return vocab_file_open.readlines()


def get_khmer_def_pair(vocab_file_content):
    '''Returns pair array for khmer word and English definition'''

    print("Creating Khmer-English array")
    khmer_def_pair_arr = []

    for line in vocab_file_content:
        khmer_def_pair = line.rstrip().split('/')
        khmer_def_pair_arr.append(khmer_def_pair)

    return khmer_def_pair_arr


def check_create_and_add_audio(khmer_def_pair_arr):
    '''Creates and adds audio files to github'''

    github_handler = GithubHandler()
    processes = []

    with ThreadPoolExecutor(max_workers=10) as executor:
        for pair in khmer_def_pair_arr:
            if not os.path.isfile('files/words/{}.mp3'.format(pair[0])):
                processes.append(executor.submit(
                    create_audio, "words", pair[0]))
                print("Adding audio creation process for - {}".format(pair[1]))
            else:
                print("Skipping word - {}".format(pair[1]))

    for task in as_completed(processes):
        print(task.result())

    commit_message = easygui.enterbox()
    github_handler.add_to_github(commit_message)


def add_vocab_to_anki(khmer_def_pair_arr):
    '''Adds vocab and audio to anki deck, must have anki open'''

    print("Begin adding new vocab to Anki deck")

    anki_request = AnkiRequest()
    for pair in khmer_def_pair_arr:
        anki_arg = anki_request.generate_json('words', pair[0], pair[1])
        response = anki_request.invoke(anki_arg)
        print(response)

    print("Completed adding vocab to anki")


def begin():
    '''Starts the textbox conversation'''

    category = easygui.buttonbox(
        "Would you like to upload letters or vocabulary?",
        choices=('Letters', 'Vocabulary'))

    if(category == "Vocabulary"):
        vocab_file_content = get_text_file()
        khmer_def_pair_arr = get_khmer_def_pair(vocab_file_content)
        print(khmer_def_pair_arr)
        audio_option = easygui.ynbox(
            "Do you need to create audio?", choices=("Yes", "No"))

        print(khmer_def_pair_arr)
        if audio_option:
            print("test")
            check_create_and_add_audio(khmer_def_pair_arr)

        add_vocab_to_anki(khmer_def_pair_arr)

    elif(category.lower() == "letters"):
        print("Letters is not supported yet")
    user_continue = easygui.ynbox(
        "Would you like to perform another command?", choices=("Yes", "No"))

    if user_continue:
        begin()
    else:
        exit()


if __name__ == '__main__':
    begin()
