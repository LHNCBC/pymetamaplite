# Description

# Prerequisites

# Installation


# Usage

The extension uses inverted indexes previously intended for use by the
Java implementation of MetaMapLite.  The indexes are available at the
MetaMapLite Web Page (https://metamap.nlm.nih.gov/MetaMapLite.html).

Below is an an example of using the MetaMapLite module on the string
'inferior vena cava stent filter' using NLTK to provide part-of-speech
tagging:

	import nltk
	from collections import namedtuple
	from metamaplite import MetaMapLite

	ivfdir = '/path/to/public_mm_lite/data/ivf/2020AA/USAbase'
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
	Token = namedtuple('Token', ['text', 'tag_', 'idx', 'start'])
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

