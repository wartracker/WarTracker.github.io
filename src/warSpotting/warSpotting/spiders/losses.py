import scrapy


class LossesSpider(scrapy.Spider):
    name = "Losses"
    start_urls = [
        "https://ukr.warspotting.net/search/?belligerent=2&weapon=1&page=1",
    ]

    def parse(self, response):
        for vehicle in response.css("#vehicleList tbody tr"):
            yield {
                "name": vehicle.css("a.vehicle-link::text").get(),
                "date": vehicle.css("a.d-none.d-lg-inline.link-secondary::text").get(),
                "type": vehicle.css("span.d-none.d-lg-block.weapon").attrib["title"],
                "link": vehicle.css("a.vehicle-link").attrib["href"]
            }

        next_page = response.css('li.page-item a.page-link.bi.bi-arrow-right::attr(href)').get()
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)