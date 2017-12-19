#!/usr/bin/python
import string
import sys
import bibtexparser
from collections import OrderedDict

ratings = OrderedDict([
	(5,{'papers': [], 'class': 'Will read.'}),
	(4,{'papers': [], 'class': 'Skimmed, but will revisit.'}),
	(1,{'papers': [], 'class': 'Read, but will revisit.'}),
	(3,{'papers': [], 'class': 'Skimmed and will not revisit.'}),
	(0,{'papers': [], 'class': 'Read and will not revisit.'}),
	(2,{'papers': [], 'class': 'Abstract/Intro read and will not revisit.'}),
])

keywords = set(['mine','sea'])

def get_planner_based_table(ratings):
	table = ''
	table += '\\begin{table}[!ht]\n'
	table += '\centering\n'
	table += '\caption{Paper Reading Status.}\n'
	table += '\label{tab:reading}\n'
	table += '\\begin{tabular}{l V{3} l}\n'
	table += '\\textbf{Status} & \\textbf{Papers} \\\\ \hline \Cline{3pt}{1-2}\n'
	for r in ratings:
		table += '\\textbf{%s} & \cite{%s} \\\\ \n' % (ratings[r]['class'], ','.join(sorted(ratings[r]['papers'])))
	table += '\end{tabular}\n'
	table += '\end{table}\n'
	return table

if len(sys.argv) < 2:
	print '\033[31m[ERROR]\033[0m Missing argument: Please provide the file directory.'
	sys.exit(2)
else:
	file_dir = sys.argv[1]

def load_bib(filename):

	# Getting the BIB Dictionary
	with open(filename) as f:
		entry_dict = bibtexparser.loads(f.read()).get_entry_dict()

	# Getting tag sets
	for key in entry_dict:
		if 'keyword' in entry_dict[key] and len(set(entry_dict[key]['keyword'].encode('ascii').split(', ')) & keywords) > 0:
			continue
		if 'priority' in entry_dict[key]:
			idx = int(entry_dict[key]['priority'].encode('ascii'))
			ratings[idx]['papers'].append(key)


load_bib(file_dir+'/bib.bib')

with open(file_dir+'/table.tex','w') as f:
	f.write(get_planner_based_table(ratings))