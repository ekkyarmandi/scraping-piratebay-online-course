import scrapy


class PirateBaySpider(scrapy.Spider):
    name = 'pirate_bay'
    allowed_domains = ['piratebay.party']
    start_urls = ['https://piratebay.party/search/udemy/1/99/0']

    def parse(self, response):
        table = response.css("table#searchResult tr")
        for tr in table:
            tr_class = tr.attrib.get('class')
            if tr_class != "header":
                columns = [
                    "type",
                    "title",
                    "uploaded",
                    "magnet",
                    "size",
                    "SE",
                    "LE",
                    "ULed"
                ]
                row = {}
                for col,td in zip(columns,tr.css("td")):
                    if col == "title":
                        title = dict(
                            name=td.css("::text").get(),
                            link=td.css("a::attr(href)").get()
                        )
                        row.update(title)
                    elif col == "magnet":
                        magnets = dict(
                            magnet=td.css("a::attr(href)").get(),
                            icons=td.css("img").getall()
                        )
                        row.update({col:magnets})
                    else:
                        row.update({col:td.css("::text").get()})
                yield row
