""" An example of using pymetamap library.

    Set environment variable MML_INDEXDIR to location of MetaMapLite index:
    In bash:

       export MML_INDEXDIR=<mml-indexdir>

"""
import os
import nltk
from metamaplite import MetaMapLite, Token

if 'MML_INDEXDIR' in os.environ:
    ivfdir = os.environ['MML_INDEXDIR']
else:
    ivfdir = 'pathto/public_mm_lite/data/ivf/2025AB/USAbase'

label = ''
case_sensitive = False
use_sources = []
use_semtypes = []
postags = set(["CD", "FW", "RB", "IN", "NN", "NNS",
               "NNP", "NNPS", "JJ", "JJR", "JJS", "LS"])
stopwords = []
excludedterms = []
mminst = MetaMapLite(ivfdir, use_sources, use_semtypes, postags,
                     stopwords, excludedterms)

inputtext = 'inferior vena cava stent filter'
print('input text: "%s"' % inputtext)
texttokenlist = inputtext.split(' ')
postokenlist = nltk.pos_tag(texttokenlist)
tokenlist = []
start = 0
idx = 0
for token in postokenlist:
    tokenlist.append(Token(text=token[0], tag_=token[1], idx=idx, start=start))
    start = start + len(token[0]) + 1
    idx += 1
matches = mminst.get_entities(tokenlist, span_info=True)
for term in matches:
    print('%s' % term.text)
    print(' start: %d' % term.start)
    print(' end: %d' % term.end)
    print(' postings:')
    for post in term.postings:
        print('   %s' % post)
