from ..search import Search
from .settings import BAIDU_URLS

from bs4 import BeautifulSoup
import re

class BASearch(Search):
	'''
	BASearch is a class to gather result from Baidu Search Engine.
	Search -> Inherited.
	'''

	URL = BAIDU_URLS['BAIDU_SEARCH']
	LABELS = ['title', 'description', 'author', 'author_link', 'domain', 'link']

	def __init__(self, search_word, start_page=1, max_page=1):
		super().__init__(search_word, start_page, max_page)
		self.start_page_num = (start_page-1) * 10
		self.max_page_num = (max_page-1) * 10
		self.pages = self.get_result(BASearch.URL, self.start_page_num, self.max_page_num)

		self.titles = []
		self.descs = []
		self.authors = []
		self.authors_link = []
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
		>>> search_wschool = BASearch('when school')
		>>> print(search_wschool.get_main('a')) # you got <a> tag
		'''

		res = []
		for page_num in self.pages:
			page = self.pages[page_num]
			soup = BeautifulSoup(page, 'html.parser')
			texts_parse = soup.findAll('div', 
									   {'class': lambda e: e in ['result-op c-container new-pmd xpath-log', 
									   							 'result c-container new-pmd']
									   							 })

			for t in texts_parse:
				if attr:
					get_attr = t.findAll(tag, attr) if findAll else t.find(tag, attr)
				else:
					get_attr = t.findAll(tag) if findAll else t.find(tag)

				res.append(get_attr)

		return res


	def get_title(self):
		'''
		Return: title -> list, title of result.
		Example: 
		>>> search_wschool = BASearch('when school')
		>>> print(search_wschool.get_title())
		'''

		if self.titles:
			return self.titles

		res = [res.text 
			   if res 
			   else None 
			   for res in self.get_main('h3')]
		self.titles.extend(res)
		return self.titles


	def get_desc(self):
		'''
		Return: description -> list, description of result.
		Example:
		>>> search_wschool = BASearch('when school')
		>>> print(search_wschool.get_desc())
		'''

		if self.descs:
			return self.descs

		res = [res.text 
			   if res 
			   else None 
			   for res in self.get_main('div', {'class': lambda e: 'c-abstract' in str(e)})]
		self.descs.extend(res)
		return self.descs


	def get_authorNlink(self):
		'''
		Return: 
		 author -> list, author of result.
		 author link -> list, link to see profile of author.
		Example:
		>>> search_wschool = BASearch('when school')
		>>> print(search_wschool.get_authorNlink())
		'''

		if self.authors and self.authors_link:
			return self.authors, self.authors_link

		for res in self.get_main('a', {'class': 'c-gray'}, findAll=True):
			authors_tmp = []
			authors_link_tmp = []

			for author in res:
				if author:
					authors_tmp.append(author.text)
					authors_link_tmp.append(author['href'])
				else:
					authors_tmp.append(None)
					authors_link_tmp.append(None)

			self.authors.append(authors_tmp)
			self.authors_link.append(authors_link_tmp)

		return self.authors, self.authors_link


	def get_domainNlink(self):
		'''
		Return:
		 domain -> list, domain of result link.
		 link -> list, link of result.
		Example:
		>>> search_wschool = BASearch('when school')
		>>> print(search_wschool.get_domainNlink())
		'''

		if self.domains and self.links:
			return self.domains, self.links

		for res in self.get_main('a'):
			if res:
				link = res['href']
				domain = re.search(r"(?:^https?:\/\/([^\/]+)(?:[\/,]|$)|^(.*)$)", link)

				self.domains.append(domain.group(1))
				self.links.append(link)
			else:
				self.domains.append(None)
				self.links.append(None)

		return self.domains, self.links


	def get_all(self):
		'''
		Return: all attributes of result -> dict.
		Example:
		>>> search_wschool = BASearch('when school')
		>>> print(search_wschool.get_all())
		'''
		
		titles = self.get_title()
		descs = self.get_desc()
		authors, authors_link = self.get_authorNlink()
		domains, links = self.get_domainNlink()

		return self.res_to_dict(BASearch.LABELS, titles, descs, 
								authors, authors_link, domains, links)
