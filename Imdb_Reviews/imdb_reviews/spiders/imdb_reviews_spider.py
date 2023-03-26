import scrapy


class ImdbReviewsSpider(scrapy.Spider):
    name = "imdb_reviews"
    allowed_domains = ["imdb.com"]
    start_urls = ["https://www.imdb.com/title/tt0317248/reviews?ref_=tt_urv"]

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'FEEDS': {
            'reviews.csv': {
                'format': 'csv',
                'overwrite': True
            }
        },
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }                 
    def parse(self, response):
        for review in response.css(".review-container"):
            yield {
                "text": review.css(".text::text").get().strip().encode("utf-8"),
            }

        next_page = response.css(".load-more-data").attrib["data-key"]
        if next_page is not None:
            yield response.follow(
                f"https://www.imdb.com/title/tt0317248/reviews/_ajax?ref_=undefined&paginationKey={next_page}",
                self.parse
            )