
from typing import Any


class BaseTokenizer:

    
    def __init__(self, vocabs=None) -> None:
        if vocabs:
            self.vocabs = vocabs
    

    def train(self, corpus:str) -> list:
        pass


    def encode(self, text:str) -> list:
        pass


    def decode(self, tokens:list) -> str:
        pass


    def __call__(self, obj: str | list) -> Any:
        if type(obj) == type(str):
            return self.encode(obj)
        elif type(obj) == type(list):
            return self.decode(obj)
        else:
            return None


    def count_tokens(self, text: str) -> int:
        return len(self.encode(text))