import unicodedata
import scrapy
import os
from scripts.Content import Content

def get_file(file):
    file = file.split("/")[-1]
    filename, _ = os.path.splitext(file)
    return filename

class PirateBaySpider(scrapy.Spider):
    page = 1
    keyword = "lynda"
    main_url = "https://piratebay.party/search/"+keyword+"/{}/99/0"
    name = 'pirate_bay'
    allowed_domains = ['piratebay.party']
    start_urls = [main_url.format(page)]

    def parse(self, response):
        table = response.css("table#searchResult tr")
        if len(table) > 1:
            for tr in table:
                tr_class = tr.attrib.get('class')
                if tr_class != "header":
                    row = {}
                    cols = ["type", "title", "uploaded", "magnet", "size", "SE", "LE", "ULed"]
                    for col,td in zip(cols,tr.css("td")):
                        text = td.css("::text").get()
                        if col == "title":
                            title = dict(
                                name=td.css("::text").get(),
                                link=td.css("a::attr(href)").get()
                            )
                            row.update({col:title})
                        elif col == "magnet":
                            icons = td.css("img::attr(src)").getall()
                            magnets = dict(
                                magnet=td.css("a::attr(href)").get(),
                                icons=list(map(get_file,icons))
                            )
                            row.update({col:magnets})
                        elif col in ["uploaded","size"]:
                            text = unicodedata.normalize("NFKC",text)
                            row.update({col:text})
                        else:
                            row.update({col:text})
                        
                        # output the row
                        if len(list(row.keys())) == len(cols):
                            content = Content(row)
                            content.insert()
                            yield row

            # find the next page
            self.page += 1
            yield scrapy.Request(self.main_url.format(self.page),callback=self.parse)