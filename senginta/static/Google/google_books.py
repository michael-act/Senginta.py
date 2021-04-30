from ..search import Search
from .google_search import GSearch
from .settings import GOOGLE_URLS

from bs4 import BeautifulSoup

class GBooks(GSearch):
	URL = GOOGLE_URLS['GOOGLE_BOOKS']
	LABELS = ['title', 'description', 'domain', 'link']

	def __init__(self, search_word, start_page=1, max_page=1):
		super().__init__(search_word, start_page, max_page)
		self.start_page_num = (start_page-1) * 10
		self.max_page_num = (max_page-1) * 10
		self.pages = self.get_result(GBooks.URL, self.start_page_num, self.max_page_num)

		self.titles = []
		self.descs = []
		self.domains = []
		self.links = []


	def get_desc(self):
		'''
		Return: description -> list.
		Example:
		>>> search_book = GBooks('Secret thing to get focus')
		>>> print(search_book.get_desc())
		'''

		if self.descs:
			return self.descs

		descs_tmp = self.get_main('div', {'class': lambda e: len(str(e).split()) == 3}, 
								  findAll=True)

		self.descs.extend([res[3].text if len(res) >= 4 else None for res in descs_tmp])
		return self.descs


	def get_all(self):
		'''
		Return: all attributes -> dict.
		Example:
		>>> search_book = GBooks('Secret thing to get focus')
		>>> print(search_book.get_all())
		'''

		self.get_title()
		self.get_desc()
		self.get_domainNlink('books.google.com')

		return self.res_to_dict(GBooks.LABELS, self.titles, self.descs, 
								self.domains, self.links)
