__author__ = 'Ran Geva'

import re, json
from dateutil.parser import parse
import dateparser
from datetime import datetime
from webhose_metrics import count as metrics_count
import pytz
from logger import Logger

datetime_html_attributes_formats = "pub+|article+|date+|time+|tms+|mod+"

logger_handler = Logger(name="article_date_extractor_logger", path="/var/log/webhose/articleDateExtractor_logs",
                        level="DEBUG").get_logger()

# try except for different urllib under python3 and python2
try:
    import urllib.request as urllib
except ImportError:
    import urllib2 as urllib

try:
    from bs4 import BeautifulSoup, Tag
except ImportError:
    from BeautifulSoup import BeautifulSoup, Tag


def parse_date_by_daetutil(dateString):
    try:
        dateTimeObj = parse(dateString)
        return dateTimeObj
    except Exception as err:
        return None


def parse_date_by_dateparser(dateString):
    try:
        dateTimeObj = dateparser.parse(dateString)
        return dateTimeObj
    except Exception as err:
        return None


def parseStrDate(dateString):
    dateTimeObj = None
    if dateString is not None:
        dateString = dateString.rstrip().lstrip()
        dateTimeObj = parse_date_by_daetutil(dateString)
        if dateTimeObj is None or "":
            dateTimeObj = parse_date_by_dateparser(dateString)
    return dateTimeObj


# Try to extract from the article URL - simple but might work as a fallback
def _extractFromURL(url):
    # Regex by Newspaper3k  - https://github.com/codelucas/newspaper/blob/master/newspaper/urls.py
    m = re.search(
        r'([\./\-_]{0,1}(19|20)\d{2})[\./\-_]{0,1}(([0-3]{0,1}[0-9][\./\-_])|(\w{3,5}[\./\-_]))([0-3]{0,1}[0-9][\./\-]{0,1})?',
        url)
    if m:
        return parseStrDate(m.group(0))

    return None


def _extract_by_tag(tag, parsedHTML, attr):
    for tag_span in parsedHTML.find_all(tag, **{attr: re.compile(datetime_html_attributes_formats, re.IGNORECASE)}):
        dateText = tag_span.string or tag_span.text
        return parseStrDate(dateText)


def _extractFromLDJson(parsedHTML):
    try:
        script = parsedHTML.find('script', type='application/ld+json')
        if script is None:
            logger_handler.debug("ERROR: [_extractFromLDJson] - script none")
            return None
        if len(script.text):
            script_data = json.loads(script.text)
        elif len(script.string):
            script_data = json.loads(script.string)
        if isinstance(script_data, dict):
            script_data = [script_data]
        for data in script_data:
            jsonDate = parseStrDate(data.get('dateCreated', None)) or parseStrDate(data.get('datePublished', None))
            if jsonDate:
                return jsonDate
    except Exception as err:
        logger_handler.debug("ERROR: [_extractFromLDJson] - {err}".format(err=err))

    return None


def _extractFromMeta(parsedHTML):
    metaDate = None
    for meta in parsedHTML.findAll("meta"):
        metaName = meta.get('name', '').lower()
        itemProp = meta.get('itemprop', '').lower()
        httpEquiv = meta.get('http-equiv', '').lower()
        metaProperty = meta.get('property', '').lower()

        # <meta name="pubdate" content="2015-11-26T07:11:02Z" >
        if 'pubdate' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta name='publishdate' content='201511261006'/>
        if 'publishdate' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta name="timestamp"  data-type="date" content="2015-11-25 22:40:25" />
        if 'timestamp' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta name="DC.date.issued" content="2015-11-26">
        if 'dc.date.issued' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta property="article:published_time"  content="2015-11-25" />
        if 'article:published_time' == metaProperty:
            metaDate = meta['content'].strip()
            break
            # <meta name="Date" content="2015-11-26" />
        if 'date' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta property="bt:pubDate" content="2015-11-26T00:10:33+00:00">
        if 'bt:pubdate' == metaProperty:
            metaDate = meta['content'].strip()
            break
            # <meta name="sailthru.date" content="2015-11-25T19:56:04+0000" />
        if 'sailthru.date' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta name="article.published" content="2015-11-26T11:53:00.000Z" />
        if 'article.published' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta name="published-date" content="2015-11-26T11:53:00.000Z" />
        if 'published-date' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta name="article.created" content="2015-11-26T11:53:00.000Z" />
        if 'article.created' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta name="article_date_original" content="Thursday, November 26, 2015,  6:42 AM" />
        if 'article_date_original' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta name="cXenseParse:recs:publishtime" content="2015-11-26T14:42Z"/>
        if 'cxenseparse:recs:publishtime' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta name="DATE_PUBLISHED" content="11/24/2015 01:05AM" />
        if 'date_published' == metaName:
            metaDate = meta['content'].strip()
            break

        # <meta itemprop="datePublished" content="2015-11-26T11:53:00.000Z" />
        if 'datepublished' == itemProp:
            metaDate = meta['content'].strip()
            break

        # <meta itemprop="datePublished" content="2015-11-26T11:53:00.000Z" />
        if 'datecreated' == itemProp:
            metaDate = meta['content'].strip()
            break

        # <meta property="og:image" content="http://www.dailytimes.com.pk/digital_images/400/2015-11-26/norway-return-number-of-asylum-seekers-to-pakistan-1448538771-7363.jpg"/>
        if 'og:image' == metaProperty or "image" == itemProp:
            url = meta['content'].strip()
            possibleDate = _extractFromURL(url)
            if possibleDate is not None:
                return possibleDate

        # <meta http-equiv="data" content="10:27:15 AM Thursday, November 26, 2015">
        if 'date' == httpEquiv:
            metaDate = meta['content'].strip()
            break

        logger_handler.debug(
            "ERROR-INFO- [_extractFromMeta] - not found properties for meta: {metadata}".format(metadata=meta))

    if metaDate is not None:
        return parseStrDate(metaDate)

    logger_handler.debug("ERROR: [_extractFromMeta] - Failed to parse from meta properties")
    return None


