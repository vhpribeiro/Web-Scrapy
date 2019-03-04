# -*- coding: utf-8 -*-
import scrapy
import json
from noticias.items import NoticiasItem

class FatoOuFakeTodasAsPaginasSpider(scrapy.Spider):
    name = 'FatoOuFakeTodasAsPaginas'
    urlDaPagina = 'https://falkor-cda.bastian.globo.com/tenants/g1/instances/9a0574d8-bc61-4d35-9488-7733f754f881/posts/page/{}'
    paginaAtual = 2
    start_urls = [urlDaPagina.format(paginaAtual)]

    def parse(self, response):
        data = json.loads(response.text)
        for itens in data['items']:
            if "#FAKE" in itens['content']['title'] or "#FATO" in itens['content']['title']:
                if "#FATO ou #FAKE" not in itens['content']['title']:
                    if  "Veja o que" not in itens['content']['title']:
                        link = itens['content']['url']
                        titulo = itens['content']['title'].encode('utf8')
                        chamadaDaMateria = itens['content']['summary']
                        if "#FAKE" in itens['content']['title']:
                            fatoOuFake = 0
                            requisicao = scrapy.Request(url = link, callback = self.parse_da_noticia)
                            requisicao.meta['titulo'] = titulo,
                            requisicao.meta['chamadaDaMateria'] = chamadaDaMateria
                            requisicao.meta['fatoOuFake'] = fatoOuFake

                        if "#FATO" in itens['content']['title']:
                            fatoOuFake = 1
                            requisicao = scrapy.Request(url = link, callback = self.parse_da_noticia)
                            requisicao.meta['titulo'] = titulo,
                            requisicao.meta['chamadaDaMateria'] = chamadaDaMateria
                            requisicao.meta['fatoOuFake'] = fatoOuFake

                    yield requisicao

            mesDaUltimaPublicacaoDoLaco = itens['created'][5:7]
            anoDaUltimaPublicacaoDoLaco = itens['created'][0:4]
        proximaPagina = data['nextPage']
        if mesDaUltimaPublicacaoDoLaco != 2017:
            yield scrapy.Request(url = self.urlDaPagina.format(proximaPagina), callback = self.parse)
        
    def parse_da_noticia(self, response):
        link = response.url
        materiaCompleta = ""
        for article in response.css('p.content-text__container'):
            materiaCompleta = materiaCompleta + str(article.css('p.content-text__container').extract_first().encode("utf-8"))
        
        yield{
            'fatoOuFake': response.meta['fatoOuFake'],
            'titulo': response.meta['titulo'],
            'link': link,
            'chamadaDaMateria': response.meta['chamadaDaMateria'],
            'materiaCompleta': materiaCompleta
        }