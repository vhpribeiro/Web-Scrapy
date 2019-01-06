# -*- coding: utf-8 -*-
import scrapy

class LupaFakeNewsSpider(scrapy.Spider):
    name = 'LupaFakeNews'
    start_urls = ['https://piaui.folha.uol.com.br/lupa/']

    def parse(self, response):
        for article in response.css("div.bloco div.inner"):
            link = article.css("h2.bloco-title a::attr(href)").extract_first()
            chamada = article.css("h3.bloco-chamada a::text").extract_first()
            request = scrapy.Request(url = link, callback = self.parse_da_noticia)
            request.meta['chamada'] = chamada
            yield request

        proximaPagina = response.css("a.btnvermais::attr(href)").extract_first()
        paginaAtual = proximaPagina[len(proximaPagina) - 2]
        if int(paginaAtual) <= 20:
            yield scrapy.Request(url = proximaPagina, callback=self.parse, dont_filter=True)
    
    def parse_da_noticia(self, response):
        link = response.url
        titulo = response.css("h2.bloco-title::text").extract_first()
        materiaCompleta = response.css("div.post-inner").extract_first()
        verificaSeEhFatoOuFake = response.css("div.etiqueta::text").extract_first()
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

