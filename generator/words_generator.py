import mc, os, aiofiles
from ast import literal_eval
from mc.builtin import validators
from data.config import BANWORD

class WordsGenerator():
    def __init__(self, generate_attempts = 25, words_buffer = 500, ban_word = BANWORD):
        self.generate_attempts = generate_attempts
        self.words_buffer = words_buffer
        self.ban_word = ban_word
        self.words_array = {}
        self.dirName = "peerstext"
        
        def read_phrases(self):
            for i in os.listdir(self.dirName):
                file_name, _ = i.split('.')
                if file_name.isdigit():
                    with open(f"{self.dirName}/{i}", "r", encoding="utf-8") as f:
                        peer = int(file_name)
                        content = f.read()
                        self.words_array[peer] = literal_eval(content)

        read_phrases(self)


    async def write_file(self, peer_id, text):
        if peer_id not in self.words_array.keys():
            self.words_array.setdefault(peer_id, [])
        self.words_array[peer_id].append(text)
        async with aiofiles.open(f'{self.dirName}/{peer_id}.txt', 'w', encoding='utf-8') as file:
            await file.write(str(self.words_array[peer_id][-self.words_buffer:]))


    async def generate_message(self, peer_id):
        generator = mc.PhraseGenerator(self.words_array[peer_id])
        result = generator.generate_phrase(attempts=self.generate_attempts, validators=[validators.words_count(minimal=1, maximal=10)])
        if result is None:
            result = generator.generate_phrase()
        if self.ban_word in result.lower():
            self.words_array[peer_id].remove(self.ban_word)
            generator = mc.PhraseGenerator(self.words_array[peer_id])
            result = generator.generate_phrase(attempts=self.generate_attempts, validators=[validators.words_count(minimal=1, maximal=10)])
        return result

