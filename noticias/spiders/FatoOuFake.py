# -*- coding: utf-8 -*-
import scrapy
from noticias.items import NoticiasItem

class FatoOuFakeSpider(scrapy.Spider):
    name = 'FatoOuFake'
    allowed_domains = ['g1.globo.com/fato-ou-fake']
    start_urls = ['https://g1.globo.com/fato-ou-fake/']

    def parse(self, response):
        for article in response.css("div.feed-post-body"):
            link = article.css("div.feed-post-body-title div div a::attr(href)").extract_first()
            titulo = article.css("div.feed-post-body-title div div a::text").extract_first()
            chamadaDaMateria = article.css("div.feed-post-body-resumo div::text").extract_first()

            if "#FAKE" in titulo or "#FATO" in titulo:
                if "#FATO ou #FAKE" not in titulo:
                    if  "Veja o que" not in titulo:
                        if "#FAKE" in titulo:
                            yield{
                                'fatoOuFake': 0,
                                'titulo': titulo,
                                'link': link,
                                'chamadaDaMateria': chamadaDaMateria
                            }
                        if "#FATO" in titulo:
                            yield{
                                'fatoOuFake': 1,
                                'titulo': titulo,
                                'link': link,
                                'chamadaDaMateria': chamadaDaMateria
                            }
