"""Generate variants table used by MetaMapLite (and MetaMap) when
using MMI format.

LVG is necessary to run this.  After installing LVG set the
environment variable LVG_DIR to location of your LVF installation
directory.

Environment variable LVG_DIR must be defined:
In bash shell:
    export LVG_DIR=<location of lvg installation>

This requires Python 3.12 or greater. due to the use of
itertools.batched.

"""
import argparse
from collections import namedtuple
from itertools import batched, groupby
import os
from subprocess import Popen, PIPE
from metamaplite.index import glean_mrconso
from tqdm import tqdm


LexItem = namedtuple('LexItem',
                     ['originalterm', 'targetterm', 'category', 'inflection',
                      'flowhistory', 'flownumber', 'sourcecategory',
                      'targetcategory',
                      'mutateinformation', 'distance_score', 'tag_information'])


def parse_fruitful_lex_item(line):
    """ parse lex item from LVG fruitful variants list """
    if len(line) >= 12:
        fields = line.split('|')
        # (originalterm, targetterm, category, inflection,
        #   flow_history, flow_number,sourcecategory, targetcategory,
        #  mutateinformation, distance_score, tag_information, extra) = fields
        return LexItem._make(fields[:11])
    else:
        return None


def get_word(line):
    "Get word component of word line."
    fields = line.split('|')
    if len(fields) > 2:
        return fields[2]
    else:
        return fields[0]


category_dict = {
    '1': 'adj',
    '2': 'adv',
    '4': 'aux',
    '8': 'compl',
    '16': 'conj',
    '32': 'det',
    '64': 'modal',
    '128': 'noun',
    '256': 'prep',
    '512': 'pron',
    '1024': 'verb',
    'n': 'all'
}


def get_category_name(category):
    return category_dict[category]


def generate_variant_list_for_term(word):
    """ List variants for term """
    p1 = Popen(["echo", word], stdout=PIPE)
    p2 = Popen(["lvg", "-f:G", "-m"], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]
    return output.decode('utf-8')


def get_original_term(lex_item):
    return lex_item.originalterm


def group_variantslist(variantlist):
    """ group variants list by original term """
    return [list(group) for key, group in groupby(
        [parse_fruitful_lex_item(x)
         for x in variantlist
         if parse_fruitful_lex_item(x) is not None], get_original_term)]


def generate_variants_list_for_termlist(wordlist):
    p1 = Popen(["echo", '\n'.join(wordlist)], stdout=PIPE)
    p2 = Popen(["lvg", "-f:G", "-m"], stdin=p1.stdout, stdout=PIPE)
    p1.stdout.close()
    output = p2.communicate()[0]
    return group_variantslist(output.decode('utf-8').split('\n'))


def transform_mutate_information(lex_item):
    """ Transform mutate information string:

      128|1|n+dd+y|8|2| yields 8|n+dd+y|2|128|1
     """
    return "{}|{}|{}|{}|{}".format(
        lex_item.distance_score,
        lex_item.mutateinformation,
        lex_item.tag_information,
        lex_item.sourcecategory,
        lex_item.targetcategory)


def generate_piped_representation(item):
    """Generate piped representation of variant information for lexical
     item."""
    return "{}|{}|{}|{}|{}|{}".format(
        item.originalterm,
        get_category_name(item.sourcecategory),
        item.targetterm,
        get_category_name(item.targetcategory),
        transform_mutate_information(item),
        item.flowhistory)


def load_word_set(wordsfilename):
    with open(wordsfilename) as chan:
        return set([get_word(line.strip()) for line in chan.readlines()])


def generate_variantlist(wordset, batchsize=500):
    variantlist = []
    wordgrouplist = list(batched(list(wordset), batchsize))
    for wordgroup in tqdm(wordgrouplist, desc="word groups"):
        for variantgroup in generate_variants_list_for_termlist(wordgroup):
            for lex_item in variantgroup:
                if lex_item is not None:
                    variantlist.append(generate_piped_representation(lex_item))
    variantlist.sort()
    return variantlist


def write_variantlist(varsfilename, variantlist):
    with open(varsfilename, 'w') as chan:
        for variant in tqdm(variantlist, desc="write variantlist"):
            chan.write('{}\n'.format(variant))


def process_words(wordsfilename, varsfilename):
    wordset = load_word_set(wordsfilename)
    variantlist = generate_variantlist(wordset)
    write_variantlist(varsfilename, variantlist)


def create_table(mrconsofilename, varsfilename, batchsize=500):
    lvgdirname = os.environ['LVG_DIR']
    os.environ['PATH'] = '{}:{}/bin'.format(os.environ['PATH'], lvgdirname)
    # if 'GV_WORD_TEMP_FILENAME' in os.environ:
    #     wordsfilename = os.environ['GV_WORD_TEMP_FILENAME']
    # else:
    #     wordsfilename = '/tmp/words.txt.tmp'
    # glean_mrconso.process(mrconsofilename, wordsfilename)
    # process_words(wordsfilename, varsfilename)
    wordset = glean_mrconso.generate_wordset(mrconsofilename)
    variantlist = generate_variantlist(wordset, batchsize=batchsize)
    write_variantlist(varsfilename, variantlist)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='GenerateVariants',
        description='generate variants table from MRCONSO')
    parser.add_argument('-b', '--batchsize', default=500,
                        help='set batchsize of wordlists sent to LVG.')
    parser.add_argument('mrconsofilename')
    parser.add_argument('varsfilename')
    args = parser.parse_args()
    if 'LVG_DIR' in os.environ:
        create_table(args.mrconsofilename, args.varsfilename,
                     batchsize=args.batchsize)
    else:
        print('Environment variable LVG_DIR is not defined:\n')
        print('In bash shell:')
        print("   export LVG_DIR=<location of lvg installation>\n")
        print("In C shell:")
        print("   setenv LVG_DIR <location of lvg installation>\n")
        print("Also, the variable LVG_DIR in the file")
        print("<lvg installation location>/lvg.properties must have full")
        print("path of LVG installation; LVG_DIR=AUTO_MODE will not work.")
