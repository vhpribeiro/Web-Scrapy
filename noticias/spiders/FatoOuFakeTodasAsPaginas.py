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
                        if "#FAKE" in itens['content']['title']:
                            yield{
                                'fatoOuFake': 0,
                                'titulo': itens['content']['title'],
                                'link': itens['content']['url'],
                                'chamadaDaMateria': itens['content']['summary']
                            }
                        if "#FATO" in itens['content']['title']:
                            yield{
                                'fatoOuFake': 1,
                                'titulo': itens['content']['title'],
                                'link': itens['content']['url'],
                                'chamadaDaMateria': itens['content']['summary']
                            }
            mesDaUltimaPublicacaoDoLaco = itens['created'][5:7]
        proximaPagina = data['nextPage']
        if mesDaUltimaPublicacaoDoLaco >= 5:
            yield scrapy.Request(url = self.urlDaPagina.format(proximaPagina), callback = self.parse)