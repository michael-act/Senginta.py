from time import sleep
import requests
import json
import random

class Search:
	def __init__(self, search_word, start_page=1, max_page=1):
		self.search_word = search_word
		self.start_page = start_page
		self.max_page = max_page

	def lastocc(snt, lst):
		rvs_lst = lst[::-1]
		snt_id = len(lst) - rvs_lst.index(snt) - 1

		return snt_id


	def get_result(self, url, page_num, max_page_num):
		'''
		Return: dict, page number: response of website
		Parameter: search_word -> string
		'''

		num = 1
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


	def res_to_dict(self, label, *data):
		'''
		Return: dict, all attribute in results.
		Parameter: 
		label -> list of string to be label of data.
		data -> list of row data and all attributes needed.
		'''

		self.dict_of_td = []
		for i, (d) in enumerate(zip(*data)):
			row = {'result_id': i}
			row.update({l:d[j] for j, l in enumerate(label)})
			self.dict_of_td.append(row)

		return self.dict_of_td


	def res_to_json(self):
		'''
		Return: json, all attribute in results.
		'''

		self.json_of_td = json.dumps(self.get_all(), indent=2)

		return self.json_of_td

