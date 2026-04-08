"""
  MetaWordIndex Utilities.

  Currently only contains an Python implementation of the Prolog
  predicate normalize_meta_string/2.

  Translated from Alan Aronson's original prolog version: mwi_utilities.pl.

  Created: Fri Dec 11 10:10:23 2008

  @author <a href="mailto:wrogers@nlm.nih.gov">Willie Rogers</a>
  @version $Id: MWIUtilities.java,v 1.2 2005/03/04 16:11:12 wrogers Exp $
"""

import sys
import nls_strings
from nls_strings.metamap_tokenization import strip_possessives


def normalize_meta_string(metastring):
    """
    Normalize metathesaurus string.

    normalizeMetaString(String) performs "normalization" on String to produce
    NormalizedMetaString.  The purpose of normalization is to detect strings
    which are effectively the same.  The normalization process (also called
    lexical filtering) consists of the following steps:

       * removal of (left []) parentheticals;
       * removal of multiple meaning designators (<n>);
       * NOS normalization;
       * syntactic uninversion;
       * conversion to lowercase;
       * replacement of hyphens with spaces; and
       * stripping of possessives.

    Some right parentheticals used to be stripped, but no longer are.
    Lexical Filtering Examples:
    The concept "Abdomen" has strings "ABDOMEN" and "Abdomen, NOS".
    Similarly, the concept "Lung Cancer" has string "Cancer, Lung".
    And the concept "1,4-alpha-Glucan Branching Enzyme" has a string
    "1,4 alpha Glucan Branching Enzyme".

    Note that the order in which the various normalizations occur is important.
    The above order is correct.
    important; e.g., parentheticals must be removed before either lowercasing
    or normalized syntactic uninversion (which includes NOS normalization)
    are performed.

    @param string meta string to normalize.
    @return normalized meta string.
    """
    try:
        pstring = remove_left_parentheticals(metastring.strip())
        un_pstring = nls_strings.normalized_syntactic_uninvert_string(pstring)
        lc_un_pstring = un_pstring.lower()
        hlc_un_pstring = remove_hyphens(lc_un_pstring)
        norm_string = strip_possessives(hlc_un_pstring)
        return norm_string.strip()
    except TypeError as te:
        print('%s: string: %s' % (te, metastring))


left_parenthetical = ["[X]", "[V]", "[D]", "[M]", "[EDTA]", "[SO]", "[Q]"]


def remove_left_parentheticals(astring):
    """ remove_left_parentheticals(+String, -ModifiedString)

    remove_left_parentheticals/2 removes all left parentheticals
    (see left_parenthetical/1) from String. ModifiedString is what is left. """
    for lp in left_parenthetical:
        if astring.find(lp) == 0:
            return astring[len(lp):].strip()
    return astring


def remove_hyphens(astring):
    """ remove_hyphens/2 removes hyphens from String and removes extra blanks
    to produce ModifiedString. """
    return remove_extra_blanks(astring.replace('-', ' ')).strip()


def remove_extra_blanks(astring):
    """ remove extra inter-token blanks """
    return astring.replace('  ', ' ')


def normalize_ast_string(aststring):
    """ similar to normalize_meta_string except hyphens are not removed
     normalizeAstString(String) performs "normalization" on String to produce
    NormalizedMetaString.  The purpose of normalization is to detect strings
    which are effectively the same.  The normalization process (also called
    lexical filtering) consists of the following steps:

       * syntactic uninversion;
       * conversion to lowercase;
       * stripping of possessives.

    """
    un_pstring = nls_strings.syntactic_uninvert_string(aststring)
    lc_un_pstring = un_pstring.lower()
    hlc_un_pstring = remove_hyphens(lc_un_pstring)
    norm_string = strip_possessives(hlc_un_pstring)
    return norm_string


if __name__ == '__main__':
    # a test fixture to test normalizeMetaString method.
    if len(sys.argv) > 1:
        print('"%s"' % normalize_meta_string(' '.join(sys.argv[1:])))

# fin: mwi_utilities