def _extractFromHTMLTag(parsedHTML):
    list_of_times_attribute = parsedHTML.findAll("time")
    # <time>
    for time in list_of_times_attribute:
        datetime = time.get('datetime', '')
        if len(datetime) > 0:
            return parseStrDate(datetime)

        datetime = time.get('class', '')
        if len(datetime) > 0:
            # and datetime[0].lower() == "timestamp":
            date_string = time.string or time.text
            return parseStrDate(date_string)

    tag = parsedHTML.find("span", {"itemprop": "datePublished"})
    if tag is not None:
        dateText = tag.get("content")
        if dateText is None:
            dateText = tag.text
        if dateText is not None:
            return parseStrDate(dateText)

    possibleDate = _extract_by_tag(['span', 'p', 'div'], parsedHTML, attr='class_')
    if possibleDate is not None and possibleDate != '':
        return possibleDate

    possibleDate = _extract_by_tag(['span', 'p', 'div', 'li'], parsedHTML, attr='id')
    if possibleDate is not None and possibleDate != '':
        return possibleDate

    logger_handler.debug("ERROR- [_extractFromHTMLTag] - Failed to parse from HTML tags")
    return None


def extractArticlePublishedDate(articleLink, html=None):
    print("Extracting date from " + articleLink)

    articleDate = None

    try:
        articleDate = _extractFromURL(articleLink)

        if html is None:
            html = _get_html_response(articleLink)

        parsedHTML = BeautifulSoup(html, "lxml")

        possibleDate = _extractFromLDJson(parsedHTML)
        if possibleDate is None:
            possibleDate = _extractFromMeta(parsedHTML)
        if possibleDate is None:
            possibleDate = _extractFromHTMLTag(parsedHTML)

        articleDate = possibleDate

    except Exception as e:
        logger_handler.debug(
            "ERROR-INFO- [extractArticlePublishedDate] - Exception for {link}".format(link=articleLink))
        print("Exception in extractArticlePublishedDate for " + articleLink)
        print(e.args)

    return articleDate


def _get_html_response(url):
    """
    simple request execution
    :param url: string of url
    :return: html response
    """
    request = urllib.Request(url)
    html = urllib.build_opener().open(request).read()
    logger_handler.info("Request - {url}".format(url=url))
    return html


def get_relevant_date(url, html=None):
    """
    retrieves the most relevant published date for an article
    :param url: string of url
    :param html: string of html response (to avoid request execution)
    :return: oldest date from the following options:
        1) date in the url
        2) headers of the response (json-ld, meta, etc.)
        3) html known tags
    """
    # getting date by input url
    url_base_date = _extractFromURL(url)
    # bs parsing for extended data
    html = html or _get_html_response(url)
    parsed_html = BeautifulSoup(html, "lxml")

    # extended dates (json-ld, html tags, etc.)
    jsonld_base_date = _extractFromLDJson(parsed_html)
    meta_base_date = _extractFromMeta(parsed_html)
    html_tags_base_date = _extractFromHTMLTag(parsed_html)

    possible_dates = [url_base_date, jsonld_base_date, meta_base_date, html_tags_base_date]
    possible_dates = filter(lambda _date: _date is not None and isinstance(_date, datetime), possible_dates)
    possible_dates = [_date.replace(tzinfo=pytz.UTC) for _date in possible_dates]

    metrics_count(
        name="articleDateExtractor_success_total" if len(possible_dates) != 0 else "articleDateExtractor_failed_total",
        value=1)

    if len(possible_dates) == 0:
        logger_handler.info("[get_relevant_date] - None possible dates for {url}".format(url=url))
        return None

    # return oldest date
    return min(possible_dates)


if __name__ == '__main__':
    d = get_relevant_date("https://elegantessence.tumblr.com/post/716279737919602688")
