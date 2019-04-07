# -*- coding: utf-8 -*-
import scrapy


class AosfatosSpider(scrapy.Spider):
    name = 'AosFatos'
    linkInicial = 'https://aosfatos.org/noticias/checamos/verdadeiro/'
    start_urls = [linkInicial]
    inicioDoLinkDaMateria = 'https://aosfatos.org/'

    def parse(self, response):
        for artigo in response.css("a.card"):
            link = self.inicioDoLinkDaMateria + artigo.css("a.card::attr(href)").get().encode("utf-8")
            titulo = artigo.css("div div div.card-title h2::text").get().encode("utf-8")

            requisicao = scrapy.Request(url = link, callback = self.parse_da_noticia)
            requisicao.meta['titulo'] = titulo
            requisicao.meta['link'] = link
            yield requisicao
        
        paginaAnteriorEProxima = response.css("section.container div.pagination a::attr(href)").getall()
        proximaPagina = paginaAnteriorEProxima[-1]
        linkDaProximaPagina = self.linkInicial + proximaPagina
        yield scrapy.Request(url = linkDaProximaPagina, callback=self.parse, dont_filter=True)

    def parse_da_noticia(self, response):
        paragrafos = str(response.css("section.container article").getall())
        paragrafosEncodificados = [x.encode("utf-8") for x in paragrafos]
        materiaCompleta = ''.join(paragrafosEncodificados)
        ehFato = 1

        yield {
            'fatoOuFake': ehFato,
            'titulo': response.meta['titulo'],
            'link': response.meta['link'],
            'chamadaDaMateria': response.meta['titulo'],
            'materiaCompleta': materiaCompleta
        }

