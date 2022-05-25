import unittest
from collections import namedtuple
from metamaplite.find_longest_match import find_longest_match


def render_text(alist):
    return [x.text for x in alist]


def render_listitems(list_of_lists):
    return ['seq: %s' % render_text(x) for x in list_of_lists]


def render_list_of_lists(list_of_lists):
    return '\n'.join(render_listitems(list_of_lists))

Token = namedtuple('Token', ['text', 'tag_', 'idx', 'start'])


class FLMTestCase(unittest.TestCase):

    def setUp(self):
        self.tokenlist0 = [
            Token(text='Papillary', tag_='NNP', idx=0, start=0),
            Token(text='Thyroid', tag_='NNP', idx=1, start=10),
            Token(text='Carcinoma', tag_='NNP', idx=2, start=18),
            Token(text='is', tag_='VBZ', idx=3, start=28),
            Token(text='a', tag_='DT', idx=4, start=31),
            Token(text='Unique', tag_='NNP', idx=5, start=33),
            Token(text='Clinical', tag_='NNP', idx=6, start=40),
            Token(text='Entity', tag_='NNP', idx=7, start=49)]

        self.allowed_part_of_speech_set = set(
            ["RB",              # should this be here?
             "NN",
             "NNS",
             "NNP",
             "NNPS",
             "JJ",
             "JJR",
             "JJS",
             ""])  # empty if not part-of-speech tagged (accept everything)
        self.dictionary = {
            "6-ohda": "C0085196",
            "carcinoma": "C0007097",
            "dimethyl fumarate": "C0058218",
            "disease": "C0012634",
            "entity": "C1551338",
            "papillary thyroid carcinoma": "C0238463",
            "parkinson's disease": "C0030567",
            "thyroid carcinoma": "C0549473",
            "thyroid": "C0040132",
            "unique": "C1710548",
            "animal model": "C0012644",
            "induced": "C0205263",
            "neurotoxicity": "C0235032"}

    def tearDown(self):
        pass

    def pos_filter(self, token):
        """is token in allowed part of speech set"""
        return token.tag_ in self.allowed_part_of_speech_set

    def testA(self):
        term_info_list = find_longest_match(self.tokenlist0, self.pos_filter,
                                            self.dictionary)
        assert(len(term_info_list) == 6)

if __name__ == '__main__':
    unittest.main()             # run all tests
