import heapq
import nltk
import re
import bs4 as bs
import urllib.request

class summary_bot():
    text=""
    def __init__(self,url):
        self.source=urllib.request.urlopen(url).read()
        self.soup=bs.BeautifulSoup(self.source,'lxml')

    def summarize(self,max_len,summary_sen):
        for paragraph in self.soup.find_all('p'):
            self.text+=paragraph.text
        #preprocessing
        self.text=re.sub(r'\[[0-9]*\]',' ',self.text)
        self.text=re.sub(r'\s+',' ',self.text)

        self.clean_text=self.text.lower()
        self.clean_text=re.sub(r'\W',' ',self.clean_text)
        #self.clean_text=re.sub(r'\d',' ',self.clean_text)
        self.clean_text=re.sub(r'\s+',' ',self.clean_text)
        
        self.sentences=nltk.sent_tokenize(self.text)
        self.stop_words=nltk.corpus.stopwords.words('english')
        self.word2count={}

        for word in nltk.word_tokenize(self.clean_text):
            if word not in self.stop_words:
                if word not in self.word2count.keys():
                    self.word2count[word]=1
                else:
                    self.word2count[word]+=1
        
        for key in self.word2count.keys():
            self.word2count[key]=self.word2count[key]/max(self.word2count.values())

        self.sent2score={}
        for sentence in self.sentences:
            for word in nltk.word_tokenize(sentence.lower()):
                if word in self.word2count.keys():
                    if len(sentence.split(' '))<max_len:
                        if sentence not in self.sent2score.keys():
                            self.sent2score[sentence]=self.word2count[word]
                        else:
                            self.sent2score[sentence]+=self.word2count[word]

        self.best_sentence=heapq.nlargest(summary_sen,self.sent2score,key=self.sent2score.get)
        return self.best_sentence