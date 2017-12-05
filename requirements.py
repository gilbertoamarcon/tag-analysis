#!/usr/bin/python
import requests
import sys
import re
from collections import OrderedDict

if len(sys.argv) < 2:
	print '\033[31m[ERROR]\033[0m Missing argument: Please provide the output file directory.'
	sys.exit(2)
else:
	filename = sys.argv[1]

requirements = OrderedDict([
	('concurrent','Concurrent action execution'),
	('nondet-outcomes','Non-deterministic action outcomes'),
	('partial-obs','Partial observability'),
	('decentralized','Decentralized execution'),
	('lim-com','Limited or no communication'),
	('temporal','Temporal constraints'),
	('continuous','Continuous variables'),
	('linear','Linear time-varying variables'),
	('nonlinear','Nonlinear time-varying variables'),
])

PATTERN = '@\w+{(.*),'
PREFIX = 'http://www.citeulike.org/bibtex/user/marcondg/tag/'
SUFFIX = '/order/year,asc,?do_username_prefix=0&key_type=4&incl_amazon=1&clean_urls=1&smart_wrap=1&q='

def get_list(tag):
	response = ''.join(requests.get(PREFIX+tag+SUFFIX))
	return re.findall(PATTERN, response)

table = '\\begin{table*}[!ht]\n\centering\n\caption{Planning Requirements.}\n\label{tab:requirements}\n\\begin{tabular}{l|l}\n\\textbf{Requirement} &  \\textbf{Planners} \\\\ \cline{1-2}\n'
for r in requirements:
	table += '\\textbf{' + requirements[r] + '} & \cite{' + ','.join(get_list(r)) + '} \\\\ \n'
table += '\end{tabular}\n\end{table*}\n'

with open(filename,'w') as f:
	f.write(table)