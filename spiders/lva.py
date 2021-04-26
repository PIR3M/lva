from scrapy import Spider, Request
from scrapy.http import FormRequest

class OldtimerSpider(Spider):
    name = "lva"
    start_urls = (
            'https://www.lva-auto.fr/cote.php?idMarque=MA55&idModele=-1&rechercheType=1',       
                    )
    
    def login(self, response):
        yield FormRequest.from_response('https://www.lva-auto.fr/compte/login',
                                        formdata={  "login[username]": "fricadelles@protonmail.com",
	                                                "login[password]": "amLsUYk3WecEhzJ",
	                                                "send": ""},
                                        callback=self.after_login)
                                        

    def after_login(self, response):
        if response.xpath('//a[text()="Déconnexion"]'):
            self.log('You are logged in')
    
    
    def parse(self, response):
    
        for products in response.css('ul.cote li'):
            yield {
                    'name': products.css('strong a::text').get(),
                    'year': products.css('.pricepad a::text').get(),
                    'max_price': products.css('.cote-max .pricepad::text').get(),
                    'auction_url': products.css('.link-result a::attr(href)').get(),
                
                }
            """ next_item = response.css('.link-result a::attr(href)').getall()
            if next_item is not None:
                next_item = response.urljoin(next_item)
                yield Request(next_item, callback=self.parse_item) """

            next_page = response.css('.nextItem ::attr(href)').get()
            if next_page is not None:
                next_page = response.urljoin(next_page)
                yield Request(next_page, callback=self.parse)
    