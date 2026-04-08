"""
 Generates a term to treecodes table for MetaMapLite
 inputs MRCONSO.RRF, MRSAT.RRF

 Load MRSAT table into map keyed by CUI, keeping only MeSH records
 with ATN field with value "MN".

 Create treecode file from MRCONSO table using previously generated
 CUI to MRSAT dictionary map to create records of form:

 (131)I-Macroaggregated Albumin|x.x.x.x
 (131)I-MAA|x.x.x.x
 1,2-Dipalmitoylphosphatidylcholine|D10.570.755.375.760.400.800.224
 1,2 Dipalmitoylphosphatidylcholine|D10.570.755.375.760.400.800.224
 1,2-Dihexadecyl-sn-Glycerophosphocholine|D10.570.755.375.760.400.800.224
 1,2 Dihexadecyl sn Glycerophosphocholine|D10.570.755.375.760.400.800.224
 1,2-Dipalmitoyl-Glycerophosphocholine|D10.570.755.375.760.400.800.224
 1,2 Dipalmitoyl Glycerophosphocholine|D10.570.755.375.760.400.800.224
 Dipalmitoylphosphatidylcholine|D10.570.755.375.760.400.800.224
 Dipalmitoylglycerophosphocholine|D10.570.755.375.760.400.800.224
 ...

MRSAT fields used:
  |CUI |concept unique identifier |field 0 |
  |ATN |attribute name            |field 8 |
  |ATV |attribute value           |field 10|

MRCONSO fields used:
  |CUI |concept unique identifier |field 0|
  |SAB |source abbreviation       |field 11|
  |STR |string                    |field 14|


Note: this only uses the MesH vocabulary.
See also:

+ Concept Names and Sources (File = MRCONSO.RRF)
  https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.concept_names_and_sources_file_mr/
+ Simple Concept and Atom Attributes (File = MRSAT.RRF)
  https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.simple_concept_and_atom_attribute/
"""
import argparse


def generate_cui_to_treecodes(mrsatfilename):
    """Given list of Mesh MRSAT records with ATN field = "MN", create
   a map of treecodes (in ATV field) by cui.  Returns a dictionary
   of treecodelists by cui.

    """
    cui_to_treecodes_dict = {}
    with open(mrsatfilename) as chan:
        for line in chan.readlines():
            fields = line.split('|')
            if len(fields) > 11:
                atn = fields[8]
                if atn == 'MN':
                    # atv field is a MeSH treecode
                    cui = fields[0]
                    atv = fields[10]
                    if cui in cui_to_treecodes_dict:
                        cui_to_treecodes_dict[cui].append(atv)
                    else:
                        cui_to_treecodes_dict[cui] = [atv]
    return cui_to_treecodes_dict


def write_term_treecode_list_to_file(treecodefilename, mrconsofilename,
                                     cui_to_treecodes_dict):
    with (open(mrconsofilename) as inchan,
          open(treecodefilename, 'w') as outchan):
        for line in inchan.readlines():
            fields = line('|')
            sab = fields[11]
            if sab == 'MSH':
                cui = fields[0]
                mstr = fields[14]
                if cui in cui_to_treecodes_dict:
                    for treecode in cui_to_treecodes_dict[cui]:
                        outchan.write('{}|{}\n'.format(mstr, treecode))


def create_table(mrconsofilename, mrsatfilename, treecodefilename):
    "Create treecodes table from MRSAT.RRF and MRCONSO.RRF"
    cui_to_treecodes_dict = generate_cui_to_treecodes(mrsatfilename)
    write_term_treecode_list_to_file(
        treecodefilename, mrconsofilename, cui_to_treecodes_dict)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        prog='ExtractTreecodes',
        description='generate treecode table from MRCONSO and MRSAT')
    parser.add_argument('mrconsofilename')
    parser.add_argument('mrsatfilename')
    parser.add_argument('treecodefilename')
    args = parser.parse_args()
    create_table(args.mrconsofilename, args.mrsatfilename,
                 args.treecodefilename)
