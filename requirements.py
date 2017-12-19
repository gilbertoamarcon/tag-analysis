#!/usr/bin/python
import string
import sys
import bibtexparser
from collections import OrderedDict

requirements = OrderedDict([
	('concurrent','Concurrent action execution'),
	('nondet-outcomes','Nondeterministic action outcomes'),
	('partial-obs','Partial observability'),
	('lim-com','Limited or non-existing communication infrastructure'),
	('temporal','Temporal constraints'),
	('continuous','Continuous fluents'),
	('linear','Linear time-varying fluents'),
	('nonlinear','Nonlinear time-varying fluents'),
	('none','None of the above'),
])

def get_planner_based_table(requirements,key_oriented):
	if 'none' in requirements:
		del requirements['none']
	nrows = len(requirements)+1
	alpha_indexes = list(string.ascii_lowercase)[:len(requirements)]
	align = 'V{3} X V{3}' + '|'.join(['c' for i in range(nrows-1)]) + 'V{3}'
	reqs = '&'.join(['\\textbf{%c}'%r for r in alpha_indexes])
	table = ''
	table += '\\begin{table}[!ht]\n'
	table += '\centering\n'
	table += '\caption[Planner Features.]{Planner Features.'
	for n,r in enumerate(requirements):
		table += ' %c) %s.' % (alpha_indexes[n], requirements[r])
	table += '}\n'
	table += '\label{tab:requirements}\n'
	table += '\\begin{tabularx}{\linewidth}{%s}\n' % align
	table += '\hline \Cline{1pt}{1-%d}\n' % nrows
	table += '\multirow{2}{*}{\\textbf{Planner}} & \multicolumn{%d}{c V{3}}{\\textbf{Features}} \\\\ \Cline{1pt}{2-%d}\n' % (nrows-1,nrows)
	table += '& '+reqs+' \\\\ \hline \Cline{1pt}{1-%d}\n' % nrows
	for p in reversed(sorted(key_oriented.keys())):
		table += '\cite{'+ ','.join(sorted(list(key_oriented[p]))) +'} & '
		req = []
		for r in p:
			if r:
				req.append('X')
			else:
				req.append('-')
		table += ' & '.join(req) + ' \\\\ \hline\n'
	table += '\Cline{1pt}{1-%d}\n' % nrows
	table += '\end{tabularx}\n\end{table}\n'
	return table

if len(sys.argv) < 2:
	print '\033[31m[ERROR]\033[0m Missing argument: Please provide the file directory.'
	sys.exit(2)
else:
	file_dir = sys.argv[1]

def load_bib(filename,requirements):

	# Getting the BIB Dictionary
	with open(filename) as f:
		entry_dict = bibtexparser.loads(f.read()).get_entry_dict()

	# Getting tag sets
	bib = OrderedDict()
	for key in entry_dict:
		if 'keyword' in entry_dict[key]:
			reqs = set(entry_dict[key]['keyword'].encode('ascii').split(', ')) & set(requirements.keys())
			if len(reqs) > 0:
				bib[key] = reqs

	# Enumerating
	if 'none' in requirements:
		del requirements['none']
	for b in bib:
		bib[b] = tuple([r in bib[b] for r in requirements])

	return bib

bib = load_bib(file_dir+'/bib.bib',requirements)

key_oriented = {}
for b in bib:
	if bib[b] not in key_oriented:
		key_oriented[bib[b]] = set()
	key_oriented[bib[b]].add(b)

with open(file_dir+'/table.tex','w') as f:
	f.write(get_planner_based_table(requirements,key_oriented))

