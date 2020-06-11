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

url = "https://towardsdatascience.com/web-scraping-with-python-a-to-copy-z-277a445d64c7"
# url needs to be reiterated so have to make change here 

req = Request(url, headers={'User-agent': 'Chrome/83.0.4103.61'}) # take users chrome default version
html = urlopen(req).read()
soup = BeautifulSoup(html,"html.parser" )

for script in soup(["script", "style"]):
    script.extract()    

# get text
text = soup.get_text()
# print(text)


# break into lines and remove leading and trailing space on each
lines = (line.strip() for line in text.splitlines())
# break multi-headlines into a line each
chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
# drop blank lines
text = '\n'.join(chunk for chunk in chunks if chunk)

filename = text

# z = filename.split()
# print(z)

# token = list(filename)
# print(token)

# t = token[0].split()
# print(t)

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

if __name__ == '__main__':
    words = 100                                 # change as per the need 
    tokens = tokenise_text_file(filename)
    markov_chain = create_markov_chain(tokens, order=1)     # need to modify order 
    print(generate_text(markov_chain, words))




