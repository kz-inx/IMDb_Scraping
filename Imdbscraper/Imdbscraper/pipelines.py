# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ImdbscraperPipeline:
    """ store the scraped data into database """
    def process_item(self, item, spider):
        """
        this function will return your data into items then it will store into the main database
        :param item: it will go to return the data in the form of the dict
        :return: it will the dict in the form the
        """
        item.save()
        return item
