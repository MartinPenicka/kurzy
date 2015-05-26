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

import urllib2
from bs4 import BeautifulSoup
import os, sys

# Constants
url_std = 'https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_devizoveho_trhu/denni_kurz.jsp'
url_oth = 'https://www.cnb.cz/cs/financni_trhy/devizovy_trh/kurzy_ostatnich_men/kurzy.jsp'
	
url_all = [url_std, url_oth]
db_file = '/tmp/kurzy.db'
# ---

class Currency(object):
	
	def __init__(self, tr_object=None, _state='', _c_name='', _code='', _price=''):
		
		if tr_object != None:
			
			self.parse_data(tr_object)
			
		else:
			
			self.state = _state
			self.c_name = _c_name
			self.code = _code
			self.price = float(_price)
			
		self.debug = False
		
	def __str__(self):
		
		ret_str = ''
		ret_str += 'Stát :\t' + self.state + '\n'
		ret_str += 'Jméno měny :\t' + self.c_name + '\n'
		ret_str += 'Kód měny :\t' + self.code + '\n'
		ret_str += 'Cena za jednotku (Kč) :\t' + str(self.price)
		
		return ret_str
	
	def parse_data(self, tr_object):
		
		tds = tr_object.find_all('td')
		
		self.state = tds[0].get_text()
		self.state.replace(',', '')
		self.c_name = tds[1].get_text()
		self.code = tds[3].get_text()
		
		self.price = float(tds[4].get_text().replace(',', '.')) / float(tds[2].get_text().replace(',', '.'))
	
	def get_csv_form(self):
		
		return '{0}|{1}|{2}|{3}\n'.format(self.state, self.c_name, self.code, str(self.price))
	
class CHolder(object):
	
	def __init__(self, web_url, db_file):
		
		self.url = web_url
		self.db_file_path = db_file
		self.cur_list = []
		
		#DEBUG_START
		print 'CHolder vytvořen'
		print '---'
		print 'Adresa serveru : ' + str(self.url)
		print 'Cesta k souboru s lokálními daty : ' + str(self.db_file_path)
		print ''
		print 'Načítám data ...'
		#DEBUG_END
		self.read_data()
		
		if not os.path.exists(self.db_file_path):
			
			#DEBUG_START
			print 'Soubor s lokální databází neexistuje, vytvářím ho ...'
			#DEBUG_END
			self.write_data()
		
	def __str__(self):
		
		ret_str = ''
		
		for item in self.cur_list:
			
			ret_str += str(item) + '\n'
			
		return ret_str
		
	def read_data(self):
		
		if os.path.exists(self.db_file_path) and os.stat(self.db_file_path).st_size > 0:
			
			#DEBUG_START
			print 'Načítám data z lokální databáze'
			#DEBUG_END
			
			with open(self.db_file_path, 'r') as fr:
				
				for line in fr.readlines():
					
					values = line.split('|')
					self.cur_list.append(Currency(tr_object=None, _state=values[0], _c_name=values[1], _code=values[2], _price=values[3]))
			
		else:
			
			#DEBUG_START
			print 'Načítám data ze serveru'
			#DEBUG_END
		
			for u in self.url:
			
				response = urllib2.urlopen(u)
		
				html = response.read()
		
				soup = BeautifulSoup(html)
		
				for tr in soup.find_all('tr'):
			
					tds = tr.find_all('td')
			
					if len(tds) != 5:
					    continue
			
					self.cur_list.append(Currency(tr))
			
	def write_data(self):
		
		try:
			with open(self.db_file_path, 'w') as fw:
				
				for item in self.cur_list:
					fw.write(item.get_csv_form())
		except:
			print 'Error : nelze zpasat do souboru s databází'
				
	def get_item_by_code(self, code):
		
		up_code = code.upper()
		print self.cur_list
		for item in self.cur_list:
			
			if item.code == up_code:
				
				return item
			
		return 'Kód nenalezen'
	
	def get_price_by_code(self, code):
		
		item = self.get_item_by_code(code)
		if isinstance(item, str):
			return item
		else:
			return item.price
	
	def get_price_by_state(self, state_name):
		
		for item in self.cur_list:
			
			if item.state == state_name:
				
				return item.price
			
		else:
			
			return 'Stát nenalezen'
			
if __name__ == '__main__':
	
	if len(sys.argv) == 1:
		print 'Zadejte kód měny'
		exit()
		
	currency_holder = CHolder(url_all, db_file)
	
	code = sys.argv[1]
	price = currency_holder.get_price_by_code(code)
	
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
