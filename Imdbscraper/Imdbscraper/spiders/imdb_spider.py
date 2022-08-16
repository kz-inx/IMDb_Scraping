""" Importing Libraries """
import scrapy
from ..items import ImdbscraperItem
from scrapy.exceptions import IgnoreRequest
from scrapy.utils.defer import defer_fail
from twisted.python import failure

class ImdbSpiderSpider(scrapy.Spider):
    name = 'imdb_spider'
    allowed_domains = ['www.imdb.com']
    # scrapping the url
    # start_urls = ['https://www.imdb.com/search/title/?groups=top_250']
    start_urls = ['https://www.imdb.com/search/title/?groups=top_1000&sort=user_rating,desc&count=100&ref_=adv_prv']
    def parse(self, response,**kwargs):
        """
                 extract required information from the imdb website. While doing the scrapping
                :param response: It will return the required the data from the website, Also return data present on next pages
                :param kwargs: Arbitrary keyword arguments.
                :return: It will go the return all the necessary data scraped from the website
                """
        try:
            """ 
            It will scraped required information form website like movie name. movie link, movie rating etc...
            After data get scrapped it will store into the database. 
            """
            self.logger.info('Parse function called on %s', response.url)
            movies = response.xpath("//div[@class='lister-item-content']")
            for movie in movies:
                item = ImdbscraperItem()
                movie_name = movie.xpath(".//h3//a//text()").get()
                movie_link = "https://www.imdb.com" + movie.xpath(".//h3//a//@href").get()
                movie_rating = movie.xpath(".//div[@class='ratings-bar']//strong//text()").get()
                movie_description = movie.xpath(".//p[@class='text-muted']//text()").get()
                movie_gross = movie.xpath(".//span[@name='nv']//text()").getall()
                if len(movie_gross) == 3:
                    movie_get_amount = movie.xpath(".//p[@class='sort-num_votes-visible']//span[5]//text()").get()
                    item['amount'] = movie_get_amount
                else:
                    item['amount'] = ''
                movie_release_year = movie.xpath(".//span[@class='lister-item-year text-muted unbold']//text()").get()
                movie_runtime = movie.xpath(".//span[@class='runtime']//text()").get()
                movie_categories = movie.xpath(".//span[@class='genre']//text()").get()
                movie_vote = movie.xpath(".//p[@class='sort-num_votes-visible']//span[2]//text()").get()

                item['name'] = movie_name
                item['link'] = movie_link
                item['rating'] = movie_rating
                item['description'] = movie_description
                # item['amount'] = movie_get_amount
                item['year'] = movie_release_year
                item['runtime'] = movie_runtime
                item['categories'] = movie_categories
                item['vote'] = movie_vote
                yield item
        except IgnoreRequest as e:
            """
            Some times it may happen your request ignore by the website in that case the exceptions are going to raise into the system.
            """
            yield defer_fail(failure.Failure(e))

        next_page = response.xpath("//a[@class='lister-page-next next-page']//@href").get()
        if next_page is not None:
            yield scrapy.Request(response.urljoin(next_page))
