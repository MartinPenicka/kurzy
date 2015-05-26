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
currency_dict = {}
# ---
		
def read_data(self):
	
	if os.path.exists(db_file_path) and os.stat(db_file_path).st_size > 0:
		self.cur_list = pickle.load(open(db_file_path, 'r'))

	else:
		for u in url_all:
		
			html = urllib2.urlopen(u).read()
	
			soup = BeautifulSoup(html)
	
			for tr in soup.find_all('tr'):
		
				tds = tr.find_all('td')
		
				if len(tds) != 5:
				    continue
		
				code = tds[3].get_text()
				price = float(tds[4].get_text().replace(',', '.')) / float(tds[2].get_text().replace(',', '.'))
		
				self.cur_list[code] = price
				
		pickle.dump(self.cur_list, open(db_file_path, 'w'))

if __name__ == '__main__':
	
	if len(sys.argv) == 1:
		print 'Zadejte kód měny'
		exit()
		
	currency_holder = CHolder()
	
	code = sys.argv[1]
	price = currency_holder.cur_list[code.upper()]
	
	if isinstance(price, str):
		print price
		exit()
	
	if len(sys.argv) == 3:
		
		try:
			amount = float(sys.argv[2])
			print price * amount
			
		except:
			print 'Špatně zadané množství měny'
			
		exit()
		
	else:
		print price
		exit()
