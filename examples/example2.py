import argparse
from collections import namedtuple
import nltk
from nltk.tokenize import TreebankWordTokenizer
from metamaplite import MetaMapLite

ivfdir = '/path/to/public_mm_lite/data/ivf/2020AA/USAbase'
gwa = '/net/lhcdevfiler/vol/cgsb5/ind/II_Group_WorkArea'
pathto = gwa + '/wjrogers/Projects/public_mm_dist/test/metamaplite/3.6.2rc6'
ivfdir = pathto + '/public_mm_lite/data/ivf/2020AA/USAbase'

label = ''
case_sensitive = False
use_sources = []
use_semtypes = []
# The token's part-of-speech must be in postags set to be looked up in
# dictionary.
postags = set(["CD", "FW", "RB", "IN", "NN", "NNS",
               "NNP", "NNPS", "JJ", "JJR", "JJS", "LS"])
stopwords = []
excludedterms = []


def process(inputtext):
    """ process inputtext returning list of matches """
    mminst = MetaMapLite(ivfdir, use_sources, use_semtypes, postags,
                         stopwords, excludedterms)
    # Named tuple Token contains token text in text, part of speech tag
    # in tag_, and charater offset is in idx.
    Token = namedtuple('Token', ['text', 'tag_', 'idx'])
    print('input text: "%s"' % inputtext)

    # break text into sentences before tagging
    sentlist = nltk.sent_tokenize(inputtext)
    sent_resultlist = []
    sentidx = 0
    for sentence in sentlist:
        spanlist = list(TreebankWordTokenizer().span_tokenize(sentence))
        texttokenlist = [sentence[start:end] for start, end in spanlist]
        postokenlist = nltk.pos_tag(texttokenlist)
        tokenlist = []
        for token, span in zip(postokenlist, spanlist):
            tokenlist.append(Token(text=token[0], tag_=token[1],
                                   idx=(sentidx+span[0])))
        matches = mminst.get_entities(tokenlist, span_info=True)
        sent_resultlist.append((sentence, matches))
        sentidx = sentidx + len(sentence) + 1
    return sent_resultlist


def display_results(sent_resultlist):
    """ process inputtext returning list of matches """
    for sentence, matches in sent_resultlist:
        print('sentence: "%s"' % sentence)
        for term in matches:
            print('  "%s"' % term.text)
            print('    start: %d' % term.start)
            print('    end: %d' % term.end)
            print('    postings:')
            for post in term.postings:
                print('      %s' % post)


def loadtextfile(inputfile):
    """ Load textfile and return as string """
    text = ''
    with open(inputfile) as fp:
        text = fp.read()
    return text

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="test spacy with metamaplite")
    parser.add_argument('inputfile',
                        help='file containing input text to process.')
    args = parser.parse_args()
    inputtext = loadtextfile(args.inputfile)
    sent_resultlist = process(inputtext)
    display_results(sent_resultlist)
