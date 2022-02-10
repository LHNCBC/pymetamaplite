# Description

# Prerequisites

# Installation

Installation using pip

    cd pymetamaplite
    pip install .

Installation using setuptools

    cd pymetamaplite
    python setup.py install

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

    # Convert tokens and part of speech tags into named tuples with
    # the following defintion:
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

	# pass tokenlist to get_entities to find entities in the input
    # text.
	matches = mminst.get_entities(tokenlist, span_info=True)
    for term in matches:
        print('{}'.format(term.text))
        print(' start: {}'.format(term.start))
        print(' end: {}'.format(term.end))
        print(' postings:')
        for post in term.postings:
            print('   {}'.format(post))

output:

    length of list of tokensublists: 15
    length of list of term_info_list: 7
    inferior vena cava
     start: 0
     end: 18
     postings:
       C0042458|S0002351|4|Inferior vena cava|RCD|PT
       C0042458|S0002351|5|Inferior vena cava|SNM|PT
       C0042458|S0002351|6|Inferior vena cava|SNMI|PT
       C0042458|S0002351|7|Inferior vena cava|UWDA|PT
       C0042458|S0002351|8|Inferior vena cava|FMA|PT
       C0042458|S0002351|9|Inferior vena cava|SNOMEDCT_US|SY
       C0042458|S0906979|10|INFERIOR VENA CAVA|NCI_CDISC|PT
       C0042458|S6146821|13|inferior vena cava|NCI_NCI-GLOSS|PT
       C0042458|S0380063|24|Inferior Vena Cava|NCI_caDSR|SY
       C0042458|S0380063|25|Inferior Vena Cava|NCI|PT
       C0042458|S0380063|26|Inferior Vena Cava|MSH|ET
       C1269024|S0002351|3|Inferior vena cava|SNOMEDCT_US|IS


Use the function __result_utils.add_semantic_types__ to add semantic
types and convert postings to records:

    from metamaplite import result_utils

	matches0 = mminst.get_entities(tokenlist, span_info=True)
	matches = result_utils.add_semantic_types(mminst, matches0)
    for term in matches:
        print('{}'.format(term.text))
        print(' start: {}'.format(term.start))
        print(' end: {}'.format(term.end))
        print(' postings:')
        for post in term.postings:
            print('   {}'.format(post))

output:

	inferior vena cava
	 start: 0
	 end: 18
	 postings:
	   PostingSTS(cui='C0042458', sui='S0002351', idx='4', str='Inferior vena cava', src='SNM', termtype='PT', semtypeset=['bpoc'])
	   PostingSTS(cui='C0042458', sui='S0002351', idx='5', str='Inferior vena cava', src='SNMI', termtype='PT', semtypeset=['bpoc'])
	   PostingSTS(cui='C0042458', sui='S0002351', idx='6', str='Inferior vena cava', src='UWDA', termtype='PT', semtypeset=['bpoc'])
	   PostingSTS(cui='C0042458', sui='S0002351', idx='7', str='Inferior vena cava', src='FMA', termtype='PT', semtypeset=['bpoc'])
	   PostingSTS(cui='C0042458', sui='S0002351', idx='8', str='Inferior vena cava', src='SNOMEDCT_US', termtype='SY', semtypeset=['bpoc'])
	   PostingSTS(cui='C0042458', sui='S0906979', idx='9', str='INFERIOR VENA CAVA', src='NCI_CDISC', termtype='PT', semtypeset=['bpoc'])
	   PostingSTS(cui='C0042458', sui='S6146821', idx='11', str='inferior vena cava', src='CHV', termtype='PT', semtypeset=['bpoc'])
	   PostingSTS(cui='C0042458', sui='S6146821', idx='12', str='inferior vena cava', src='NCI_NCI-GLOSS', termtype='PT', semtypeset=['bpoc'])
	   PostingSTS(cui='C0042458', sui='S0380063', idx='23', str='Inferior Vena Cava', src='NCI', termtype='SY', semtypeset=['bpoc'])
	   PostingSTS(cui='C0042458', sui='S0380063', idx='24', str='Inferior Vena Cava', src='NCI', termtype='PT', semtypeset=['bpoc'])
	   PostingSTS(cui='C0042458', sui='S0380063', idx='25', str='Inferior Vena Cava', src='MSH', termtype='ET', semtypeset=['bpoc'])
	   PostingSTS(cui='C1269024', sui='S0002351', idx='3', str='Inferior vena cava', src='SNOMEDCT_US', termtype='IS', semtypeset=['bpoc'])

* Cython

# Speeding up pyMetaMapLite: Using Cython

Certain computationally expensive sections of pyMetaMapLite can be sped up
using Cython (https://cython.org).  Cython is an optimizing static
compiler for both the Python programming language.

If you are using Microsoft Windows 10 you must have
"Microsoft Visual C++ Build Tools"
(https://visualstudio.microsoft.com/visual-cpp-build-tools/) to
compile the c files generated by Cython.  On Unix-like systems like
Linux or MacOS either GCC or Clang (LLVM) must be installed.

Modify setup.py to the following:

    # -*- coding: utf-8 -*-

    from setuptools import setup, find_packages
    from Cython.Build import cythonize

    setup(name='pymetamaplite',
          version='0.2',
          description='MetaMapLite Entity Recognizer implementation',
          author='Willie Rogers',
          author_email='wjrogers@mail.nih.gov',
          url="https://metamap.nlm.nih.gov/",
          license="Public Domain",
          packages=find_packages(),
          classifiers=[
              "Programming Language :: Python :: 3",
              "Operating System :: OS Independent",
          ],
          python_requires='>=3.6',
          ext_modules=cythonize("*/*.py"))

Then re-install pymetamaplite:

	$ pip install cython
    $ pip install .

