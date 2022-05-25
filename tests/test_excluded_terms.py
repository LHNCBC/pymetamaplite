import unittest
from metamaplite import remove_excluded_terms
from collections import namedtuple

Term = namedtuple('Term', ['text', 'start', 'end', 'postings'])


class ExcludedTermsTestCase(unittest.TestCase):

    def testA(self):
        matchlist = [
            Term(text='CLAP', start=0, end=4,
                 postings=['C0018081|S0618679|24|Clap|MEDLINEPLUS|ET',
                           'C0018081|S0618679|25|Clap|SNOMEDCT_US|SY',
                           'C0018081|S0144453|26|CLAP|DXP|SY',
                           'C0018081|S1218046|27|clap|CHV|SY',
                           'C1367449|S0144453|5|CLAP|HGNC|SYN',
                           'C1706590|S0144453|4|CLAP|NCI|SY'])]
        expectedmatchlist = [
            Term(text='CLAP', start=0, end=4,
                 postings=['C1367449|S0144453|5|CLAP|HGNC|SYN',
                           'C1706590|S0144453|4|CLAP|NCI|SY'])]
        excluded_terms = [
            'C0004002:got',
            'C0006104:bra',
            'C0011710:doc',
            'C0012931:construct',
            'C0014522:ever',
            'C0015737:national',
            'C0018081:clap',
            'C0023668:lie',
            'C0025344:period',
            'C0025344:periods',
            'C0029144:optical',
            'C0071973:prime']
        newmatchlist = remove_excluded_terms(matchlist, excluded_terms)
        self.assertEqual(newmatchlist[0].postings, expectedmatchlist[0].postings)


if __name__ == '__main__':
    unittest.main()             # run all tests
