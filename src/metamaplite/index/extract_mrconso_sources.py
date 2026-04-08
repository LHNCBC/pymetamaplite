"""
 Generate table consisting records each with a pair containing a
 concept unique identifier, string unique identifier

  MRCONSO fields used:
  |CUI |concept unique identifier |field 0|
  |LAT |language of term          |field 1|
  |SUI |string unique identifier  |field 5|
  |SAB |source abbreviation       |field 11|
  |TTY |source term type          |field 12|
  |STR |string                    |field 14|

  Format of cui -&gt; sui, str, sab, tty output file.
  |CUI |concept unique identifier |field 0|
  |SUI |string unique identifier  |field 1|
  |STR |string                    |field 2|
  |SAB |source abbreviation       |field 3|
  |TTY |source term type          |field 4|

See also:

+ Concept Names and Sources (File = MRCONSO.RRF)
  https://www.ncbi.nlm.nih.gov/books/NBK9685/table/ch03.T.concept_names_and_sources_file_mr/
"""


def create_table(mrconsofilename, cuisourceinfofilename,
                 first_of_each_source_only, include_sui_info,
                 language, displayWarnings, releaseformat):
    """ Process input mrconso file and output cui/sourcinfo file. """
    cui0 = "C......"
    n = 0
    with (open(mrconsofilename) as inchan,
          open(cuisourceinfofilename, 'w') as outchan):
        for line in inchan.readlines():
            fields = line.split('|')
            if len(fields) >= 15:
                lat = fields[1]
                if lat == language:
                    cui = fields[0]
                    sui = fields[5]
                    sab = fields[11]
                    tty = fields[12]
                    mstr = fields[14]
                    if cui != cui0:
                        n = 0
                        cui0 = cui
                    outchan.write(
                        '{}\n'.format('|'.join([cui, sui, str(n), mstr, sab, tty])))
            n += 1
