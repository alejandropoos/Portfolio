from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader
from scrapy.selector import Selector
from scrapy.loader.processors import MapCompose

class Articulo(Item):
    titulo = Field()
    precio = Field()
    descripcion = Field()

class MercadoLibreCrawler(CrawlSpider):
    name = 'mercadolibre'
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.103 Safari/537.36',
        'CLOSESPIDER_PAGECOUNT': 20
    }
download_delay = 1
allowed_domains = ['mercadolibre.com.ar', 'listado.mercadolibre.com.ar', 'articulo.mercadolibre.com.ar']
start_urls = ['https://listado.mercadolibre.com.ar/mates_NoIndex_True']

rules = (
    Rule(
        LinkExtractor(
            allow=(r'/MLA-'),),
            callback='parse_item',
            follow=True),
    Rule(LinkExtractor(
        allow=('/mates_Desde_')),
        follow=True),

)
def limpiarTexto(self, texto):
    nuevoTexto = texto.replace('\n', '').replace('\t', '').replace('\r', '').strip()
    return nuevoTexto

def parse_item(self, response):
    item = ItemLoader(Articulo(), response)
    item.add_xpath('titulo','//h1[@class="ui-pdp-title"]/text()', MapCompose(self.limpiarTexto))
    item.add_xpath('precio','//span[@class="price-tag-fraction"]/text()', MapCompose(self.limpiarTexto))
    item.add_xpath('descripcion','//div[@id="ui-pdp-description__content"]/p/text()', MapCompose(self.limpiarTexto))
    yield item.load_item()