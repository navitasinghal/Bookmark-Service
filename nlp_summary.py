from flask import Flask, jsonify
from flask_restplus import Resource, Api
import chrome_bookmarks
import json
from flask_cors import CORS
import random
import argparse
from collections import defaultdict
import sys
if sys.version_info >= (3,):
    import queue
else:
    import Queue as queue
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from nltk import tokenize

app = Flask(__name__)
CORS(app)
api = Api(app)

@api.route('/health')
class HelloWorld(Resource):
    def get(self):
        return {'hello': 'world'}

@api.route('/bookmark/folder' , endpoint='bookmark')
class Bookmark(Resource):
    def get(self):
        array=[]
        i=0
        for folder in chrome_bookmarks.folders:
            array.append({"folderName" : folder.name, "urls":[] })
            for url in folder.urls:
                array[i]["urls"].append(url)
            i+=1
        data=(json.dumps({"data":array}))
        return array, 201

def get_next_state(markov_chain, state):
    next_state_items = list(markov_chain[state].items())
    next_states = [x[0] for x in next_state_items]
    next_state_counts = [x[1] for x in next_state_items]
    total_count = sum(next_state_counts)
    next_state_probabilities = []
    probability_total = 0
    for next_state_count in next_state_counts:
        probability = float(next_state_count) / total_count
        probability_total += probability
        next_state_probabilities.append(probability_total)
    sample = random.random()
    for index, next_state_probability in enumerate(next_state_probabilities):
        if sample <= next_state_probability:
            return next_states[index]
    return None

def tokenise_text_file(file_name):
    return file_name.split()

def create_markov_chain(tokens, order):
    if order > len(tokens):
        raise Exception('Order greater than number of tokens.')
    markov_chain = defaultdict(lambda: defaultdict(int))
    current_state_queue = queue.Queue()
    for index, token in enumerate(tokens):
        if index < order:
            current_state_queue.put(token)
            if index == order - 1:
                current_state = ' '.join(list(current_state_queue.queue))
        elif index < len(tokens):
            current_state_queue.get()
            current_state_queue.put(token)
            next_state = ' '.join(list(current_state_queue.queue))
            markov_chain[current_state][next_state] += 1
            current_state = next_state
    return markov_chain

def get_random_state(markov_chain):
    uppercase_states = [state for state in markov_chain.keys() if state[0].isupper()]
    if len(uppercase_states) == 0:
        return random.choice(list(markov_chain.keys()))
    return random.choice(uppercase_states)

def generate_text(markov_chain, words):
    state = get_random_state(markov_chain)
    text = state.split()[:words]
    while len(text) < words:
        state = get_next_state(markov_chain, state)
        if state is None:
            state = get_random_state(markov_chain)
        text.append(state.split()[-1])
    return ' '.join(text)


@api.route('/bookmark/allurls')
class Url(Resource):
    def get(self):
        x=[]
        for url in chrome_bookmarks.urls:
            print(url)
            x.append(url)
        return (x) , 201


@api.route('/bookmark/summary')
class Url(Resource):
    def get(self):
        x = []
        for url in chrome_bookmarks.urls:
            content = (url['url'])
            req = Request(content, headers={'User-agent': 'Chrome/83.0.4103.61'})
            html = urlopen(req).read()
            soup = BeautifulSoup(html,"html.parser" )
            for script in soup(["script", "style"]):
                script.extract()    
            text = soup.get_text()
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            filename = text
            words = 100
            tokens = tokenise_text_file(filename)
            markov_chain = create_markov_chain(tokens, order=1)
            return(generate_text(markov_chain, words))

if __name__ == "__main__":
    app.run(port=8080, debug=True)


# sample
# {'date_added': '13214900973129805', 'guid': 'a85efbb6-c679-4def-b4f5-937236e83141', 'id': '7', 'name': 'Google AI Blog', 'type': 'url', 'url': 'https://ai.googleblog.com/'}



    

