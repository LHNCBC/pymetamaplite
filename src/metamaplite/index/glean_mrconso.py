"""  GleanMrconso -
 Implement the words file generation functionality of
 the original Prolog version of glean_mrconso using MRCONSO.RRF
 present in Prolog and Java versions of glean_mrconso.

 The original program, glean_mrconso.pl, also gleaned strings, and
 concepts.  This extra functionality has been ommited (for now).
"""
import argparse
from collections import namedtuple
from nls_strings.metamap_tokenization import tokenize_text_mm


WordInfo = namedtuple('WordInfo', ['cui', 'sui', 'words'])


def mrconso_record_to_word_info(line):
    """ Create words info from line of MRCONSO """
    fields = line.split('|')
    if len(fields) >= 14:
        return WordInfo(cui=fields[0], sui=fields[5],
                        words=tokenize_text_mm(fields[14]))
    return None


def write_words(chan, wordlist, sui, cui):
    """Write word list with associated sui and cui to channel."""
    for index, word in enumerate(wordlist):
        chan.write('{}|{}|{}|{}|{}\n'.format(
            index, len(wordlist), ''.join(word), sui, cui))


def generate_wordset(mrconsofilename):
    """Generate wordset from mrconso, discarding string unique
    identifier (SUI), and concept unique identifier (CUI)."""
    wordset = set([])
    with open(mrconsofilename) as mrconsochan:
        for line in mrconsochan.readlines():
            fields = line.split('|')
            if len(fields) >= 14:
                for word in tokenize_text_mm(fields[14]):
                    wordset.add(word)
    return wordset


def process(mrconsofilename, wordsfilename):
    """ Generate wordfile from mrconso """
    with (open(mrconsofilename) as mrconsochan,
          open(wordsfilename, 'w') as outchan):
        for line in mrconsochan.readlines():
            word_info = mrconso_record_to_word_info(line)
            write_words(outchan, word_info.words, word_info.sui, word_info.cui)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='GleanMrconso',
        description='generate words file from MRCONSO')
    parser.add_argument('mrconsofilename')
    parser.add_argument('wordsfile')
    args = parser.parse_args()
    process(args.mrconsofilename, args.wordsfile)
