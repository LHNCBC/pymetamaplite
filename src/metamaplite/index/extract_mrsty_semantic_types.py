"""
Extract MRSTY Semantic Types
Purpose:  Extracts semantic type information from mrsty.eng.

Generate cui_st.txt of form:

    cui|semtype

example cui_st.txt (abbreviated):

    C0000005|aapp
    C0000005|irda
    C0000005|phsu
    C0000039|orch
    C0000039|phsu
    C0000052|aapp
    C0000052|enzy
    C0000074|orch
    C0000084|aapp
    C0000084|bacs

MRSTY table:

    col|name|description
    --------------------------------------------
      0|CUI |Unique indentifier of concept
      1|TUI |Unique indentifier of Semantic Type
      2|STN |Semantic Type tree number.
      3|STY |Semantic Type.
      4|ATUI|Unique indentifier for attribute
      5|CVF |Content View Flag

See also:

+ 3.3.7. Semantic Types (File = MRSTY.RRF)
  https://www.ncbi.nlm.nih.gov/books/NBK9685/
"""


default_semtype_types_raw = {
    "Acquired Abnormality": "acab",
    "Activity": "acty",
    "Age Group": "aggp",
    "Amino Acid Sequence": "amas",
    "Amino Acid,  Peptide, or Protein": "aapp",
    "Amphibian": "amph",
    "Anatomical Abnormality": "anab",
    "Anatomical Structure": "anst",
    "Animal": "anim",
    "Antibiotic": "antb",
    "Archaeon": "arch",
    "Bacterium": "bact",
    "Behavior": "bhvr",
    "Biologic Function": "biof",
    "Biologically Active Substance": "bacs",
    "Biomedical Occupation or Discipline": "bmod",
    "Biomedical or Dental Material": "bodm",
    "Bird": "bird",
    "Body Location or Region": "blor",
    "Body Part, Organ, or Organ Component": "bpoc",
    "Body Space or Junction": "bsoj",
    "Body Substance": "bdsu",
    "Body System": "bdsy",
    "Carbohydrate Sequence": "crbs",
    "Carbohydrate": "carb",
    "Cell Component": "celc",
    "Cell Function": "celf",
    "Cell or Molecular Dysfunction": "comd",
    "Cell": "cell",
    "Chemical Viewed Functionally": "chvf",
    "Chemical Viewed Structurally": "chvs",
    "Chemical": "chem",
    "Classification": "clas",
    "Clinical Attribute": "clna",
    "Clinical Drug": "clnd",
    "Conceptual Entity": "cnce",
    "Congenital Abnormality": "cgab",
    "Daily or Recreational Activity": "dora",
    "Diagnostic Procedure": "diap",
    "Disease or Syndrome": "dsyn",
    "Drug Delivery Device": "drdd",
    "Educational Activity": "edac",
    "Eicosanoid": "eico",
    "Element, Ion, or Isotope": "elii",
    "Embryonic Structure": "emst",
    "Entity": "enty",
    "Environmental Effect of Humans": "eehu",
    "Enzyme": "enzy",
    "Eukaryote": "euka",
    "Event": "evnt",
    "Experimental Model of Disease": "emod",
    "Family Group": "famg",
    "Finding": "fndg",
    "Fish": "fish",
    "Food": "food",
    "Fully Formed Anatomical Structure": "ffas",
    "Functional Concept": "ftcn",
    "Fungus": "fngs",
    "Gene or Gene Product": "gngp",
    "Gene or Genome": "gngm",
    "Genetic Function": "genf",
    "Geographic Area": "geoa",
    "Governmental or Regulatory Activity": "gora",
    "Group Attribute": "grpa",
    "Group": "grup",
    "Hazardous or Poisonous Substance": "hops",
    "Health Care Activity": "hlca",
    "Health Care Related Organization": "hcro",
    "Hormone": "horm",
    "Human": "humn",
    "Human-caused Phenomenon or Process": "hcpp",
    "Idea or Concept": "idcn",
    "Immunologic Factor": "imft",
    "Indicator, Reagent, or Diagnostic Aid": "irda",
    "Individual Behavior": "inbe",
    "Injury or Poisoning": "inpo",
    "Inorganic Chemical": "inch",
    "Intellectual Product": "inpr",
    "Laboratory Procedure": "lbpr",
    "Laboratory or Test Result": "lbtr",
    "Language": "lang",
    "Lipid": "lipd",
    "Machine Activity": "mcha",
    "Mammal": "mamm",
    "Manufactured Object": "mnob",
    "Medical Device": "medd",
    "Mental Process": "menp",
    "Mental or Behavioral Dysfunction": "mobd",
    "Molecular Biology Research Technique": "mbrt",
    "Molecular Function": "moft",
    "Molecular Sequence": "mosq",
    "Natural Phenomenon or Process": "npop",
    "Neoplastic Process": "neop",
    "Neuroreactive Substance or Biogenic Amine": "nsba",
    "Nucleic Acid, Nucleoside, or Nucleotide": "nnon",
    "Nucleotide Sequence": "nusq",
    "Object": "objt",
    "Occupation or Discipline": "ocdi",
    "Occupational Activity": "ocac",
    "Organ or Tissue Function": "ortf",
    "Organic Chemical": "orch",
    "Organism Attribute": "orga",
    "Organism Function": "orgf",
    "Organism": "orgm",
    "Organization": "orgt",
    "Organophosphorus Compound": "opco",
    "Pathologic Function": "patf",
    "Patient or Disabled Group": "podg",
    "Pharmacologic Substance": "phsu",
    "Phenomenon or Process": "phpr",
    "Physical Object": "phob",
    "Physiologic Function": "phsf",
    "Plant": "plnt",
    "Population Group": "popg",
    "Professional Society": "pros",
    "Professional or Occupational Group": "prog",
    "Qualitative Concept": "qlco",
    "Quantitative Concept": "qnco",
    "Receptor": "rcpt",
    "Regulation or Law": "rnlw",
    "Reptile": "rept",
    "Research Activity": "resa",
    "Research Device": "resd",
    "Self-help or Relief Organization": "shro",
    "Sign or Symptom": "sosy",
    "Social Behavior": "socb",
    "Spatial Concept": "spco",
    "Steroid": "strd",
    "Substance": "sbst",
    "Temporal Concept": "tmco",
    "Therapeutic or Preventive Procedure": "topp",
    "Tissue": "tisu",
    "Vertebrate": "vtbt",
    "Virus": "virs",
    "Vitamin": "vita",
}


def load_st_raw_file(st_raw_filename):
    semtype_to_stabbev_dict = {}
    with open(st_raw_filename) as chan:
        for line in chan.readlines():
            fields = line.split('|')
            semtype_to_stabbev_dict[fields[0]] = fields[1]
    return semtype_to_stabbev_dict


def create_table(mrstyfilename, cuistfilename,
                 display_warnings, releaseformat, st_raw_filename):
    "Process input mrsty file and output cui/semantictype file."
    if st_raw_filename is not None:
        semtype_to_stabbev_dict = load_st_raw_file(st_raw_filename)
    else:
        semtype_to_stabbev_dict = default_semtype_types_raw
    with open(mrstyfilename) as inchan, open(cuistfilename, 'w') as outchan:
        for line in inchan.readlines():
            fields = line.split('|')
            cui = fields[0]
            sty = fields[3]
            if sty in semtype_to_stabbev_dict:
                semtype = semtype_to_stabbev_dict[sty]
            else:
                semtype = 'unkn'  # use unknown if mapping not found
            outchan.write('{}|{}\n'.format(cui, semtype))
