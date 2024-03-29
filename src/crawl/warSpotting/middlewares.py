# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


class WarspottingSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):

        for tank in result:
            if isinstance(tank, dict):
                model = self.get_tank_model(tank["name"])
                tank["t_value"] = model["t_value"]
                tank["model_match"] = model["name"]
                tank["link"] = "https://ukr.warspotting.net" + tank["link"]

            yield tank
        

    def get_tank_model(self, tankName):
        tank_models = [
            {"name": "T-54", "t_value": 54},
            {"name": "T-55", "t_value": 55},
            {"name": "T-62", "t_value": 62},
            {"name": "T-64", "t_value": 64},
            {"name": "T-72", "t_value": 72},
            {"name": "T-80", "t_value": 80},
            {"name": "T-90", "t_value": 90},
            {"name": "T-14", "t_value": 114}
        ]

        bestModel = {"name": "No Match Found", "t_value": 0}
        longestMatch = 0
        for model in tank_models:
            matchedLetters = 0
            for j in range(min(len(tankName), len(model["name"]))):
                if tankName[j].upper() == model["name"][j]:
                    matchedLetters += 1
            if matchedLetters > longestMatch and matchedLetters > 3:
                longestMatch = matchedLetters
                bestModel = model
        return bestModel

    
    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesnt have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class WarspottingDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)
