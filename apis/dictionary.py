import requests
import aiohttp
from decouple import config


headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}


class AntiBozo:
    def __init__(self) -> None:
        self._API_KEY = config('WORDNIK_API_KEY')

    async def word_of_the_day(self):
        url = f'https://api.wordnik.com/v4/words.json/wordOfTheDay?api_key={self._API_KEY}'
        session = aiohttp.ClientSession()
        async with session.get(url, headers=headers) as res:
            word_of_the_day_dictionary = {}

            word = await res.json().get('word')
            part_of_speech = res.json().get('definitions')[
                0].get('partOfSpeech')
            definition = res.json().get('definitions')[0].get('text')
            examples = res.json().get('examples')[0].get('text')
            note = res.json().get('note')

            word_of_the_day_dictionary.update(
                {'word': word,
                 'part_of_speech': part_of_speech,
                 'definition': definition,
                 'examples': examples,
                 'note': note
                 })
        # res = requests.get(url, headers=headers)
        # print(res.elapsed.total_seconds())
        await session.close()
        return word_of_the_day_dictionary

    async def word_search(self, word):

        url = f'https://api.wordnik.com/v4/word.json/{word}/definitions?limit=15&includeRelated=false&useCanonical=false&includeTags=false&api_key={self._API_KEY}'
        session = aiohttp.ClientSession()
        async with session.get(url, headers=headers) as res:
            definition_list = await res.json()
            for dictionary in definition_list[:1]:
                definition = dictionary.get('text')
                part_of_speech = dictionary.get('partOfSpeech')
        await session.close()
        return definition, part_of_speech
        # res = requests.get(url, headers=headers)
        # print(res.elapsed.total_seconds())
