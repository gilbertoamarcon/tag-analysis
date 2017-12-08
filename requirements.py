#!/usr/bin/python
import requests
import string
import sys
import re
import bibtexparser
from collections import OrderedDict
from itertools import combinations

requirements = OrderedDict([
	('nonlinear','Nonlinear time-varying variables'),
	('linear','Linear time-varying variables'),
	('continuous','Continuous variables'),
	('temporal','Temporal constraints'),
	('lim-com','Limited or no communication'),
	('partial-obs','Partial observability'),
	('nondet-outcomes','Non-deterministic action outcomes'),
	('concurrent','Concurrent action execution'),
	('none','None of the above'),
])

def get_planners(tag, bib):
	ret_val = []
	for k in bib:
		if tag in bib[k]:
			ret_val.append(k)
	return ret_val

def get_feature_based_table(requirements, bib):
	table = '\\begin{table}[!ht]\n\centering\n\caption{Planning Requirements.}\n\label{tab:requirements}\n\\begin{tabular}{l|l}\n\\textbf{Requirement} &  \\textbf{Planners} \\\\ \cline{1-2}\n'
	for r in requirements:
		table += '\\textbf{' + requirements[r] + '} & \cite{' + ','.join(get_planners(r,bib)) + '} \\\\ \n'
	table += '\end{tabular}\n\end{table}\n'
	return table

def get_planner_based_table(requirements,key_oriented):
	nrows = len(requirements)+1
	alpha_indexes = list(string.ascii_lowercase)[:len(requirements)]
	align = 'X | ' + '|'.join(['c' for i in range(nrows-1)])
	reqs = '&'.join(['\\textbf{%c}'%r for r in alpha_indexes])
	table = ''
	table += '\\begin{table}[!ht]\n'
	table += '\centering\n'
	table += '\caption{Planning Requirements.'
	for n,r in enumerate(requirements):
		table += ' %c) %s.' % (alpha_indexes[n], requirements[r])
	table += '}\n'
	table += '\label{tab:requirements}\n'
	table += '\\begin{tabularx}{\linewidth}{%s}\n' % align
	table += '\\textbf{Planner} & '+reqs+' \\\\ \cline{1-%d}\n' % nrows
	for p in key_oriented:
		table += '\cite{'+ ','.join(key_oriented[p]) +'} & '
		req = []
		for r in requirements:
			if r in p:
				req.append('X')
			else:
				req.append('-')
		table += ' & '.join(req) + ' \\\\ \cline{1-%d}\n' % nrows
	table += '\end{tabularx}\n\end{table}\n'
	return table

if len(sys.argv) < 2:
	print '\033[31m[ERROR]\033[0m Missing argument: Please provide the file directory.'
	sys.exit(2)
else:
	file_dir = sys.argv[1]

# Getting BIB Dictionary
with open(file_dir+'/bib.bib') as f:
	entry_dict = bibtexparser.loads(f.read()).get_entry_dict()

# Getting tag sets
bib = {}
for key in entry_dict:
	if 'keyword' in entry_dict[key]:
		bib[key] = set(entry_dict[key]['keyword'].encode('ascii').split(', '))

# Filtering
for b in bib:
	bib[b] &= set(requirements.keys())

key_oriented = {}
for b in bib:
	key = tuple(sorted(list(bib[b])))
	if key not in key_oriented:
		key_oriented[key] = set()
	key_oriented[key].add(b)

with open(file_dir+'/table.tex','w') as f:
	f.write(get_planner_based_table(requirements,key_oriented))