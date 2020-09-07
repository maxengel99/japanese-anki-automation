'''Handles interaction with anki'''
import json
import urllib.request


class AnkiRequest:
    """Handles interaction with anki"""

    def generate_json(self, cur_word):
        """Create json for anki"""
        fields = {'Kanji': cur_word[0],
                  'Hiragana': cur_word[1], 'English': cur_word[2]}

        audio_json = {'url': 'https://raw.githubusercontent.com/maxengel99/japanese-anki-automation/master/mp3/{}.mp3'.format(cur_word[0]), 'filename': '{}.mp3'.format(cur_word[0]),
                      'fields': ['Audio']}
        deck_name = 'Japanese Vocab'
        model_name = 'Japanese Vocab'
        json_args = {'deckName': deck_name, 'modelName': model_name,
                     'fields': fields, 'options': {'allowDuplicate': False},
                     'tags': [], 'audio': audio_json}
        return {'action': 'addNote', 'params': {'note': json_args},
                'version': 6}

    def invoke(self, params):
        """Makes request to add anki card"""
        response = json.load(urllib.request.urlopen(
            'http://localhost:8765', json.dumps(params).encode('utf-8')))
        return response
