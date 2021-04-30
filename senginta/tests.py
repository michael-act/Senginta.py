#####################################################################################
# If you use this module as installed with pip, use import method as below.
#from Senginta.static.Google import GSearch, GNews, GBooks, GShop, GVideo, GScholar
#from Senginta.static.Baidu import BASearch
# ------------------------------------ OR
#from Senginta.static import Google, Baidu
# ------------------------------------
#####################################################################################


from static.Google import GSearch, GNews, GBooks, GShop, GVideo, GScholar
from static.Baidu import BASearch


# GoogleSearch = GSearch('Tokopedia')
# print(GoogleSearch.res_to_json())

# GoogleBooks = GBooks('Python Programming', 1, 3)
# print(GoogleBooks.res_to_json())

# GoogleNews = GNews('Idcloudhost', 1, 3) 
# print(GoogleNews.res_to_json())

# GoogleShops = GShop('Remote TV', 1, 3)
# print(GoogleShops.res_to_json())

# GoogleVideo = GVideo('Pegipegi', 1, 3)
# print(GoogleVideo.res_to_json())

# BaiduSearch = BASearch('Gojek', 1, 3)
# print(BaiduSearch.res_to_json())


###################################################################################
# If when you use Google Scrapper is not give anything, you must try
# manual search with format https://scholar.google.com/scholar?q=KEYWORD&start=0
# and pass the bot manually.
# Usually you got the additional parameter, paste that additional parameter 
# into below.
#GScholar.URL += "ANOTHER_PARAMETER_TO_PASS_BOT_PROTECTOR"
###################################################################################

# GoogleScholar = GScholar('Penggunaan Naive Bayes Classifier')
# print(GoogleScholar.res_to_json())