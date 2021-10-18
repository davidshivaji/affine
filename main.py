import argparse
import sys
import datamuse
api = datamuse.Datamuse()
import os
import click

def grouplen(sequence, chunk_size):
    return list(zip(*[iter(sequence)] * chunk_size))


def some_function(entry):
    arch = dict()
    for result in api.words(ml=entry, max=51):
        # print(result)
        arch[result['word']] = {'score': result['score'], 'color': None}
        # print(len(arch))

    # print(arch)

    starch = dict()

    for key, value in arch.items():
        if len(key) > 20:
            starch[key[:16] + '...'] = arch[key]
        else:
            # print('shorter')
            # print(key)
            starch[key] = arch[key]

    # print('starch length', len(starch))
    # print(len(starch.items()))
    # print(starch)

    results = grouplen(starch.items(), 3)
    # print(results)

    for key, value in starch.items():
        if value['score'] > 60000:
            value['color'] = u"\u001b[38;5;" + "202" + "m"
        elif 50000 > value['score'] > 40000:
            value['color'] = u"\u001b[38;5;" + "208" + "m"
        elif 40000 > value['score']:
            value['color'] = u"\u001b[38;5;" + "214" + "m"
        else:
            value['color'] = u"\u001b[38;5;" + "130" + "m"

    cols = os.get_terminal_size().columns


    for trip in results:
        for word in trip:
            sys.stdout.write(word[1]['color'] + word[0].ljust(int(cols/3)) + u"\u001b[0m")

    print(u"\u001b[0m")
    # print(msg)


def start():
    # All the logic of argparse goes in this function
    # it's just basically telling it to expect these.
    parser = argparse.ArgumentParser(description='Enter word.')
    parser.add_argument('entry', type=str, help='the name of the entry')
    # parser.add_argument('--end', dest='end', default="!",
    #                 help='sum the integers (default: find the max)')

    # parser.parse_args() will pass arguments along to
    # any function that calls it.
    args = parser.parse_args()
    some_function(args.entry)
