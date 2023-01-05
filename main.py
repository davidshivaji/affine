import argparse
import sys
import datamuse
api = datamuse.Datamuse()
import os

def grouplen(sequence, chunk_size):
    return list(zip(*[iter(sequence)] * chunk_size))


def some_function(entry):
    arch = dict()
    for result in api.words(ml=entry, max=51):
        arch[result['word']] = {'score': result['score'], 'color': None}

    starch = dict()

    for key, value in arch.items():
        if len(key) > 20:
            starch[key[:16] + '...'] = arch[key]
        else:
            starch[key] = arch[key]

    for key, value in starch.items():
        if value['score'] > 60000:
            value['color'] = u"\u001b[38;5;" + "202" + "m"
        elif 50000 > value['score'] > 40000:
            value['color'] = u"\u001b[38;5;" + "208" + "m"
        elif 40000 > value['score']:
            value['color'] = u"\u001b[38;5;" + "214" + "m"
        else:
            value['color'] = u"\u001b[38;5;" + "130" + "m"

    max_word_length = max(len(word) for word in starch)

    col_width = max_word_length + 1

    num_rows = (len(starch) + 2) // 3

    terminal_width = os.get_terminal_size().columns
    col_width = terminal_width // 3

    for row in range(num_rows):
        for col in range(3):
            index = row + col * num_rows
            if index < len(starch):
                word, data = list(starch.items())[index]
                sys.stdout.write(data['color'] + word.ljust(col_width))
        print('')
    print(u"\u001b[0m")



def start():
    parser = argparse.ArgumentParser(description='Enter word.')
    parser.add_argument('entry', type=str, help='the name of the entry')

    args = parser.parse_args()
    some_function(args.entry)
