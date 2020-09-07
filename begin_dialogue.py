'''Starts the textbox conversation'''
import os
import easygui
from anki_request import AnkiRequest
from concurrent.futures import ThreadPoolExecutor, as_completed


def get_text_file():
    '''Read in textfile from user and returns content'''

    vocab_file_name = easygui.fileopenbox(
        "Please upload a textfile of the new vocabulary.")
    vocab_file_open = (
        open(vocab_file_name, 'r', encoding='utf8', errors='ignore'))

    return vocab_file_open.readlines()


def parse_vocab_content(vocab_file_content):
    '''Returns tuple object with kanji, hiragana, and English definitition'''
    vocab_info = []

    for line in vocab_file_content:
        cur_info = line.rstrip().split('/')
        vocab_info.append(cur_info)

    return vocab_info


def create_audio(category, word):

    first_url = "https://kheng.info/static/dictionary/audio/" + word + ".mp3"
    doc = requests.get(first_url)

    if doc.status_code == 200:
        filename = 'files/{}/{}.mp3'.format("words", word)
        with open(filename, "wb") as file:
            print('writing file {}'.format(filename))
            file.write(doc.content)

        return

    print("First audio link doesn't have the file")

    '''creates the audio file'''
    url = "https://translate.google.com/translate_tts?ie=UTF-8&tl=km&client=tw-ob&q=" + word

    # url = 'https://translate.google.com/translate_tts?'
    # 'ie=UTF-8&tl=km&client=tw-ob&q={}'.format(word)
    print(url)
    doc = requests.get(url)
    filename = 'files/{}/{}.mp3'.format(category, word)
    print(filename)
    with open(filename, "wb") as file:
        print('writing file {}'.format(filename))
        file.write(doc.content)
        print("File writing completed for " + word)

    return "completed"


def create_and_save_info(vocab_info):
    '''Create and saves audio files to ./mp3'''

    processes = []
    with ThreadPoolExecutor(max_workers=10) as executor:
        hiragana_word = cur_word[1]
        for cur_word in vocab_info:
            if not os.path.isfile('mp3/{}.mp3'.format(hiragana_word)):
                print('Adding audio for {}'.format(hiragana_word))
                processes.append(executor.submit(
                    create_audio, hiragana_word))
            else:
                print('Skipping word - {}'.format(hiragana_word)

    for task in as_completed(processes):
        print(task.result())

def add_vocab_to_anki(vocab_info):
    '''Adds vocab and audio to anki deck, must have anki open'''

    anki_request=AnkiRequest()

    for pair in vocab_info:
        anki_arg=anki_request.generate_json('words', pair[0], pair[1])
        response=anki_request.invoke(anki_arg)
        print(response)

    print("Completed adding vocab to anki")


def begin():
    '''Starts the textbox conversation'''

    print("Beginning dialogue")

    vocab_file_content=get_text_file()
    vocab_info=parse_vocab_content(vocab_file_content)

    print('Creating audio')

    create_and_save_audio(vocab_info)

    print('Adding to Anki deck')

    add_vocab_to_anki(vocab_info)

    user_continue=easygui.ynbox(
        "Would you like to perform another command?", choices=("Yes", "No"))

    if user_continue:
        begin()
    else:
        exit()


if __name__ == '__main__':
    begin()
