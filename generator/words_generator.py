import mc, os, aiofiles
from ast import literal_eval
from mc.builtin import validators
from data.config import BANWORD

class WordsGenerator():
    def __init__(self, generate_attempts:int = 25, words_buffer:int = 500, ban_word:str = BANWORD):
        self.generate_attempts = generate_attempts  # кол-во попыток для генерации предложения
        self.words_buffer = words_buffer            # кол-во хранимых предложений/слов в каждой беседе
        self.ban_word = ban_word                    # слово, которое будет избегать бот при генерации сообщений (необяз)
        self.words_array = {}                       # глобальный список со всеми беседами и их словами
        self.dirName = "peerstext"                  # папка, в которой будут хранится все слова из бесед
        
        def read_phrases(self) -> None:
            if not os.path.isdir(self.dirName):
                os.mkdir(self.dirName)
            for i in os.listdir(self.dirName):
                file_name, _ = i.split('.')
                if file_name.isdigit():
                    with open(f"{self.dirName}/{i}", "r", encoding="utf-8") as f:
                        peer = int(file_name)
                        content = f.read()
                        self.words_array[peer] = literal_eval(content)

        read_phrases(self)


    async def write_file(self, peer_id:int, text:str) -> None:
        if peer_id not in self.words_array.keys():
            self.words_array.setdefault(peer_id, [])
        self.words_array[peer_id].append(text)
        async with aiofiles.open(f'{self.dirName}/{peer_id}.txt', 'w', encoding='utf-8') as file:
            await file.write(str(self.words_array[peer_id][-self.words_buffer:]))   # магия, сохраняем выбранный буфер сообщений


    async def generate_message(self, peer_id:int) -> str:
        generator = mc.PhraseGenerator(self.words_array[peer_id])
        result = generator.generate_phrase(attempts=self.generate_attempts, validators=[validators.words_count(minimal=1, maximal=10)])
        if result is None:  # почему-то, иногда оно отказывается генерировать с выбранными параметрами(??)
            result = generator.generate_phrase()
        if self.ban_word in result.lower(): # если выпало бан-слово, то исключаем и пробуем сгенерировать заново
            self.words_array[peer_id].remove(self.ban_word)
            generator = mc.PhraseGenerator(self.words_array[peer_id])
            result = generator.generate_phrase(attempts=self.generate_attempts, validators=[validators.words_count(minimal=1, maximal=10)])
        return result

