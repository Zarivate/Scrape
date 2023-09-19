# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class BookscraperPipeline:
    def process_item(self, item, spider):

        adapter = ItemAdapter(item)

        # Get all the field names from the data
        field_names = adapter.field_names()

        # Removes any whitespace from the strings, excluding the description
        for field_name in field_names:
            if field_name != 'description':
                value = adapter.get(field_name)
                adapter[field_name] = value.strip()

        # Lowercase all the category and product_type strings
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()


        # Convert the prices to float values
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', "tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = adapter.replace("$", "")
            adapter[price_key] = float(value)

        # Store only the availability number, not the whole string
        avail_string = adapter.get('availability')
        split_string_array = avail_string.split('(')
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        else:
            avail_array = split_string_array[1].split(' ')
            adapter['availability'] = int(avail_array[0])

        return item
