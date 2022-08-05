# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class ImdbscraperPipeline:
    ctr = 0
    def process_item(self, item, spider):
        ImdbscraperPipeline.ctr += 1
        print(ImdbscraperPipeline.ctr, '>>>>>>>>>>>>>>>>>>>>>>>>>>>>>.')
        item.save()
        return item
