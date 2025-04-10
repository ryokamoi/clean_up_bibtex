import bibtexparser
from bibtexparser.bparser import BibTexParser
from collections import defaultdict

def is_arxiv_entry(entry):
    journal = entry.get('journal', '').lower()
    return 'arxiv' in journal

def load_bibtex_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as bibtex_file:
        bibtex_str = bibtex_file.read()
        parser = BibTexParser(common_strings=True)
        # Don't use homogenize_latex_encoding to avoid modifying titles
        bib_database = bibtexparser.loads(bibtex_str, parser=parser)
    return bib_database.entries

def remove_duplicates(entries):
    entry_dict = defaultdict(list)
    for entry in entries:
        entry_dict[entry['ID']].append(entry)

    unique_entries = []
    for key, dup_entries in entry_dict.items():
        if len(dup_entries) == 1:
            unique_entries.append(dup_entries[0])
        else:
            non_arxiv = [e for e in dup_entries if not is_arxiv_entry(e)]
            if non_arxiv:
                unique_entries.append(non_arxiv[0])  # keep first non-arxiv
            else:
                unique_entries.append(dup_entries[0])  # fallback to first if all are arxiv
    return sorted(unique_entries, key=lambda x: x['ID'])

def save_bibtex_file(entries, output_path):
    bib_database = bibtexparser.bibdatabase.BibDatabase()
    bib_database.entries = entries
    writer = bibtexparser.bwriter.BibTexWriter()
    writer.indent = '    '
    writer.order_entries_by = ('ID',)
    writer.comma_first = False
    with open(output_path, 'w', encoding='utf-8') as bibtex_file:
        bibtex_file.write(writer.write(bib_database))

# Example usage:
input_file = 'input.bib'
output_file = 'cleaned_output.bib'

entries = load_bibtex_file(input_file)
unique_sorted_entries = remove_duplicates(entries)
save_bibtex_file(unique_sorted_entries, output_file)

print(f"Cleaned BibTeX file saved to: {output_file}")
