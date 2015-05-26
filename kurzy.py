#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
(C) Copyright 2015 Martin Pěnička

Authors:
 *	 Martin Pěnička <penickamx@gmail.com>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

from __future__ import division
from bs4 import BeautifulSoup
import urllib2, os, sys, pickle

# Constants
url_std = 'https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.jsp'
url_oth = 'https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_ostatnich_men/kurzy.jsp'
	
url_all 	 = [url_std, url_oth]
db_file_path = '/tmp/kurzy.db'
# ---
		
def get_currency_dict():

	if os.path.exists(db_file_path) and os.stat(db_file_path).st_size > 0:
		currency_dict = pickle.load(open(db_file_path, 'r'))

	else:
		currency_dict = {}
		
		for u in url_all:
		
			html = urllib2.urlopen(u).read()
			soup = BeautifulSoup(html)
			
			#a = [tr.find_all('td') for tr in soup.find_all('tr') if len(tr.find_all('td')) != 5]
			for tr in soup.find_all('tr'):
		
				tds = tr.find_all('td')
		
				if len(tds) != 5:
				    continue
		
				code = tds[3].get_text()
				price = float(tds[4].get_text().replace(',', '.')) / float(tds[2].get_text().replace(',', '.'))
		
				currency_dict[code] = price
				
		pickle.dump(currency_dict, open(db_file_path, 'w'))
	return currency_dict

if __name__ == '__main__':
	
	if len(sys.argv) == 1:
		sys.stderr.write('Zadejte kód měny\n')
		exit()
	
	code = sys.argv[1]
	try:
		price = get_currency_dict()[code.upper()]
	except KeyError:
		sys.stderr.write('Kód měny nenalezen.\n')
		exit()
	
	if len(sys.argv) == 3:
		try:
			amount = float(sys.argv[2])
			sys.stdout.write(str(price * amount)+'\n')
		except:
			sys.stderr.write('Špatně zadané množství měny.\n')
		exit()
	else:
		sys.stdout.write(str(price)+'\n')
		exit()
