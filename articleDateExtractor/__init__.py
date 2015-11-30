__author__ = 'Ran Geva'

import sys, urllib2,re, dateparser,json
try:
    from bs4 import BeautifulSoup
except ImportError:
    from BeautifulSoup import BeautifulSoup



# Try to extract from the article URL - simple but might work as a fallback
def _extractFromURL(url):
    date = None

    m = re.search('(\d{4}[/-]\d{2}[/-]\d{2})', url)
    if m:
        return dateparser.parse(m.group(1))


    return  date

def _extractFromLDJson(parsedHTML):
    jsonDate = None
    data = None
    try:
        script = parsedHTML.find('script', type='application/ld+json')
        if script is None:
            return None

        data = json.loads(script.text)
    except Exception, e:
        return

    try:
        jsonDate = dateparser.parse(data['datePublished'])
    except Exception, e:
        pass

    try:
        jsonDate = dateparser.parse(data['dateCreated'])
    except Exception, e:
        pass

    return jsonDate


def _extractFromMeta(parsedHTML):

    metaDate = None
    for meta in parsedHTML.findAll("meta"):
        metaName = meta.get('name', '').lower()
        itemProp = meta.get('itemprop', '').lower()
        httpEquiv = meta.get('http-equiv', '').lower()
        metaProperty = meta.get('property', '').lower()


        #<meta name="pubdate" content="2015-11-26T07:11:02Z" >
        if 'pubdate' == metaName:
            metaDate = meta['content'].strip()
            break


        #<meta name='publishdate' content='201511261006'/>
        if 'publishdate' == metaName:
            metaDate = meta['content'].strip()
            break

        #<meta name="timestamp"  data-type="date" content="2015-11-25 22:40:25" />
        if 'timestamp' == metaName:
            metaDate = meta['content'].strip()
            break

        #<meta name="DC.date.issued" content="2015-11-26">
        if 'dc.date.issued' == metaName:
            metaDate = meta['content'].strip()
            break

        #<meta property="article:published_time"  content="2015-11-25" />
        if 'article:published_time' == metaProperty:
            metaDate = meta['content'].strip()
            break
            #<meta name="Date" content="2015-11-26" />
        if 'date' == metaName:
            metaDate = meta['content'].strip()
            break

        #<meta property="bt:pubDate" content="2015-11-26T00:10:33+00:00">
        if 'bt:pubdate' == metaProperty:
            metaDate = meta['content'].strip()
            break
            #<meta name="sailthru.date" content="2015-11-25T19:56:04+0000" />
        if 'sailthru.date' == metaName:
            metaDate = meta['content'].strip()
            break

        #<meta name="article.published" content="2015-11-26T11:53:00.000Z" />
        if 'article.published' == metaName:
            metaDate = meta['content'].strip()
            break

        #<meta name="published-date" content="2015-11-26T11:53:00.000Z" />
        if 'published-date' == metaName:
            metaDate = meta['content'].strip()
            break

        #<meta name="article.created" content="2015-11-26T11:53:00.000Z" />
        if 'article.created' == metaName:
            metaDate = meta['content'].strip()
            break

        #<meta name="article_date_original" content="Thursday, November 26, 2015,  6:42 AM" />
        if 'article_date_original' == metaName:
            metaDate = meta['content'].strip()
            break

        #<meta name="cXenseParse:recs:publishtime" content="2015-11-26T14:42Z"/>
        if 'cxenseparse:recs:publishtime' == metaName:
            metaDate = meta['content'].strip()
            break

        #<meta name="DATE_PUBLISHED" content="11/24/2015 01:05AM" />
        if 'date_published' == metaName:
            metaDate = meta['content'].strip()
            break


        #<meta itemprop="datePublished" content="2015-11-26T11:53:00.000Z" />
        if 'datepublished' == itemProp:
            metaDate = meta['content'].strip()
            break


        #<meta itemprop="datePublished" content="2015-11-26T11:53:00.000Z" />
        if 'datecreated' == itemProp:
            metaDate = meta['content'].strip()
            break




        #<meta property="og:image" content="http://www.dailytimes.com.pk/digital_images/400/2015-11-26/norway-return-number-of-asylum-seekers-to-pakistan-1448538771-7363.jpg"/>
        if 'og:image' == metaProperty or "image" == itemProp:
            url = meta['content'].strip()
            possibleDate = _extractFromURL(url)
            if possibleDate is not None:
                return  possibleDate


        #<meta http-equiv="data" content="10:27:15 AM Thursday, November 26, 2015">
        if 'date' == httpEquiv:
            metaDate = meta['content'].strip()
            break

    if metaDate is not None:
        return dateparser.parse(metaDate)

    return None

def _extractFromHTMLTag(parsedHTML):
    #<time>
    for time in parsedHTML.findAll("time"):
        datetime = time.get('datetime', '')
        if len(datetime) > 0:
            return dateparser.parse(datetime)

        datetime = time.get('class', '')
        if len(datetime) > 0 and datetime[0].lower() == "timestamp":
            return dateparser.parse(time.string)


    tag = parsedHTML.find("span", {"itemprop": "datePublished"})
    if tag is not None:
        dateText = tag.get("content")
        if dateText is None:
            dateText = tag.text
        if dateText is not None:
            return dateparser.parse(dateText)

    #class=
    for tag in parsedHTML.find_all(['span', 'p','div'], class_=re.compile("pubdate|timestamp|article_date|articledate|date",re.IGNORECASE)):
        dateText = tag.string
        if dateText is None:
            dateText = tag.text

        possibleDate = dateparser.parse(dateText)

        if possibleDate is not None:
            return  possibleDate



    return None


def extractArticlePublishedDate(articleLink):

    print "Extracting date from " + articleLink

    articleDate = None

    try:
        articleDate = _extractFromURL(articleLink)
        request = urllib2.Request(articleLink)
        # Using a browser user agent, decreases the change of sites blocking this request - just a suggestion
        # request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36')
        html = urllib2.build_opener().open(request).read()
        parsedHTML = BeautifulSoup(html)

        possibleDate = _extractFromLDJson(parsedHTML)
        if possibleDate is None:
            possibleDate = _extractFromMeta(parsedHTML)
        if possibleDate is None:
            possibleDate = _extractFromHTMLTag(parsedHTML)


        articleDate = possibleDate

    except Exception, e:
        print e


    return articleDate



