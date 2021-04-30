from ..search import Search
from .settings import GOOGLE_URLS

from bs4 import BeautifulSoup
import re

class GSearch(Search):
	'''
	GSearch is a class for gather result from Google Search Engine.
	Search --> Inherited.
	'''
	
	URL = GOOGLE_URLS['GOOGLE']
	LABELS = ['date', 'title', 'description', 'domain', 'link']

	def __init__(self, search_word, start_page=1, max_page=1):
		super().__init__(search_word, start_page, max_page)
		self.start_page_num = (start_page-1) * 10
		self.max_page_num = (max_page-1) * 10
		self.pages = self.get_result(GSearch.URL, self.start_page_num, self.max_page_num)

		self.titles = []
		self.descs = []
		self.dates = []
		self.domains = []
		self.links = []


	def get_main(self, tag, attr=None, findAll=False):
		'''
		Return: result -> list, the value is BS4 object. This function 
				is used by all another function inside this class.
		Parameter:
		tag -> string, html tag to gather.
		[attr] !optional -> string, attribute from a tag. 
		[findAll] !optional -> boolean, the result will be 2D list instead of 1D, 
							   because BS4 will search all tag and attr 
							   that meet the criteria, not the first match.
		Example:
		>>> search_spider = GSearch('study from home')
		>>> print(search_spider.get_main('a')) # you got <a> tag
		'''

		res = []
		for page_num in self.pages:
			page = self.pages[page_num]
			soup = BeautifulSoup(page, 'html.parser')
			texts_parse = soup.findAll('div', {'class': lambda e: len(str(e).split()) == 4})

			for t in texts_parse:
				if attr:
					get_attr = t.findAll(tag, attr) if findAll else t.find(tag, attr)
				else:
					get_attr = t.findAll(tag) if findAll else t.find(tag)

				res.append(get_attr)

		return res


	def get_title(self):
		'''
		Return: title -> list, title of all results.
		Example: 
		>>> search_spider = GSearch('study from home')
		>>> print(search_spider.get_title())
		'''

		if self.titles:
			return self.titles

		titles_tmp = self.get_main('a')

		for res in titles_tmp:
			if res:
				title = res.find('h3')
				if title:
					self.titles.append(title.text)
					continue
			self.titles.append(None)

		return self.titles


	def get_desc(self):
		'''
		Return: description -> list, description of all results.
		Example: 
		>>> search_spider = GSearch('study from home')
		>>> print(search_spider.get_title())
		'''

		if self.descs:
			return self.descs

		descs_tmp = self.get_main('div', {'class': lambda e: len(str(e).split()) == 3}, 
								  findAll=True)

		self.descs.extend([res[2].text if len(res) >= 3 else None for res in descs_tmp])
		return self.descs


	def get_date(self):
		'''
		Return: date -> list, date of result.
		Example: 
		>>> search_spider = GSearch('study from home')
		>>> print(search_spider.get_date())
		'''

		if self.dates:
			return self.dates

		split_sym = '·'
		for desc in self.get_desc():
			date = None
			if split_sym in str(desc):
				date = desc.split(split_sym)[0]

			self.dates.append(date)
		return self.dates


	def get_domainNlink(self, keylink, spec_keylink=''):
		'''
		Return: 
		 domain -> list, domain of all results.
		 link -> list, link of all results.
		Example: 
		>>> search_spider = GSearch('study from home')
		>>> print(search_spider.get_domainNlink())
		'''

		if self.domains and self.links:
			return self.domains, self.links

		dlinks_tmp = self.get_main('a')

		for attr in dlinks_tmp:
			if attr:
				link = attr['href']
				if keylink in link:
					keylink_id = link.index(spec_keylink)
					link = link[keylink_id+3:]
			else:
				self.links.append(None)
				self.domains.append(None)
				continue
				
			domain = re.search(r"(?:^https?:\/\/([^\/]+)(?:[\/,]|$)|^(.*)$)", link)
			self.domains.append(domain.group(1))
			self.links.append(link)
			
		return self.domains, self.links


	def run_some_clean(self):
		'''
		Return: None
		Result: Several variable value got cleaned data.
		'''

		# Remove date from description
		split_sym = '·'
		self.descs = [d.split(split_sym)[1] if split_sym in str(d) else d for d in self.descs]


	def get_all(self):
		'''
		Return: 
		'''

		self.get_title()
		self.get_desc()
		self.get_date()
		self.get_domainNlink('url?q=', '?')

		self.run_some_clean()

		return self.res_to_dict(GSearch.LABELS, self.dates, self.titles, 
								self.descs, self.domains, self.links)
		