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
                adapter[field_name] = value[0].strip()

        # Lowercase all the category and product_type strings
        lowercase_keys = ['category', 'product_type']
        for lowercase_key in lowercase_keys:
            value = adapter.get(lowercase_key)
            adapter[lowercase_key] = value.lower()


        # Convert the prices to float values
        price_keys = ['price', 'price_excl_tax', 'price_incl_tax', "tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace("£", "")
            adapter[price_key] = float(value)

        # Store only the availability number, not the whole string
        avail_string = adapter.get('availability')
        # Split the string at the first parentheses, since that's where the actual number is held, IE: "In stock (5 available)"
        split_string_array = avail_string.split('(')
        # If the length of the split array is less than 2, then that means there are none available and just set that as the value
        if len(split_string_array) < 2:
            adapter['availability'] = 0
        # Otherwise split the string again, this time now split the first value in the array, which should be the parentheses value
        # holding the availibility, IE: (5 available), at the white space between them and convert the string value to an int and 
        # store that in the 'availability' parameter
        else:
            avail_array = split_string_array[1].split(' ')
            adapter['availability'] = int(avail_array[0])


        # Convert the review count to an actual number from a string
        num_reviews = adapter.get("num_reviews")
        adapter["num_reviews"] = int(num_reviews)


        # Convert the star count from a string to an actual number
        stars_string = adapter.get("stars")
        split_stars = stars_string.split(" ")
        star_value = split_stars[1].lower()
 
        if star_value == "zero":
            adapter["stars"] = 0
        elif star_value == "one":
            adapter["stars"] = 1
        elif star_value == "two":
            adapter["stars"] = 2
        elif star_value == "three":
            adapter["stars"] = 3
        elif star_value == "four":
            adapter["stars"] = 4
        elif star_value == "five":
            adapter["stars"] = 5

        return item

import mysql.connector

# Class that handles the actual data upload to any MySQL databases
class SaveToMySQLPipeline:
    def __init__(self):
        self.conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            # Password excluded here for obvious reasons
            password = '',
            database = 'books'
        )

        ## Create cursor, used to execute commands
        self.cur = self.conn.cursor()
        
        ## Create new books table if none exists
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS books(
            id int NOT NULL auto_increment, 
            url VARCHAR(255),
            title text,
            upc VARCHAR(255),
            product_type VARCHAR(255),
            price_excl_tax DECIMAL,
            price_incl_tax DECIMAL,
            tax DECIMAL,
            price DECIMAL,
            availability INTEGER,
            num_reviews INTEGER,
            stars INTEGER,
            category VARCHAR(255),
            description text,
            PRIMARY KEY (id)
        )
        """)

    # The actual insert statement for the tables
    def process_item(self, item, spider):
        self.cur.execute(""" insert into books (
            url, 
            title, 
            upc, 
            product_type, 
            price_excl_tax,
            price_incl_tax,
            tax,
            price,
            availability,
            num_reviews,
            stars,
            category,
            description
            ) values (
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s,
                %s
                )""", (
            item["url"],
            item["title"],
            item["upc"],
            item["product_type"],
            item["price_excl_tax"],
            item["price_incl_tax"],
            item["tax"],
            item["price"],
            item["availability"],
            item["num_reviews"],
            item["stars"],
            item["category"],
            str(item["description"][0])
        ))

        ## Execute insert of data into database
        self.conn.commit()
        return item

    
    def close_spider(self, spider):

        ## Close cursor & connection to database 
        self.cur.close()
        self.conn.close()