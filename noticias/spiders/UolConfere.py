# -*- coding: utf-8 -*-
import scrapy


class UolconfereSpider(scrapy.Spider):
    name = 'UolConfere'
    start_urls = ['https://noticias.uol.com.br/confere/']

    def parse(self, response):
        for article in response.css('div.thumbnail-standard-wrapper a'):
            link = article.css("a::attr(href)").extract_first()
            titulo = article.css("h3.thumb-title::text").extract_first()
            chamadaDaMateria = article.css("p.thumb-description::text").extract_first()
            fatoOuFake = 0
            data = article.css("time.thumb-time::text").extract_first()
            palavrasChave = ['nao disse', 'nao falou', 'mentira', 'falso', 'falsas', 'fake', 'mentiras', 'mentira', 'bolsonaro', 'jair', 'lula', 'haddad',
             'manuela', 'marina', 'guilherme boulos', 'boulos', 'ciro', 'alckimin', 'urnas', 'urna', 'eleicao', 'eleicoes', 'fraude', 'pt', 'psl', 'pcdob', 'pmdb']
            if any(palavra in titulo for palavra in palavrasChave):
                yield {
                    'fatoOuFake': fatoOuFake,
                    'titulo': titulo,
                    'link': link,
                    'chamadaDaMateria': chamadaDaMateria
                }
        if (int(data[3:5]) > 4):
            numeroQueIndicamQualAProximaPagina = response.css('button.btn-search::attr(data-next)').extract_first()
            linkParaProximaPagina = 'https://noticias.uol.com.br/confere/?next=' + numeroQueIndicamQualAProximaPagina
            yield scrapy.Request(url = linkParaProximaPagina, callback=self.parse)