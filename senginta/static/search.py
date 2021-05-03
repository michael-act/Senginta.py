from time import sleep
import requests
import json
import random
import pandas as pd

class Search:
	def __init__(self, search_word, start_page=1, max_page=1):
		self.search_word = search_word
		self.start_page = start_page
		self.max_page = max_page

		self.sleep = []
		self.dict_of_td = {}
		self.dataframe = None
		self.json_of_td = []

	def lastocc(snt, lst):
		'''
		Return: int, Last occurence id of specific element value.
		Parameter: 
		snt -> element value to get index.
		lst -> iterable.
		Example:
		>>> data = ['study', 'from', 'home', 'study', 'from', 'school']
		>>> Search.lastocc('from', data)
		4
		'''

		rvs_lst = lst[::-1]
		snt_id = len(lst) - rvs_lst.index(snt) - 1

		return snt_id


	def get_result(self, url, page_num, max_page_num):
		'''
		Return: dict, page number: response of website. Used by Internal Function.
		Parameter: 
		url -> string, url to get response
		page_num -> int, page number of Search Engine to starting get response.
		max_page_num -> int, maximum page number of of Search Engine to stop get response.
		'''

		num = self.start_page
		result = {}
		self.sleep = []
		while page_num <= max_page_num:
			search_url = url.format(self.search_word, page_num)
			page = requests.get(search_url)
			result.update({num: page.content})
			page_num += 10
			num += 1

			time_wait = random.uniform(1, 2)
			self.sleep.append(time_wait)
			sleep(time_wait)

		return result


	def to_dict(self, label, *data):
		'''
		Return: dict, {label1: data1, label2: data2, ..., labeln: datan} 
				all attribute in results. Used by get_all() function. If
				you want to get dictionary result, use get_all() instead
				of to_dict().
		Parameter: 
		label -> list of string to be label of data.
		data -> list of row data and all attributes needed.
		'''

		if self.dict_of_td:
			return self.dict_of_td

		for i in range(len(label)):
			self.dict_of_td.update({label[i]: data[i]})
			print(label[i], len(data[i]))
		return self.dict_of_td


	def to_pd(self):
		'''
		Return: dataframe, all column and row based on attributes.
		Example:
		>>> search_news = GNews('events today')
		>>> print(search_news.to_pd())
		'''

		if self.dataframe:
			return self.dataframe

		self.dataframe = pd.DataFrame(self.get_all())
		return self.dataframe


	def to_json(self):
		'''
		Return: json, all attribute in results.
		Example:
		>>> search_news = GNews('events today')
		>>> print(search_news.to_json())
		'''

		if self.json_of_td:
			return self.json_of_td

		result = self.to_pd().to_json(orient='index')
		parsed = json.loads(result)
		self.json_of_td = json.dumps(parsed, indent=4, ensure_ascii=False)
		return self.json_of_td

