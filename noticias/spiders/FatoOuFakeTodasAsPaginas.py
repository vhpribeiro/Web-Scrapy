# encoding: utf-8
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
                        titulo = itens['content']['title']
                        chamadaDaMateria = itens['content']['summary']
                        if "#FAKE" in itens['content']['title']:
                            fatoOuFake = 0
                            request = scrapy.Request(url = link, callback = self.parse_da_noticia)
                            request.meta['titulo'] = titulo,
                            request.meta['chamadaDaMateria'] = chamadaDaMateria
                            request.meta['fatoOuFake'] = fatoOuFake
                            yield request

                        if "#FATO" in itens['content']['title']:
                            fatoOuFake = 1
                            request = scrapy.Request(url = link, callback = self.parse_da_noticia)
                            request.meta['titulo'] = titulo,
                            request.meta['chamadaDaMateria'] = chamadaDaMateria
                            request.meta['fatoOuFake'] = fatoOuFake
                            yield request

            mesDaUltimaPublicacaoDoLaco = itens['created'][5:7]
        proximaPagina = data['nextPage']
        if mesDaUltimaPublicacaoDoLaco >= 5:
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