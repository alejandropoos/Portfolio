from scrapy.item import Item, Field
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from scrapy.loader import ItemLoader

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
start_urls = ['https://listado.mercadolibre.com.ar/mates#D[A:mates]']

rules = (
    Rule(
        LinkExtractor(
            allow=(r'/MLA-'),),
            callback='parse_item',
            follow=True),
    Rule(LinkExtractor(
        allow=('_Desde_')),
        follow=True),

)
def parse_item(self, response):
    item = ItemLoader(Articulo(), response)
    item['titulo'] = response.xpath('//h1[@class="ui-pdp-title"]/text()').extract_first()
    item['precio'] = response.xpath('//span[@class="price-tag-fraction"]/text()').extract_first()
    item['descripcion'] = response.xpath('//div[@id="ui-pdp-description__content"]/p/text()').extract_first()
    yield item.load_item()