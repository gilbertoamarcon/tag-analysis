#!/usr/bin/python
import requests
import re
from collections import OrderedDict

taxonomy = OrderedDict([
	('quality', OrderedDict([('exact', []), ('approximation', []), ('heuristic', [])]) ),
	('horizon', OrderedDict([('finite-horizon', []), ('infinite-horizon', [])]) ),
	('type', OrderedDict([('dp', []), ('heuristic-search', []), ('expectation-maximization', []), ('hierarchical-decomposition', []), ('optimization', [])]) ),
	('solution', OrderedDict([('decision-tree', []), ('deterministic-fsc', []), ('stochastic-fsc', [])]) ),
])

nice_names = {
	'exact': 'Exact',
	'approximation': 'Approximation',
	'heuristic': 'Heuristic',
	'exact': 'Exact',
	'decision-tree': 'Decision Tree',
	'deterministic-fsc': 'Det. FSC',
	'stochastic-fsc': 'Stoch. FSC',
}

PATTERN = '@\w+{(.*),'
PREFIX = 'http://www.citeulike.org/bibtex/user/marcondg/tag/'
SUFFIX = '/order/year,asc,?do_username_prefix=0&key_type=4&incl_amazon=1&clean_urls=1&smart_wrap=1&q='

def get_list(tag):
	response = ''.join(requests.get(PREFIX+tag+SUFFIX))
	return re.findall(PATTERN, response)

def sort_set(input):
	ls = list(input)
	struct = [(re.findall('\d{4}', k),k) for k in ls]
	return '\cite{' + ','.join([k[1] for k in sorted(struct)]) + '};'

for t in taxonomy:
	for v in taxonomy[t]:
		taxonomy[t][v] = get_list(v)

table = 'Quality;'
for q in taxonomy['solution']:
	table += '%s;' % nice_names[q]

for q in taxonomy['quality']:
	table += '\n%s;' % nice_names[q]
	table += sort_set(set(taxonomy['quality'][q]) & set(taxonomy['solution']['decision-tree']))
	table += sort_set(set(taxonomy['quality'][q]) & set(taxonomy['solution']['deterministic-fsc']))
	table += sort_set(set(taxonomy['quality'][q]) & set(taxonomy['solution']['stochastic-fsc']))

print table


