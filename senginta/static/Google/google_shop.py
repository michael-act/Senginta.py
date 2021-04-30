from ..search import Search
from .settings import GOOGLE_URLS

from bs4 import BeautifulSoup

class GShop(Search):
	'''
	GShop is a class for gather all top product from Google Shop Search.
	Search --> Inherited
	'''

	URL = GOOGLE_URLS['GOOGLE_SHOP']
	LABELS = ['title', 'price', 'e-commerce', 'src-link', 'img-link']

	def __init__(self, search_word, start_page=1, max_page=1):
		super().__init__(search_word, start_page, max_page)
		self.start_page_num = start_page * 10
		self.max_page_num = max_page * 10
		self.pages = self.get_result(GShop.URL, self.start_page_num, self.max_page_num)

		self.titles = []
		self.src_links = []
		self.img_links = []
		self.e_commerces = []
		self.prices = []


	def get_main(self, tag, attr, partial=False):
		'''
		Return: result -> list, the value is BS4 object. This function 
				is used by all another function inside this class.
		Parameter:
		tag -> string, html tag to gather.
		attr -> string, attribute from a tag. 
		[partial] !optional -> boolean, BS4 will match attr parameter 
							   with partial string, not full if True.
		Example:
		>>> search_assistant = GSearch('google assistant home')
		>>> print(search_assistant.get_main('a')) # you got <a> tag
		'''

		texts = []
		for page_num in self.pages:
			page = self.pages[page_num]
			soup = BeautifulSoup(page, 'html.parser')
			texts_parse = soup.findAll(tag, attr, partial=partial)

			attr_need = {'a': 'href', 'img': 'src'}
			if tag in attr_need:
				attr_specific = attr_need[tag]
				texts_ext = [t[attr_specific] for t in texts_parse]
			else:
				texts_ext = [t.text for t in texts_parse]

			texts.extend(texts_ext)

		return texts


	def get_title(self):
		'''
		Return: title -> list, title of product.
		Example: 
		>>> search_assistant = GSearch('google assistant home')
		>>> print(search_assistant.get_title())
		'''

		if self.titles:
			return self.titles

		self.titles.extend(self.get_main('div', {'class': 'sh-np__product-title translate-content'}))
		return self.titles


	def get_price(self):
		'''
		Return: price -> list, price of product.
		Example:
		>>> search_assistant = GSearch('google assistant home')
		>>> print(search_assistant.get_price())
		'''

		if self.prices:
			return self.prices

		price_tmp = self.get_main('b', None)
		self.prices.extend([p for p in price_tmp if 'Rp' in p])
		return self.prices


	def get_ecommerce(self):
		'''
		Return: e-commerce -> list, name of e-commerce platform to sell and buy product.
		Example:
		>>> search_assistant = GSearch('google assistant home')
		>>> print(search_assistant.get_ecommerce())
		'''

		if self.e_commerces:
			return self.e_commerces

		self.e_commerces.extend(self.get_main('div', {'class': 'sh-np__seller-container'}))
		return self.e_commerces


	def get_src_link(self):
		'''
		Return: source link -> list, link of product.
		Example:
		>>> search_assistant = GSearch('google assistant home')
		>>> print(search_assistant.get_src_link())
		'''

		if self.src_links:
			return self.src_links

		self.src_links.extend(self.get_main('a', {'class': 'sh-np__click-target'}))
		return self.src_links


	def get_img_link(self):
		'''
		Return: images link -> list, link of product image.
		Example:
		>>> search_assistant = GSearch('google assistant home')
		>>> print(search_assistant.get_img_link())
		'''

		if self.img_links:
			return self.img_links

		self.img_links.extend(self.get_main('img', {'role': 'presentation'}))
		return self.img_links


	def get_all(self):
		'''
		Return: all attributes of result -> dict.
		Example:
		>>> search_assistant = GSearch('google assistant home')
		>>> print(search_assistant.get_all())
		'''

		self.get_title()
		self.get_price()
		self.get_ecommerce()
		self.get_src_link()
		self.get_img_link()

		return self.res_to_dict(GShop.LABELS, self.titles, self.prices, 
								self.e_commerces, self.src_links, self.img_links)
