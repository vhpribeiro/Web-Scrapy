# -*- coding: utf-8 -*-
import scrapy
import json
from noticias.items import NoticiasItem

class G1Fatos(scrapy.Spider):
    name = 'G1Fatos'
    urlDaPagina = 'https://falkor-cda.bastian.globo.com/tenants/g1/instances/1b9deafa-9519-48a2-af13-5db036018bad/posts/page/{}'
    paginaAtual = 2
    start_urls = [urlDaPagina.format(paginaAtual)]

    def parse(self, response):
        data = json.loads(response.text)
        for itens in data['items']:
            fatoOuFake = 1
            link = itens['content']['url']
            titulo = itens['content']['title'].encode('utf8')
            chamadaDaMateria = itens['content']['summary']
            requisicao = scrapy(url = link, callback = self.parse_da_noticia)
            requisicao.meta['titulo'] = titulo,
            requisicao.meta['chamadaDaMateria'] = chamadaDaMateria
            requisicao.meta['fatoOuFake'] = fatoOuFake
            requisicao.meta['link'] = link
            
            yield requisicao

            mesDaUltimaPublicacaoDoLaco = itens['created'][5:7]
            anoDaUltimaPublicacaoDoLaco = itens['created'][0:4]
        proximaPagina = data['nextPage']
        if mesDaUltimaPublicacaoDoLaco != 2017:
            yield scrapy.Request(url = self.urlDaPagina.format(proximaPagina), callback = self.parse)
        
    def parse_da_noticia(self, response):
        materiaCompleta = ""
        for article in response.css('p.content-text__container'):
            materiaCompleta = materiaCompleta + str(article.css('p.content-text__container').get().encode("utf-8"))
        
        yield{
            'fatoOuFake': response.meta['fatoOuFake'],
            'titulo': response.meta['titulo'],
            'link': response.meta['link'],
            'chamadaDaMateria': response.meta['chamadaDaMateria'],
            'materiaCompleta': materiaCompleta
        }