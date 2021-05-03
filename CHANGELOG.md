## [0.0.3] - 2021-05-03
### Added
- Implementation of Pandas | to_pd()
- Support special character language, like japan, korean and others
- Add Blog: [Naufal Ardhani](https://www.naufalardhani.com/2021/05/senginta-all-in-one-search-engine.html) 
- to_dict() is relatable for pandas DataFrame
- More comment
- Support multiple language
- Some optimize for BASearch()

### Changed
- Fix key of self.pages dictionary to sync with [start_page_num] parameter
- res_to_json() --> to_json()
- res_to_dict() --> to_dict() Note: Use get_all() for get dictionary result 
  instead of to_dict().