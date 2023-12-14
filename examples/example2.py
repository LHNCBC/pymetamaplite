import argparse
from collections import namedtuple
from nltk import sent_tokenize, pos_tag
from nltk.tokenize import TreebankWordTokenizer
from metamaplite import MetaMapLite

ivfdir = 'pathto/public_mm_lite/data/ivf/2020AA/USAbase'

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


def process(ivfdir, inputtext):
    """ process inputtext returning list of matches """
    mminst = MetaMapLite(ivfdir, use_sources, use_semtypes, postags,
                         stopwords, excludedterms)
    # Named tuple Token contains token text in text, part of speech tag
    # in tag_, and charater offset is in idx.
    Token = namedtuple('Token', ['text', 'tag_', 'idx'])
    print('input text: "%s"' % inputtext)

    # break text into sentences before tagging
    sentlist = sent_tokenize(inputtext)
    sent_resultlist = []
    sentidx = 0
    for sentence in sentlist:
        spanlist = list(TreebankWordTokenizer().span_tokenize(sentence))
        texttokenlist = [sentence[start:end] for start, end in spanlist]
        postokenlist = pos_tag(texttokenlist)
        tokenlist = []
        for token, span in zip(postokenlist, spanlist):
            tokenlist.append(Token(text=token[0], tag_=token[1],
                                   idx=(sentidx+span[0])))
        matches = mminst.get_entities(tokenlist, span_info=True)
        sent_resultlist.append((sentence, matches))
        sentidx = sentidx + len(sentence) + 1
    return sent_resultlist


def display_results(sent_resultlist):
    """ display list of matches """
    for sentence, matches in sent_resultlist:
        print('sentence: "%s"' % sentence)
        for term in matches:
            print('  "%s"' % term.text)
            print('    start: %d' % term.start)
            print('    end: %d' % term.end)
            print('    postings:')
            for post in term.postings:
                print('      {}'.format(post))


def loadtextfile(inputfile):
    """ Load textfile and return as string """
    text = ''
    with open(inputfile) as fp:
        text = fp.read()
    return text


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="test metamaplite")
    parser.add_argument('inputfile',
                        help='file containing input text to process.')
    parser.add_argument('--ivfdir',
                        help='inverted file index directory.',
                        default=ivfdir)
    args = parser.parse_args()
    inputtext = loadtextfile(args.inputfile)
    sent_resultlist = process(args.ivfdir, inputtext)
    display_results(sent_resultlist)
