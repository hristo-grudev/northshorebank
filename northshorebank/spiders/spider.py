import scrapy

from scrapy.loader import ItemLoader

from ..items import NorthshorebankItem
from itemloaders.processors import TakeFirst


class NorthshorebankSpider(scrapy.Spider):
	name = 'northshorebank'
	start_urls = ['https://www.northshorebank.com/about-us/press-releases.aspx']

	def parse(self, response):
		post_links = response.xpath('//a[@aria-label="View the full post."]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1/text()').get()
		description = response.xpath('//div[@id="BlogContentContainer"]//text()[normalize-space()]|//h2//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@id="ContentContainer"]/em/text()').get()

		item = ItemLoader(item=NorthshorebankItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
