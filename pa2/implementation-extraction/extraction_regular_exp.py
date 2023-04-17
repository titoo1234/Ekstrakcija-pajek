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
    # print(title)

    subtitle_pattern = r"<div class=\"subtitle\">(.*)<\/div>"
    match = re.compile(subtitle_pattern).search(html)
    subtitle = match.group(1)
    slovar['subtitle'] = subtitle
    # print(subtitle)

    author_pattern = r"<div class=\"author-timestamp\">\s+<strong>(.*)<\/strong>"
    match = re.compile(author_pattern).search(html)
    author = match.group(1)
    slovar['author'] = author
    # print(author)

    publishedTime_pattern = r"<\/strong>\|\s+(.*)\s*<\/div>\s*<div class=\"place-source\">"
    match = re.compile(publishedTime_pattern).search(html)
    publishedTime = match.group(1)
    slovar['publishedTime'] = publishedTime
    # print(publishedTime)

    lead_pattern = r"<p class=\"lead\">(.+)<\/p>"
    match = re.compile(lead_pattern).search(html)
    lead = match.group(1)
    slovar['lead'] = lead
    # print(lead)

    content_pattern = r"<p class=\"Body\">([\s\S]+?)<\/p>"
    # content_pattern = r"(?:(?<=^)|(?<=\W))<article(.*?)(<p.*?>(.+?)<\/p.*?>)+?(.*?)(?=<\/article>)(?:(?=\W)|(?=$))"
    contents = re.finditer(content_pattern, html)
    all_content = ''    
    for content in contents:
        all_content += content.group(1)
    slovar['content'] = all_content

    return slovar
def overstock(html):
    '''
    '''
    title = r"</tbody></table></td><td valign=\"top\">\s*<a.*>\s*<b>(.*)<\/b>"
    # "<td valign=\"top\">\s*<a.*>\s*<b>(.*)<\/b>
    listPrice = r"[\s\S|.]*?<td align=\"left\" nowrap=\"nowrap\">\s*<s>(.*)<\/s>"
    # [\s\S|.]*?<td align=\"left\" nowrap=\"nowrap\">\s*<s>(.*)<\/s>
    price = r"[\s\S|.]*?<span class=\"bigred\">\s*<b>(.*)<\/b>"
    # \s*<\/td>[\s\S|.]*?<span class=\"bigred\">\s*<b>(.*)<\/b>
    saving = r"[\s\S|.]*?<span class=\"littleorange\">([$€]\s*[0-9\.,]+).*"
    # [\s\S|.]*?<span class=\"littleorange\">([$€]\s*[0-9\.,]+)
    savingPercent = r"\((.*?)\)"
    # \((.*)\)<\/span>[\s\S|.]*?
    content = r"[\s\S|.]*?<span class=\"normal\">([\s\S|.]*?)<br>"
    #  <span class=\"normal\">([\s\S|.]*?)<br>"
    regex = title+listPrice+price+saving+savingPercent+content
    slovar = dict()
    counter = 1
    # regex = r"<td valign=\"top\">\s*<a.*>\s*<b>(.*)<\/b>[\s\S|.]*?<td align=\"left\" nowrap=\"nowrap\">\s*<s>(.*)<\/s>\s*<\/td>[\s\S|.]*?<span class=\"bigred\">\s*<b>(.*)<\/b>[\s\S|.]*?<span class=\"littleorange\">([$€]\s*[0-9\.,]+) \((.*)\)<\/span>[\s\S|.]*?<span class=\"normal\">([\s\S|.]*?)<br>"
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
    genre = r'[\s\S]+?<span class="genre">[^A-Z]*(.+?)</span>'
    rating = r'[\s\S]+?<div class="inline-block ratings-imdb-rating" name="ir" data-value="([^>]*?)">'
    content = r'[\s\S]+?<p class="text-muted">[^A-Z]*?\s*([\s\S]*?)</p>'
    slovar =dict()
    counter = 1
    regex = title + year + runtime + genre+ rating +content
    matches = re.finditer(regex, html)
    # print(len(matches))
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
        slovar['item ' + str(counter) ] = item
        counter += 1
        item = dict()
    print(counter)
    return slovar




if __name__ == '__main__':
    path1 = '../input-extraction/WebPages/overstock.com/jewelry01.html'
    path1 = r'C:\Users\Uporabnik\Desktop\IŠRM 1\Ekstrakcija\Ekstrakcija-pajek\pa2\input-extraction\WebPages\overstock.com\jewelry01.html'
    path2 = r'C:\Users\Uporabnik\Desktop\IŠRM 1\Ekstrakcija\Ekstrakcija-pajek\pa2\input-extraction\WebPages\overstock.com\jewelry02.html'
    htmls = [path1,path2]
    path =        r'C:\Users\Uporabnik\Desktop\IŠRM 1\Ekstrakcija\Ekstrakcija-pajek\pa2\input-extraction\WebPages\rtvslo.si\Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html'
    path_amazon = r'C:\Users\Uporabnik\Desktop\IŠRM 1\Ekstrakcija\Ekstrakcija-pajek\pa2\input-extraction\WebPages\imdb.com\imdb1.html'
    
    # path = r'C:\Users\Uporabnik\Desktop\IŠRM 1\Ekstrakcija\Ekstrakcija-pajek\pa2\input-extraction\WebPages\overstock.com\jewelry01.html'
    # with open(path, 'r',encoding='utf-8') as file:
    #     pageContent = file.read()
    # rtv_slo(pageContent)

    pageContent = codecs.open(path_amazon, 'r', encoding='utf-8', errors='ignore').read()
    json_object = json.dumps(imdb(pageContent), indent = 4) 
    # rtv_slo(pageContent)
    print(json_object)

