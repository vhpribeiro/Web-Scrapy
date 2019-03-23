# -*- coding: utf-8 -*-
import scrapy
import sys

reload(sys)

sys.setdefaultencoding("utf-8")

class UolconfereSpider(scrapy.Spider):
    name = 'UolConfere'
    start_urls = ['https://noticias.uol.com.br/confere/']

    def parse(self, response):
        for article in response.css('div.thumbnail-standard-wrapper a'):
            link = article.css("a::attr(href)").get()
            titulo = article.css("h3.thumb-title::text").get()
            chamadaDaMateria = article.css("p.thumb-description::text").get()
            fatoOuFake = 0
            data = article.css("time.thumb-time::text").get()
            palavrasChave = ['não disse', 'nao falou', 'mentira', 'falso', 'falsas', 'fake', 'mentiras', 'mentira']
            if any(palavra in titulo for palavra in palavrasChave):
                request = scrapy.Request(url = link, callback = self.parse_da_noticia)
                request.meta['titulo'] = titulo,
                request.meta['chamadaDaMateria'] = chamadaDaMateria
                request.meta['fatoOuFake'] = fatoOuFake
                yield request

        numeroQueIndicamQualAProximaPagina = response.css('button.btn-search::attr(data-next)').get()
        linkParaProximaPagina = 'https://noticias.uol.com.br/confere/?next=' + str(numeroQueIndicamQualAProximaPagina)
        yield scrapy.Request(url = linkParaProximaPagina, callback=self.parse)
    
    def parse_da_noticia(self, response):
        link = response.url
        materiaCompleta = response.css('div.text').get()
        yield{
            'fatoOuFake': response.meta['fatoOuFake'],
            'titulo': response.meta['titulo'],
            'link': link,
            'chamadaDaMateria': response.meta['chamadaDaMateria'],
            'materiaCompleta': materiaCompleta
        }