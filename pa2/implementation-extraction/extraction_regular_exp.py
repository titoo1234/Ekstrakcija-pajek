# FUNKCIJE ZA REGULARNE
# 3 funkcije za vsak par strani
import re
import codecs
import regex
import json
def rtv_slo(html):
    slovar = dict()

    title_pattern = r"<h1>(.*)<\/h1>\s*<div class=\"subtitle\">"
    match = re.compile(title_pattern).search(html)
    title = match.group(1)
    slovar['title'] = title

    subtitle_pattern = r"<div class=\"subtitle\">(.*)<\/div>"
    match = re.compile(subtitle_pattern).search(html)
    subtitle = match.group(1)
    slovar['subtitle'] = subtitle

    author_pattern = r"<div class=\"author-timestamp\">\s+<strong>(.*)<\/strong>"
    match = re.compile(author_pattern).search(html)
    author = match.group(1)
    slovar['author'] = author

    publishedTime_pattern = r"<\/strong>\|\s+(.*?)\s*<\/div>\s*<div class=\"place-source\">"
    match = re.compile(publishedTime_pattern).search(html)
    publishedTime = match.group(1)
    slovar['publishedTime'] = publishedTime

    lead_pattern = r"<p class=\"lead\">(.+)<\/p>"
    match = re.compile(lead_pattern).search(html)
    lead = match.group(1)
    slovar['lead'] = lead


    content_pattern = r'<article class="article">[\s\S]+?<p[^>]*([\s\S]*)<\/p>[\s\S]*<\/article>'
    match = re.compile(content_pattern).search(html)
    content = match.group(1)
    content = re.sub('<br>', '', content)
    content = re.sub('<p>', '', content)
    content = re.sub('</p>', '', content)
    content = re.sub(r'\n', '', content)
    content = re.sub(r'\t', '', content)
    content = re.sub(r'</strong>', '', content)
    content = re.sub(r'<strong>', '', content)
    content = re.sub(r'<p class=\"Body\">', '', content)    
    slovar['content'] = content
    return slovar
def overstock(html):
    '''
    '''
    title = r"</tbody></table></td><td valign=\"top\">\s*<a.*>\s*<b>(.*)<\/b>"
    listPrice = r"[\s\S|.]*?<td align=\"left\" nowrap=\"nowrap\">\s*<s>(.*)<\/s>"
    price = r"[\s\S|.]*?<span class=\"bigred\">\s*<b>(.*)<\/b>"
    saving = r"[\s\S|.]*?<span class=\"littleorange\">([$€]\s*[0-9\.,]+).*"
    savingPercent = r"\((.*?)\)"
    content = r"[\s\S|.]*?<span class=\"normal\">([\s\S|.]*?)<br>"
    regex = title+listPrice+price+saving+savingPercent+content
    slovar = dict()
    counter = 1
    matches = re.finditer(regex, html)
    item = dict()
    for match in matches:
        title = match.group(1)
        item['title'] = title

        listPrice = match.group(2)
        item['listPrice'] = listPrice
        
        price = match.group(3) 
        item['price'] = price

        saving = match.group(4)
        item['saving'] = saving
        
        savingPercent = match.group(5)
        item['savingPercent'] = savingPercent
        
        content = match.group(6)
        item['content'] = content

        slovar['item ' + str(counter) ] = item
        counter += 1
        item = dict()
    return slovar

def imdb(html):
    title = r'<a href=\"\/title[^>]*>(.*?)<\/a>'
    year = r'[^<]*<span class="lister-item-year text-muted unbold">\((.*)\)</span>'
    runtime = r'[\s\S]+?<span class="runtime">(.+)</span>'
    genre = r'[\s\S]+?<span class="genre">[^A-Z]*(.+?)\s{2}'
    rating = r'[\s\S]+?<div class="inline-block ratings-imdb-rating" name="ir" data-value="([^>]*?)">'
    content = r'[\s\S]+?<p class="text-muted">[^A-Z]*?\s*([\s\S]*?)</p>'
    slovar =dict()
    counter = 1
    regex = title + year + runtime + genre+ rating +content
    matches = re.finditer(regex, html)
    item = dict()
    for match in matches:
        title = match.group(1)
        year = match.group(2)
        runtime = match.group(3)
        genre = match.group(4)
        rating = match.group(5)
        content = match.group(6)
        item['title'] = title
        item['year'] = year
        item['runtime'] = runtime
        item['genre'] = genre
        item['rating'] = rating
        item['content'] = content
        slovar['movie ' + str(counter) ] = item
        counter += 1
        item = dict()
    return slovar

def zazeni():
    path1_overstock = r'../input-extraction/WebPages/overstock.com/jewelry01.html'
    path2_overstock = r'../input-extraction/WebPages/overstock.com/jewelry02.html'
    path_imdb1 = r'../input-extraction/WebPages/imdb.com/imdb1.html'
    path_imdb2 = r'../input-extraction/WebPages/imdb.com/imdb2.html'
    path_rtvslo1 = r'../input-extraction/WebPages/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html'
    path_rtvslo2 = r'../input-extraction/WebPages/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljs╠îe v razredu - RTVSLO.si.html'
    
    print("REGULAR EXPRESSION:")
    print("==================================================================")
    print("Overstock.com")
    print("-------------------------------------------")
    pageContent = codecs.open(path1_overstock, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(overstock(pageContent), indent = 4,ensure_ascii=False) 
    print(json_object)
    print("-------------------------------------------")
    pageContent = codecs.open(path2_overstock, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(overstock(pageContent), indent = 4,ensure_ascii=False) 
    print(json_object)
    print("\n\n")

    print("Rtvslo.si")
    print("-------------------------------------------")
    pageContent = codecs.open(path_rtvslo1, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(rtv_slo(pageContent), indent = 4,ensure_ascii=False) 
    print(json_object)
    pageContent = codecs.open(path_rtvslo2, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(rtv_slo(pageContent), indent = 4,ensure_ascii=False) 
    print("-------------------------------------------")
    print(json_object)
    print("\n\n")

    print("Imdb.si")
    print("-------------------------------------------")
    pageContent = codecs.open(path_imdb1, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(imdb(pageContent), indent = 4,ensure_ascii=False) 
    print(json_object)
    pageContent = codecs.open(path_imdb2, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(imdb(pageContent), indent = 4,ensure_ascii=False) 
    print("-------------------------------------------")
    print(json_object)


