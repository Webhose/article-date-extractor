[![version][pypi-version]][pypi-url]

[![License][pypi-license]][license-url]
[![Downloads][pypi-downloads]][pypi-url]
[![Gitter][gitter-image]][gitter-url]

About
=====

articleDateExtractor (Article Date Extractor) is a simple open source Python module, built and maintained by [Webhose.io](https://webhose.io), that automatically detects, extracts and normalizes the publication date of an online article or blog post.

## Feature


1.  Extracting the publication date information when it is specified in a web page, with over 90% success rate.


## A Quick Example


```python

    import articleDateExtractor

    d = articleDateExtractor.extractArticlePublishedDate("http://edition.cnn.com/2015/11/28/opinions/sutter-cop21-paris-preview-two-degrees/index.html")

    print (d)

    d = articleDateExtractor.extractArticlePublishedDate("http://techcrunch.com/2015/11/29/tyro-payments/")

    print (d)

```


## Installing

Available through pip:

```bash

    $ pip install articleDateExtractor
```
Alternatively, you can install from source:

```bash

    $ git clone https://github.com/Webhose/article-date-extractor
    $ cd article-date-extractor
    $ python setup.py install
```

## Dependencies

* [beautifulsoup4](http://www.crummy.com/software/BeautifulSoup/bs4/) >= 4.6.0
* [python-dateutil](https://github.com/dateutil/dateutil/) >= 2.4.2


## About Webhose.io


At [Webhose.io](https://webhose.io) we crawl, structure, unify and aggregate data from millions of online sources (news sites, blogs, discussion forums, comments etc..), so the need for a
scalable solution that will automatically extract and structure the unstructured web is critical. We use multiple signals and algorithms to automatically detect where the post text is, the author name, the comments,
and of course the date. With articleDateExtractor (Article Date Extractor) we rely on the many "different types of standards" out there to automatically detect the date (with a success rate of over 90%).




[license-url]: https://github.com/Webhose/article-date-extractor/blob/master/LICENSE

[gitter-url]: https://gitter.im/Webhose
[gitter-image]: https://img.shields.io/badge/Gitter-Join%20Chat-blue.svg?style=flat


[pypi-url]: https://pypi.python.org/pypi/articleDateExtractor
[pypi-license]: https://img.shields.io/pypi/l/articleDateExtractor.svg?style=flat
[pypi-version]: https://img.shields.io/pypi/v/articleDateExtractor.svg?style=flat
[pypi-downloads]: https://img.shields.io/pypi/dm/articleDateExtractor.svg?style=flat
