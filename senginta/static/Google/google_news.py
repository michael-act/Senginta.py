from ..search import Search
from .google_search import GSearch
from .settings import GOOGLE_URLS

from bs4 import BeautifulSoup

class GNews(GSearch):
	'''
	GNews is a class to get result from Google News.
	GSearch --> Inherited
	'''

	URL = GOOGLE_URLS['GOOGLE_NEWS']
	LABELS = ['date', 'title', 'description', 'domain', 'link']

	def __init__(self, search_word, start_page=1, max_page=1):
		super().__init__(search_word, start_page, max_page)
		self.start_page_num = (start_page-1) * 10
		self.max_page_num = (max_page-1) * 10
		self.pages = self.get_result(GNews.URL, self.start_page_num, self.max_page_num)

		self.titles = []
		self.descs = []
		self.dates = []
		self.domains = []
		self.links = []


	def get_desc(self):
		'''
		Return: description -> list.
		Example:
		>>> search_news = GNews('events today')
		>>> print(search_news.get_desc())
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
		>>> search_news = GNews('events today')
		>>> print(search_news.get_all())
		'''

		self.get_title()
		self.get_desc()
		self.get_date()
		self.get_domainNlink('url?q=', '?')

		self.run_some_clean()

		return self.res_to_dict(GNews.LABELS, self.dates, self.titles, 
								self.descs, self.domains, self.links)
		