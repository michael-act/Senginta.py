<p align="center">
    <img src="Senginta.jpg"></img>
</p>

<p align="center">
    All in one Search Engine Scrapper for used by API or Python Module.
</p>

<p align="center">
    <a href="https://youtu.be/-B3CO467Kzo"> How to use: Video</a>
</p>

**`Documentation`** |
------------------- |
[![Documentation](https://img.shields.io/badge/api-reference-blue.svg)]() |

Senginta is All in one Search Engine Scrapper. With traditional scrapping, 
Senginta can be powerful to get result from any Search Engine, and convert
to Json. Now support only for Google Product Search Engine (GShop, GVideo 
and many too) and Baidu Search Engine.

Senginta was originally developed by me alone. So, if you want to contribute for
support another search engine, let's fork this Repository. 

Senginta provides beta Python.

## Install

```
$ pip install senginta
```

To update senginta to the latest version, add `--upgrade` flag to the above
commands.

#### Try your first Senginta program

```shell
$ python
```

```python
>>> from senginta.static.Google import GSearch
>>> search_spider = GSearch('study from home')
>>> print(search_spider.res_to_json())
...
...
...
Json Formatting
>>> search_spider.get_all()
...
...
...
Dictionary
```

## Resources

*   Let's contribute your blog about this module here!

## License

[MIT License](LICENSE)
