from .google_search import GSearch
from .settings import GOOGLE_URLS

from bs4 import BeautifulSoup
import re

class GVideo(GSearch):
	'''
	GVideo is a class to gather result from Google Video Search (Not Youtube).
	GSearch --> Inherited.
	'''

	URL = GOOGLE_URLS['GOOGLE_VIDEO']
	LABELS = ['date', 'title', 'description', 'duration', 'domain', 'link']

	def __init__(self, search_word, start_page=1, max_page=1):
		super().__init__(search_word, start_page, max_page)
		self.start_page_num = (start_page-1) * 10
		self.max_page_num = (max_page-1) * 10
		self.pages = self.get_result(GVideo.URL, self.start_page_num, self.max_page_num)

		self.descs = []
		self.durs = []


	def get_desc(self):
		'''
		Return: description -> list, description of video.
		Example:
		>>> search_film = GSearch('Trailer: Godzilla vs Kong')
		>>> print(search_film.get_desc())
		'''

		if self.descs:
			return self.descs

		descs_tmp = self.get_main('div', {'class': lambda e: len(str(e).split()) == 3}, 
								  findAll=True)

		self.descs.extend([res[3].text if len(res) >= 4 else None for res in descs_tmp])
		return self.descs


	def get_dur(self):
		'''
		Return: duration -> list, duration of video.
		Example:
		>>> search_film = GSearch('Trailer: Godzilla vs Kong')
		>>> print(search_film.get_dur())
		'''

		if self.durs:
			return self.durs

		for df in self.descs:
			found = re.search(r"([0-9]+)?(:)?([0-5]?[0-9]):([0-5]?[0-9])", df)
			if found:
				self.durs.append(found.group(0))
			else:
				self.durs.append(None)

		return self.durs


	def run_some_clean(self):
		'''
		Return: None
		Result: Several variable value got cleaned data.
		'''

		# Remove duration and date from description
		split_sym = '·'
		junk_sym = '...'
		descs_tmp = []
		for d in self.descs:
			if junk_sym in d:
				d = d[:d.index(junk_sym)]

			if split_sym in d:
				d = d.split(split_sym)[1]

			descs_tmp.append(d)

		self.descs = descs_tmp


	def get_all(self):
		'''
		Return: all attributes of result -> dict.
		Example:
		>>> search_film = GSearch('Trailer: Godzilla vs Kong')
		>>> print(search_film.get_all())
		'''

		self.get_title()
		self.get_desc()
		self.get_date()
		self.get_dur()
		self.get_domainNlink('url?q=', '?')

		self.run_some_clean()

		return self.res_to_dict(GVideo.LABELS, self.dates, self.titles, 
								self.descs, self.durs, self.domains, self.links)
