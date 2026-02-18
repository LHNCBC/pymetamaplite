""" A bridge to access python metamaplite implementation """

import os.path
import logging
from collections import namedtuple
from metamaplite.dictionary.irindex import IRIndex
from metamaplite.find_longest_match import find_longest_match
from metamaplite.subsume import remove_subsumed_entities, resolve_overlaps
from metamaplite.filtering import restrict_postings_to_sources
from metamaplite.filtering import restrict_postings_to_semantic_types
from metamaplite.simple_cache import SimpleCache
from metamaplite.uda_lookup import UDALookup

Term = namedtuple('Term', ['text', 'start', 'end', 'postings'])


def remove_excluded_terms(matchlist, excludedterms):
    newmatchlist = []
    for match in matchlist:
        newpostings = []
        # Discard any postings for term with concept that are in
        # excludedterms list.
        for posting in match.postings:
            fields = posting.split('|')
            conceptterm = '{}:{}'.format(fields[0], match.text.lower())
            if conceptterm not in excludedterms:
                newpostings.append(posting)
        if newpostings != []:
            newmatchlist.append(Term(text=match.text,
                                     start=match.start,
                                     end=match.end,
                                     postings=newpostings))
    return newmatchlist


class MetaMapLite():

    def __init__(self, ivfdir, sources=[], semtypes=[],
                 postags=set(['CD', 'FW', 'RB', 'IN', 'NN', 'NNS',
                              'NNP', 'NNPS', 'JJ', 'JJR', 'JJS', 'LS']),
                 stopwords=[],
                 excludedterms=[],
                 minimum_length=3,
                 use_cache=False,
                 uda_dict={}):
        """ Initialize MetaMapLite instance

        PARAMS:
          ivdir: root of inverted file directory
          sources: list of vocabulary sources
          semtypes: list of semantic type
          postags: set of penn treebank part of speech tags
          stopwords: set of stopwords
          excludedterms: set of id|term (cui|term)
          minimum_length:  minimum length of terms
        """
        self.indexname = 'cuisourceinfo'
        if not os.path.exists(ivfdir):
            logging.error('index directory %s does not exist. ', ivfdir)
            exit()
        self.index = IRIndex(ivfdir, self.indexname)
        self.sources = sources
        self.semtypes = semtypes
        self.minimum_length = minimum_length
        self.postags = postags
        self.semtypeindexname = 'cuist'
        self.semtypeindex = IRIndex(ivfdir, self.semtypeindexname)
        self.cuiconceptindexname = 'cuiconcept'
        self.cuiconceptindex = IRIndex(ivfdir, self.cuiconceptindexname)
        self.treecodeindexname = 'meshtcrelaxed'
        self.treecodeindex = IRIndex(ivfdir, self.treecodeindexname)
        if type(stopwords) is set:
            self.stopwords = stopwords
        else:
            self.stopwords = set(stopwords)
        if type(excludedterms) is set:
            self.excludedterms = excludedterms
        else:
            self.excludedterms = set(excludedterms)
        # user defined acronyms/abbreviations
        if uda_dict != {}:
            self.index = UDALookup(self.index, uda_dict)
        # lookup index caches
        if use_cache:
            self.use_cache = use_cache
            self.index = SimpleCache(self.index)
            self.semtypeindex = SimpleCache(self.semtypeindex)
            self.cuiconceptindex = SimpleCache(self.cuiconceptindex)
            self.treecodeindex = SimpleCache(self.treecodeindex)

    def set_semtypes(self, semtypelist):
        """ set restrict to semantic type list """
        self.semtypes = semtypelist

    def set_sources(self, sourcelist):
        """ set restrict to source list """
        self.sources = sourcelist

    def lookup(self, tokensublist, column=3):
        """Extract text part of tokens, join and call index lookup
           function."""
        term = " ".join([token.text for token in tokensublist]).lower()
        if len(term) >= self.minimum_length and (term not in self.stopwords):
            logging.debug('metamaplite:lookup():term: %s' % term)
            return self.index.lookup(term, column)
        else:
            return None

    def token_filter_func(self, tokenlist):
        """Return true if first token in tokenlist is in postags list and is
           not the word 'other'"""
        return (tokenlist[0].text.lower() != 'other') & \
            (tokenlist[0].tag_ in self.postags)

    def get_entities(self, tokenlist, span_info=True, aa_dict={}):
        """Given tokenlist, return list of Term instances matching entities
           in dictionary."""
        # logging.debug('get_entities')
        matches = []
        if aa_dict != {}:
            def newlookup(tokensublist):
                if len(tokensublist) == 1:
                    term = tokensublist[0]
                    return self.lookup(aa_dict[term].split(' ')
                                       if term in aa_dict else [term])
                else:
                    return self.lookup(tokensublist)
            lookup = newlookup
        else:
            lookup = self.lookup

        resultlist = find_longest_match(tokenlist, lookup,
                                        self.token_filter_func)
        # logging.debug('get_entities: resultlist: %s' % resultlist)
        for tokensublist, postings in resultlist:
            # logging.debug('get_entities: tokensublist: %s' % tokensublist)
            matchstring = ' '.join([token.text for token in tokensublist])
            # logging.debug('get_entities: %s, %d, %d' %
            #               (matchstring,
            #                tokensublist[0].idx,
            #                tokensublist[0].idx + len(matchstring)))
            matches.append(Term(text=matchstring,
                                start=tokensublist[0].idx,
                                end=tokensublist[0].idx + len(matchstring),
                                postings=postings))
        newmatches0 = remove_excluded_terms(matches, self.excludedterms)
        if self.sources:
            for match in matches:
                if restrict_postings_to_sources(match.postings, self.sources):
                    newmatches0.append(match)
        else:
            newmatches0 = matches

        newmatches = []
        if self.semtypes:
            for match in newmatches0:
                logging.debug(match)
                if restrict_postings_to_semantic_types(match.postings,
                                                       self.semtypes,
                                                       self.has_semantic_type):
                    newmatches.append(match)
        else:
            newmatches = newmatches0
        entities0 = remove_subsumed_entities(newmatches)
        return resolve_overlaps(entities0)

    def get_semantic_types(self, cui):
        """ get semantic types for concept """
        semtypes = [
            post.split('|')[1] for post in self.semtypeindex.lookup(cui, 0)
            ]
        logging.debug('get_semantic_types: %s:%s' % (cui, semtypes))
        return semtypes

    def has_semantic_type(self, cui, semtypelist):
        """ Does cui have semantic type in semantic type set. """
        logging.debug('has_semantic_types: %s' % cui)
        cuisemtypeset = set(self.get_semantic_types(cui))
        if type(semtypelist) is set:
            semtypeset = semtypelist
        else:
            semtypeset = set(semtypelist)
        logging.debug('has_semantic_types: %s intersection %s -> %s' % (
            semtypeset,
            cuisemtypeset,
            semtypeset.intersection(cuisemtypeset)))
        return semtypeset.intersection(cuisemtypeset) != set()

    def get_sources(self, postingslist_or_cui):
        """ Return sources from postings list or cui. Source
        identifier is in 4th column of postings record. """
        if type(postingslist_or_cui) is str:
            cui = postingslist_or_cui
            return set([post.split('|')[4] for post in self.index.lookup(
                cui, 0)])
        if type(postingslist_or_cui) is list:
            postingslist = postingslist_or_cui
            logging.info('get_sources: %s' % (
                [posting.split('|')[4] for posting in postingslist]))
            return set([posting.split('|')[4] for posting in postingslist])
        return []

    def get_cuis(self, postingslist):
        """Return concept unique identifiers (CUIs) from postings list.
        Concept unique identifier is in zeroth column of postings
        record. """
        return [posting.split('|')[0] for posting in postingslist]

    def get_preferredname(self, cui):
        """get preferred name string for cui """
        records = self.cuiconceptindex.lookup(cui, 0)
        return records[0].split('|')[1]

    def get_treecodes(self, term):
        """ get MeSH treecodes for term if present. """
        return self.treecodeindex.lookup(term, 0)

    def get_cuiinfo(self, cui):
        """get preferredname, semantictypelist, vocabulary sourcelist, and
           treecodes (if present) for cui. """
        cuiinfo = {}
        prefname = self.get_preferredname(cui)
        cuiinfo = {'prefname': prefname,
                   'semantictypes': self.get_semantic_types(cui),
                   'sources': self.get_sources(cui)}
        treecodelist = self.get_treecodes(prefname)
        if treecodelist != []:
            cuiinfo['treecodes'] = treecodelist
        return cuiinfo
