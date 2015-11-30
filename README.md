About
=====

articleDateExtractor (Article Date Extractor) is a simple open source Python module, built and maintained by [Webhose.io](https://webhose.io), that automatically detects, extracts and normalizes the publication date of an online article or blog post.

Feature
--------

1.  Extracting the publication date information when it is specified in web pages, with over 90% success rate.


A Quick Example
---------------

```python

    import articleDateExtractor

    date = articleDateExtractor.extractArticlePublishedData("http://edition.cnn.com/2015/11/28/opinions/sutter-cop21-paris-preview-two-degrees/index.html")

    print date
```


Installing
----------
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

Dependencies
------------
[BeautifulSoup](http://www.crummy.com/software/BeautifulSoup/) >= 3.2.1
[dateparser](https://github.com/scrapinghub/dateparser) >= 0.3.1


About Webhose.io
----------------

At [Webhose.io](https://webhose.io) we crawl, structure, unify and aggregate data from millions of online sources (news sites, blogs, discussion forums, comments etc..), so the need for a
scalable solution that will automatically extract and structure the unstructured web is critical. We use multiple signals and algorithms to automatically detect where the post text is, the author name, the comments,
and of course the date. With articleDateExtractor (Article Date Extractor) we rely on the many "different types of standards" out there to automatically detect the date (with a success rate of over 90%).





