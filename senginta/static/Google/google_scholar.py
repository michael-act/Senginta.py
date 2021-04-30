from ..search import Search
from .settings import GOOGLE_URLS

from bs4 import BeautifulSoup
import re

class GScholar(Search):
	'''
	GScholar is a class to get result from Google Scholar Search.
	Search --> Inherited.
	'''

	URL = GOOGLE_URLS['GOOGLE_SCHOLAR']
	LABELS = ['year', 'title', 'description', 'authors', 'link', 
			  'pdf_link', 'journal_domain', 'domain', 'many_version']

	def __init__(self, search_word, start_page=1, max_page=1):
		super().__init__(search_word, start_page, max_page)
		self.start_page_num = (start_page-1) * 10
		self.max_page_num = (max_page-1) * 10
		self.pages = self.get_result(GScholar.URL, self.start_page_num, self.max_page_num)

		self.years = []
		self.titles = []
		self.descs = []
		self.authors = []
		self.links = []
		self.pdf_links = []
		self.journal_domains = []
		self.domains = []
		self.many_versions = []


	def get_main(self, tag, attr, findAll=False):
		'''
		Return: result -> list, the value is BS4 object. This function 
				is used by all another function inside this class.
		Parameter:
		tag -> string, html tag to gather.
		attr -> string, attribute from a tag. 
		[findAll] !optional -> boolean, the result will be 2D list instead of 1D, 
							   because BS4 will search all tag and attr 
							   that meet the criteria, not the first match.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_main('h3', {'class': 'gs_rt'})) # you get title
		'''

		res = []
		for page_num in self.pages:
			page = self.pages[page_num]
			soup = BeautifulSoup(page, 'html.parser')
			texts_parse = soup.findAll('div', {'class': 'gs_r gs_or gs_scl'})

			for t in texts_parse:
				get_attr = t.findAll(tag, attr) if findAll else t.find(tag, attr)

				if get_attr:
					res.append(get_attr)
				else:
					res.append(None)

		return res


	def get_year(self):
		'''
		Return: year -> list, year of result.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_year())
		'''

		if self.years:
			return self.years

		dates_tmp = self.get_main('div', {'class': 'gs_a'})
		for d in dates_tmp:
			d = d.text
			pattern = r"\d{4}"
			found_year = re.search(pattern, str(d))
			if found_year:
				self.years.append(found_year.group(0))
			else:
				self.years.append(None)

		return self.years


	def get_title(self):
		'''
		Return: title -> list, title of result.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_title())
		'''

		if self.titles:
			return self.titles

		res = [res.text for res in self.get_main('h3', {'class': 'gs_rt'})]
		self.titles.extend(res)
		return self.titles


	def get_desc(self):
		'''
		Return: description -> list, description of result.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_desc())
		'''

		if self.descs:
			return self.descs

		res = [res.text for res in self.get_main('div', {'class': 'gs_rs'})]
		self.descs.extend(res)
		return self.descs


	def get_author(self):
		'''
		Return: author -> list, author of result.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_author())
		'''

		if self.authors:
			return self.authors

		split_sym = '-'
		dates_tmp = self.get_main('div', {'class': 'gs_a'})
		for d in dates_tmp:
			d = d.text
			if split_sym in d:
				id_split_sym = d.index(split_sym)
				self.authors.append(d[:id_split_sym-1])
			else:
				self.authors.append(None)

		return self.authors


	def get_link(self):
		'''
		Return: link -> list, link of result.
		Example:
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_link())
		'''

		if self.links:
			return self.links

		res = [res.find('a')['href'] for res in self.get_main('h3', {'class': 'gs_rt'})]
		self.links.extend(res)

		return self.links


	def get_pdflink(self):
		'''
		Return: pdflink -> list, if the result have pdf, then the 
						   element must not be None.
		Example: 
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_pdflink())
		'''

		if self.pdf_links:
			return self.pdf_links

		self.pdf_links = [res.find('a')['href'] 
						 if res 
						 else None 
						 for res in self.get_main('div', {'class': 'gs_or_ggsm'})]

		return self.pdf_links


	def get_journal_domain(self):
		'''
		Return: journal_domain -> list, domain or subdomain that used 
								  for online publication.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_journal_domain())
		'''

		if self.journal_domains:
			return self.journal_domains

		split_sym = '-'
		journal_dom_tmp = self.get_main('div', {'class': 'gs_a'})
		for j in journal_dom_tmp:
			j = j.text
			pattern = r"([a-z0-9][a-z0-9\-]{0,61}[a-z0-9]\.)+[a-z0-9][a-z0-9\-]*[a-z0-9]"
			found_domain = re.search(pattern, str(j))
			if found_domain:
				self.journal_domains.append(found_domain.group(0))
			else:
				self.journal_domains.append(None)

		return self.journal_domains


	def get_domain(self):
		'''
		Return: domain -> list, domain or subdomain that extracted from link.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_domain())
		'''

		if self.domains:
			return self.domains

		subdomains = self.get_journal_domain()
		for s in subdomains:
			found_domain = re.search(r"(\w{2,}\.\w{2,3}\.\w{2,3}|\w{2,}\.\w{2,3})$", str(s))
			if found_domain:
				self.domains.append(found_domain.group(1))
			else:
				self.domains.append(None)

		return self.domains


	def get_many_version(self):
		'''
		Return: many of version -> list, available version of result.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_many_version())
		'''

		if self.many_versions:
			return self.many_versions

		self.many_versions = [res[-1].text
							  if res 
							  else None 
							  for res in self.get_main('a', {'class': 'gs_nph'}, findAll=True)]

		return self.many_versions


	def get_all(self):
		'''
		Return: all attributes of result -> dict.
		Example:
		>>> search_thesis = GScholar('informatics and technology thesis')
		>>> print(search_thesis.get_all())
		'''

		years = self.get_year()
		titles = self.get_title()
		descs = self.get_desc()
		authors = self.get_author()
		links = self.get_link()
		pdf_links = self.get_pdflink()
		journal_domains = self.get_journal_domain()
		domains = self.get_domain()
		many_versions = self.get_many_version()

		return self.res_to_dict(GScholar.LABELS, years, titles, descs, authors, 
								links, pdf_links, journal_domains, domains, many_versions)

