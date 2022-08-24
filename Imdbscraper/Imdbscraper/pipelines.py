# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter

from Scrapping.models import IMDbScrapping
from Scrapping.task import download_image

class ImdbscraperPipeline:
    """ store the scraped data into database """
    data_store = []
    def process_item(self, item, spider):
        """
        this function will return your data into items then it will store into the main database
        :param item: it will go to return the data in the form of the dict
        :return: it will the dict in the form the
        """
        obj = IMDbScrapping(**item)
        print(obj, '<<<<<', obj.image_urls, obj.image_file)
        ImdbscraperPipeline.data_store.append(obj)
        # item.save()
        return item

    def close_spider(self, spider):
        objects = IMDbScrapping.objects.bulk_create(ImdbscraperPipeline.data_store)
        for obj in objects:
            download_image.delay(obj.id)


