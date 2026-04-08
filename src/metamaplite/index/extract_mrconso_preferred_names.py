"""
 Generate table consisting records each with a pair containing a
 concept unique identifier and the preferred name for that concept.

  MRCONSO fields used:
  | CUI |concept unique identifier |field 0|
  | LAT |language of term          |field 1|
  | TS  |term status               |field 2|
  | STT |string type               |field 4|
  | STR |string                    |field 14|


  Format of cui/preferred name output file
  | CUI |concept unique identifier |field 0|
  | STR |preferred name            |field 1|

See also:

+ Concept Names and Sources (File = MRCONSO.RRF)
  https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.concept_names_and_sources_file_mr/
"""


def create_table(mrconsofilename, cuiconceptfilename, language,
                 display_warnings, releaseformat):
    "Process input mrconso file and output cuiinfo/preferredname file."
    with (open(mrconsofilename) as inchan,
          open(cuiconceptfilename, 'w') as outchan):
        for line in inchan.readlines():
            fields = line.split('|')
            if len(fields) >= 15:
                lat = fields[1]
                if lat == language:
                    cui = fields[0]
                    ts = fields[2]
                    stt = fields[4]
                    mstr = fields[14]
                    if (ts == 'P') & (stt == 'PF'):
                        outchan.write('{}|{}\n'.format(cui, mstr))
