Overview
============================

articleDateExtractor (Article Date Extractor) is a simple open source Python module that automatically detects, extracts and normalizes the publication date of an online article or blog post.
Testing this module against Google news feed resulted in over 90% success rate in detecting and extracting the correct article date.
This module is built and maintained by [Webhose.io](https://webhose.io).

A Quick Example
---------------

```python

    import articleDateExtractor

    date = articleDateExtractor.extractArticlePublishedData("http://edition.cnn.com/2015/11/28/opinions/sutter-cop21-paris-preview-two-degrees/index.html")
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