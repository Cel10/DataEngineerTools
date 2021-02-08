import scrapy
from scrapy import Request
from ..items import ImdbcrawlerItem

class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ['www.imdb.com']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_1000&ref_=adv_prv', 
                  'https://www.imdb.com/search/title/?groups=top_1000&start=51&ref_=adv_prv',
                  'https://www.imdb.com/search/title/?groups=top_1000&start=101&ref_=adv_nxt',
                  'https://www.imdb.com/search/title/?groups=top_1000&start=151&ref_=adv_nxt'
    ]

    def clean_spaces(self, string):
        if string:
            return " ".join(string.split())

    def parse(self, response):
        
        all_links = {
            name:response.urljoin(url) for name, url in zip(
            response.xpath("//h3[starts-with(@class, 'lister-item-header')]/a/text()").extract(),
            response.xpath("//h3[starts-with(@class, 'lister-item-header')]/a/@href").extract())
        }
        for link in all_links.values():
            yield Request(link, callback=self.movies)
            print(link)

    def movies(self, response):
          
        title = self.clean_spaces(response.xpath("//div[contains(@class, 'title_wrapper')]/h1/text()").extract_first())        
        image = response.xpath("//div[starts-with(@class, 'poster')]/a/img/@src").extract_first()
        year = self.clean_spaces(response.xpath(".//span[starts-with(@id, 'titleYear')]/a/text()").extract_first())
        note = response.xpath(".//div[contains(@class, 'ratingValue')]/strong/span/text()").get()
        metascore = self.clean_spaces(response.xpath(".//div[contains(@class,'metacriticScore score_favorable ')]/span/text()").get())
        time = self.clean_spaces(response.xpath(".//div[contains(@class,'subtext')]/time/text()").get())
        genres = response.xpath(".//div[contains(@class,'see-more inline canwrap')]/a/text()").extract()
        
        index = []
        for i in range(len(genres)):
            if (genres[i] == ' '):
                index.append(i)
            genres[i] = self.clean_spaces(genres[i])
            
        del genres[index[0]:index[-1]+1]
        
        directors = response.xpath("//div[contains(@class, 'credit_summary_item')][1]/a/text()").extract()
        characters = response.xpath("//td[contains(@class, 'character')]/a/text()").extract()
        actors = response.xpath("//tr[contains(@class, 'odd') or contains(@class, 'even')]/td[2]/a/text()").extract()
        synopsis = response.xpath("//div[@class='summary_text']/text()").extract()
        
        rang = response.xpath("//div[@class='titleReviewBarSubItem']/div/span[@class = 'subText']/text()").extract()
            
        yield ImdbcrawlerItem(
            classement = 'Top 1000',
            title = title,
            image = image,
            year = year,
            synopsis = synopsis,
            note = note,
            metascore = metascore,
            time = time,
            genres = genres,
            directors = directors,
            actors = actors,
            characters = characters,
            rang = rang
            #link = response            
            )    
            