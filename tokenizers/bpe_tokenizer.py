from tokenizers.base_tokenizer import BaseTokenizer
from tokenizers.utils import sliding_window
import re

class BPETokenizer(BaseTokenizer):


    def __init__(self, vocabs=[], merges=[]):
        self.merges = merges
        self.vocabs = vocabs


    def _count_freqs(self, text):
        itext = self.divide(text)
        occs = {}
        for token1, token2 in sliding_window(itext):
            if (token1,token2) in occs:
                occs[(token1,token2)]+=1
            else:
                occs[(token1,token2)]=1
        return occs

    
    def _update_vocabs(self, text):
        vocabs = self.vocabs.copy()
        merges = self.merges.copy()
        occs = self._count_freqs(text)
        keys = max(occs.keys(), key=lambda x: occs[x])
        merges.append(keys)
        vocabs.append("".join(keys))
        return vocabs, merges


    def train(self, corpus:str, maxvocab = 100, stop_when_anomaly=True) -> list:
        words = list(set(corpus.split(sep=" ")))
        self.vocabs = list(set(list(" ".join(words))))
        self.merges = []

        pattern = r"[a-zA-Z0-9]+\s[a-zA-Z0-9]+"
        
        while len(self.vocabs)<maxvocab:
            newvocabs, newmerges = self._update_vocabs(corpus)
            if re.search(pattern, newmerges[-1][0]+newmerges[-1][1]) and stop_when_anomaly: #re.match(pattern, newmerges[-1][0]+newmerges[-1][1]):
                print("Terminalized", newmerges[-1])
                break
            self.vocabs, self.merges = newvocabs, newmerges
            print(len(self.vocabs))
        #print("' , '".join(vocabs))


    def divide(self, text):
        split = list(text)
        for pair in self.merges:
            i = 0
            while i < len(split) - 1:
                if split[i]==pair[0] and split[i+1]==pair[1]:
                    split = split[:i] + [pair[0]+pair[1]] + split[i+2:]
                else:
                    i+=1
        return split
    

    def encode(self, text):
        split = self.divide(text)
        result = []
        for token in split:
            for i, el in enumerate(self.vocabs):
                if token == el:
                    result.append(i)
                    break
        return result


    def decode(self, tokens:list) -> str:
        result = ""
        for token in tokens:
            result += self.vocabs[token]
        return result
    