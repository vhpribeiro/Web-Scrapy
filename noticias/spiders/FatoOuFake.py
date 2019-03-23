#encoding: utf-8
import scrapy
from noticias.items import NoticiasItem

class FatoOuFakeSpider(scrapy.Spider):
    name = 'FatoOuFake'
    start_urls = ['https://g1.globo.com/fato-ou-fake/']

    def parse(self, response):
        for article in response.css("div.feed-post-body"):
            link = article.css("div.feed-post-body-title div div a::attr(href)").get()
            titulo = article.css("div.feed-post-body-title div div a::text").get()
            chamadaDaMateria = article.css("div.feed-post-body-resumo div::text").get()

            if "#FAKE" in titulo or "#FATO" in titulo:
                if "#FATO ou #FAKE" not in titulo:
                    if  "Veja o que" not in titulo:
                        if "#FAKE" in titulo:
                            fatoOuFake = 0
                            request = scrapy.Request(url = link, callback = self.parse_da_noticia)
                            request.meta['titulo'] = titulo.encode("utf-8")
                            request.meta['chamadaDaMateria'] = chamadaDaMateria
                            request.meta['fatoOuFake'] = fatoOuFake

                        if "#FATO" in titulo:
                            fatoOuFake = 1
                            request = scrapy.Request(url = link, callback = self.parse_da_noticia)
                            request.meta['titulo'] = titulo
                            request.meta['chamadaDaMateria'] = chamadaDaMateria
                            request.meta['fatoOuFake'] = fatoOuFake
                            
            yield request
            
    def parse_da_noticia(self, response):
        link = response.url
        materiaCompleta = ""
        for article in response.css('p.content-text__container'):
            materiaCompleta = materiaCompleta + str(article.css('p.content-text__container').get().encode("utf-8"))
        
        yield{
            'fatoOuFake': response.meta['fatoOuFake'],
            'titulo': response.meta['titulo'],
            'link': link,
            'chamadaDaMateria': response.meta['chamadaDaMateria'],
            'materiaCompleta': materiaCompleta
        }