#####################################################################################
# If you use this module as installed with pip, use import method as below.
#from senginta.static.Google import GSearch, GNews, GBooks, GShop, GVideo, GScholar
#from senginta.static.Baidu import BASearch
# ------------------------------------ OR
#from senginta.static import Google, Baidu
# ------------------------------------
#####################################################################################


from static.Google import GSearch, GNews, GBooks, GShop, GVideo, GScholar
from static.Baidu import BASearch


# GoogleSearch = GSearch('Tokopedia', 1, 3)
# print(GoogleSearch.to_json())

# GoogleBooks = GBooks('Python Programming', 1, 3)
# print(GoogleBooks.to_json())

# GoogleNews = GNews('Idcloudhost', 1, 3) 
# print(GoogleNews.to_json())

# GoogleShops = GShop('Remote TV', 'Rp', 1, 3)
# print(GoogleShops.to_json())

# GoogleVideo = GVideo('Pegipegi', 1, 3)
# print(GoogleVideo.to_json())

# BaiduSearch = BASearch('Gojek', 1, 3)
# print(BaiduSearch.to_json())


###################################################################################
# If when you use Google Scrapper is not give anything, you must try
# manual search with format https://scholar.google.com/scholar?q=KEYWORD&start=0
# and pass the bot manually.
# Usually you got the additional parameter, paste that additional parameter 
# into below.
#GScholar.URL += "ANOTHER_PARAMETER_TO_PASS_BOT_PROTECTOR"
###################################################################################

# GoogleScholar = GScholar('Penggunaan Naive Bayes Classifier', 1, 3)
# print(GoogleScholar.to_json())
