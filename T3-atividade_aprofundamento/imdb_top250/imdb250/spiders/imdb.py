import scrapy
import csv


def get_summary(link):
    url = link
    resp = requests.get(url)
    soup = BeautifulSoup(resp.content, "html.parser")
    summary = soup.find("div", {"class": "summary_text"}).text.strip()

    return summary

class ImdbSpider(scrapy.Spider):
    name = 'imdb'
    allowed_domains = ["imdb.com"]
    start_urls = ['https://www.imdb.com/chart/top/?ref_=nv_mv_250']

    custom_settings = {
        'LOG_LEVEL': 'DEBUG',
        'FEEDS': {
            'imdb_top250.csv': {
                'format': 'csv',
                'overwrite': True
            }
        },
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, '
                      'like Gecko) Chrome/102.0.0.0 Safari/537.36'
    }
    def parse(self, response):
        for filmes in response.css('.lister-list tr'):
            link_raw = filmes.css(".titleColumn a::attr(href)").get()
            link = f"https://www.imdb.com{link_raw}"
            yield scrapy.Request(link, callback=self.parse_text, cb_kwargs=dict(
                title=filmes.css(".titleColumn a::text").get(),
                year=filmes.css(".titleColumn span::text").re_first("\((.*?)\)"),
                rating=filmes.css(".imdbRating strong::text").get(),
                link= link
            ))


    def parse_text(self, response, title, year, rating, link):

        conteudo = {
            'titulo': title,
            'ano': year,
            'nota': rating,
            'genero': response.xpath('//span[@class="ipc-chip__text"]//text()').get(),
            'diretor': response.xpath('//a[@class="ipc-metadata-list-item__list-content-item '
                                          'ipc-metadata-list-item__list-content-item--link"]//text('
                                         ')').get(),
            'url': link
            }
       # with open('IMDB_top250.csv', 'a', newline='', encoding="utf-8") as output_file:
            #dict_writer = csv.DictWriter(output_file, conteudo.keys())
            #dict_writer.writerows([conteudo])
        yield conteudo
