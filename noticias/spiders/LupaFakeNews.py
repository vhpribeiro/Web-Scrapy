# -*- coding: utf-8 -*-
import scrapy

class LupaFakeNewsSpider(scrapy.Spider):
    name = 'LupaFakeNews'
    start_urls = ['https://piaui.folha.uol.com.br/lupa/']

    def parse(self, response):
        for article in response.css("div.bloco div.inner"):
            link = article.css("h2.bloco-title a::attr(href)").get()
            chamada = article.css("h3.bloco-chamada a::text").get()
            request = scrapy.Request(url = link, callback = self.parse_da_noticia)
            request.meta['chamada'] = chamada
            yield request

        proximaPagina = response.css("a.btnvermais::attr(href)").get()
        yield scrapy.Request(url = proximaPagina, callback=self.parse, dont_filter=True)
    
    def parse_da_noticia(self, response):
        link = response.url
        titulo = response.css("h2.bloco-title::text").get()
        materiaCompleta = response.css("div.post-inner").get()
        verificaSeEhFatoOuFake = response.css("div.etiqueta::text").get()
        if "F" in verificaSeEhFatoOuFake:
            fatoOuFake = 0
            if "#Verificamos:" in titulo:
                yield {
                    'fatoOuFake': fatoOuFake,
                    'titulo': titulo,
                    'link': link,
                    'chamadaDaMateria': response.meta['chamada'],
                    'materiaCompleta': materiaCompleta
                    
                }
        if "V" in verificaSeEhFatoOuFake:
            fatoOuFake = 1
            if "#Verificamos:" in titulo:
                yield {
                    'fatoOuFake': fatoOuFake,
                    'titulo': titulo,
                    'link': link,
                    'chamadaDaMateria': response.meta['chamada'],
                    'materiaCompleta': materiaCompleta
                }

