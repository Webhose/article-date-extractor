Article Date Extractor
============================

A simple Python module to automatically detect, extract and normalizes an online article or blog post publication date.

```python

    import articleDateExtractor

    articleDateExtractor.extractArticlePublishedData("http://edition.cnn.com/2015/11/28/opinions/sutter-cop21-paris-preview-two-degrees/index.html")
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