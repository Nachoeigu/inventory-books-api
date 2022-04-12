import asyncio
import aiohttp
import random
import time
from constants import basic_headers
from lxml import html
import re

class Data_Extractor:
    def __init__(self):
        #Here we will save the responses
        self.responses = []

    async def get_books(self, session, number:int):
        data = await session.get(f'https://books.toscrape.com/catalogue/page-{number}.html', headers = random.choice(basic_headers))
        #We convert it into HTML object
        self.responses.append(html.fromstring(await data.text()))
        print(f"Scraped page Nº {number}")
    

    #This function will gather all the tasks in a list so then we can call the list and execute the tasks asynchronously
    async def defining_tasks(self, session):
        tasks = []
        #For the BWIN case:
        for number in range(1,50):
            #With this syntaxis, we create the name of the tasks automatically
            task = self.get_books(session, number)
            tasks.append(task)

        return tasks

    #With this funcion, we execute asynchronously the tasks
    async def executing_tasks(self):
        async with aiohttp.ClientSession() as session:
            tasks = await self.defining_tasks(session)
            await asyncio.gather(*tasks)

    #This function is which we will use each time we instance the class
    def main(self):
        i = time.time()
        asyncio.run(self.executing_tasks())
        print(time.time()-i)
        return self.responses

class Data_Transformation(Data_Extractor):
    
    def __init__(self, data_extractor_responses):
        self.responses = data_extractor_responses.responses
        self.items = []
        self.prices_in_eur = []
        self.ratings = []
        self.stock = []
        self.url = []

    def __flatten_list(self):
        self.url = [item for sublist in self.url for item in sublist]
        self.ratings = [item for sublist in self.ratings for item in sublist]
        self.items = [item for sublist in self.items for item in sublist]
        self.prices_in_eur = [item for sublist in self.prices_in_eur for item in sublist]
        self.stock = [item for sublist in self.stock for item in sublist]

    def cleaning_html(self):
        for response in self.responses:
            enlaces = response.xpath("//ol//li//div[@class='image_container']//a/@href")
            enlaces = list(map(lambda x :"https://books.toscrape.com/catalogue/" + x, enlaces))
            stars = response.xpath("//ol//li//p[contains(@class, 'star-rating')]/@class")
            #We remove unnecesary words for its value
            stars = list(map(lambda x: x.replace("star-rating ", ''), stars))
            titles = response.xpath("//ol//li//h3//a/@title")
            prices = response.xpath("//ol//li//div[@class='product_price']//p[@class='price_color']/text()")
            #We remove the symbol of the coin
            prices = list(map(lambda x: re.sub("£", "", x), prices))
            availability = response.xpath("//ol//li//div[@class='product_price']//p[contains(@class,('availability'))]//text()")
            availability = list(map(lambda x : x.replace("\n","").strip(), availability))
            availability = ['Out of stock' if item.replace("\n","").strip() == '' else item.replace("\n","").strip() for item in availability]
            self.url.append(enlaces)
            self.ratings.append(stars)
            self.items.append(titles)
            self.prices_in_eur.append(prices)
            self.stock.append(availability)

            self.__flatten_list()
        
        


