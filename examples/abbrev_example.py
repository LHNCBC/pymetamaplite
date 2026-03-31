"""This example requires Phil Gooch's Python3 implementation of the
Schwartz-Hearst algorithm for identifying abbreviations and their
corresponding definitions in free
text[1]. (https://github.com/philgooch/abbreviation-extraction)"""

import argparse
from collections import namedtuple
import os
import sys
from nltk import sent_tokenize, pos_tag
from nltk.tokenize import TreebankWordTokenizer
from abbreviations import schwartz_hearst
from metamaplite import MetaMapLite, Token


case_sensitive = False
use_sources = []
use_semtypes = []
# The token's part-of-speech must be in postags set to be looked up in
# dictionary.
postags = set(["CD", "FW", "RB", "IN", "NN", "NNS",
               "NNP", "NNPS", "JJ", "JJR", "JJS", "LS"])
stopwords = []
excludedterms = []


def process(ivfdir, inputtext, uda_dict={}):
    """ process inputtext returning list of matches """
    mminst = MetaMapLite(ivfdir, use_sources, use_semtypes, postags,
                         stopwords, excludedterms, uda_dict=uda_dict)
    print('input text: "%s"' % inputtext)

    # break text into sentences before tagging
    sentlist = sent_tokenize(inputtext)
    sent_resultlist = []
    sent_start = 0
    for sentence in sentlist:
        spanlist = list(TreebankWordTokenizer().span_tokenize(sentence))
        texttokenlist = [sentence[start:end] for start, end in spanlist]
        postokenlist = pos_tag(texttokenlist)
        tokenlist = []
        for idx, (token, span) in enumerate(zip(postokenlist, spanlist)):
            tokenlist.append(Token(text=token[0], tag_=token[1],
                                   idx=idx, start=(sent_start+span[0])))
        matches = mminst.get_entities(tokenlist, span_info=True)
        sent_resultlist.append((sentence, matches))
        sent_start = sent_start + len(sentence) + 1
    return sent_resultlist


def listcuis(postings):
    return ','.join(set([post.split('|')[0] for post in postings]))


def display_results(sent_resultlist):
    """ display list of matches """
    for sentence, matches in sent_resultlist:
        print('sentence: "%s"' % sentence.replace('\n', ' '))
        for term in matches:
            print('  "%s" (%d, %d): %s' % (term.text, term.start, term.end,
                                           listcuis(term.postings)))


def loadtextfile(inputfile):
    """ Load textfile and return as string """
    text = ''
    with open(inputfile) as fp:
        text = fp.read()
    return text


if __name__ == '__main__':
    if 'MML_INDEXDIR' in os.environ:
        indexdir = os.environ['MML_INDEXDIR']
        print(indexdir)
    else:
        indexdir = None

    parser = argparse.ArgumentParser(
        description="metamaplite abbreviation example")
    parser.add_argument('inputfile',
                        help='file containing input text to process.')
    parser.add_argument('--indexdir',
                        help='inverted file index directory.')
    args = parser.parse_args()
    if args.indexdir:
        indexdir = args.indexdir
    if indexdir is not None:
        inputtext = loadtextfile(args.inputfile)
        pairs = schwartz_hearst.extract_abbreviation_definition_pairs(
            doc_text=inputtext)
        sent_resultlist = process(indexdir, inputtext, uda_dict=pairs)
        print('found abbreviations: {}'.format(pairs))
        display_results(sent_resultlist)
    else:
        print("""index directory not specified, use --indexdir <mml
        index directory path> or set MML_INDEXDIR environment variable
        to path of mml index directory.""")
        sys.exit(1)
