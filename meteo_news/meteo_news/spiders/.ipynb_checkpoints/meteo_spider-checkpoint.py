import scrapy
import time

class MeteoSpider(scrapy.Spider):
    name = 'MeteoSpider'
    allowed_domains = ['stirileprotv.ro']
    start_urls = ['https://stirileprotv.ro/stiri/vremea']

    custom_settings = {
        'FEEDS': {
            'meteo_news.json': {
                'format': 'json',
                'encoding': 'utf8',
                'overwrite': True
            }
        },
        'USER_AGENT': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36",
        'ROBOTSTXT_OBEY': True,
        'DOWNLOAD_DELAY': 20, # Increasing download delay
        # 'DOWNLOADER_MIDDLEWARES': {
        #    'myproject.middlewares.RandomProxy': 100,  # Middleware to handle proxy rotation, requires more setup
        #    'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 110,
        # },
    }

    def parse(self, response):
        # If we get a 429 error, respect the Retry-After header (if it exists)
        if response.status == 429:
            retry_after = response.headers.get('Retry-After')
            if retry_after:
                sleep_time = int(retry_after)
                self.logger.debug(f"Got a 429 error. Sleeping for {sleep_time} seconds.")
                time.sleep(sleep_time)
                return self.make_request(response.url, callback=self.parse)

        # Extracting the headers of all news articles
        for article in response.xpath('//article[contains(@class, "grid article")]'):
            title = article.xpath('.//div[@class="article-title"]/h2/a/text()').get()
            if title:  # Ensure that a title was successfully extracted
                yield {
                    'article_title': title.strip(),
                }

        # Pagination
        current_page_number = int(response.xpath('//div[@class="pagination"]/ul/li/a[contains(@class, "is-active")]/text()').get())
        next_page_number = current_page_number + 1
        last_page_number = int(response.xpath('//div[@class="pagination"]/ul/li[last()-1]/a/text()').get())

        if next_page_number <= last_page_number:
            next_page_url = f'/stiri/vremea/?page={next_page_number}'
            yield scrapy.Request(response.urljoin(next_page_url), callback=self.parse)
