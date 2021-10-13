import sys
import datamuse
api = datamuse.Datamuse()
import os

################################################################################

# WHAT DO YOU DO WHEN THE DATAMUSE API FUCKS UP?
# switch to oxford, pythesaurus, collegiate (+ antonyms),

################################################################################

entry = sys.argv[1]
# entry = "search"
tip = ''

if len(sys.argv) > 2:
    tip = sys.argv[2]
    if tip.lower() == 'noun':
        tip = 'n'
    if tip.lower() == 'verb':
        tip = 'v'
    if tip.lower() == 'adjective' or tip.lower() == 'a':
        tip = 'adj'

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    DIM = '\033[2;32m'
    # 92
    OKGREEN = '\033[32m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def grouplen(sequence, chunk_size):
    # i want to pivot this, so that it goes down first instead of across.
    return list(zip(*[iter(sequence)] * chunk_size))

orange = u"\u001b[38;5;214m "

reslist = []
arch = {}

if tip != '':
    # filter for only specd.
    for result in api.words(ml=entry, max=51):
        # print(result)
    # for result in testresults:
        if 'tags' in result:
            if tip in result['tags']:
                arch[result['word']] = {'score': result['score'], 'color': None}
            # if result['score'] > 50000:
                # reslist.append(result['word'])
else:
    for result in api.words(ml=entry, max=51):
        arch[result['word']] = {'score': result['score'], 'color': None}

starch = dict()

for key, value in arch.items():
    if len(key) > 20:
        starch[key[:16] + '...'] = arch[key]
    else:
        starch[key] = arch[key]

results = grouplen(starch.items(), 3)


valuecolor = bcolors.OKGREEN

for key, value in starch.items():
    if value['score'] > 60000:
        value['color'] = u"\u001b[38;5;" + "202" + "m"
    elif 50000 > value['score'] > 40000:
        value['color'] = u"\u001b[38;5;" + "208" + "m"
    elif 40000 > value['score']:
        value['color'] = u"\u001b[38;5;" + "214" + "m"
    else:
        value['color'] = u"\u001b[38;5;" + "130" + "m"

################################################################################
# print(os.get_terminal_size()) # >> returns a tuple.
# you can mofify the ljust parameter to display things nicely
# across any system.

cols = os.get_terminal_size().columns

################################################################################


for trip in results:
    for word in trip:
        sys.stdout.write(word[1]['color'] + word[0].ljust(int(cols/3)) + u"\u001b[0m")

print(u"\u001b[0m")
