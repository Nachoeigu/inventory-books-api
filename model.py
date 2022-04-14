import asyncio
import aiohttp
import random
import time
from constants import basic_headers
from lxml import html
import re
import pandas as pd
from datetime import datetime

class Data_Extractor:
    def __init__(self, list_of_urls:list=None):
        #Here we will save the responses
        self.responses = []
        if list_of_urls is None:
            pass
        else:
            self.list_of_urls = list_of_urls

    async def get_books(self, session, mode = True, number:int=None, book_url:str=None):
        #If mode = True, we want to obtain the urls of each book, if its False we want to scrape each book url
        if mode == True:
            data = await session.get(f'https://books.toscrape.com/catalogue/page-{number}.html', headers = random.choice(basic_headers))
            #We convert it into HTML object and we use a tuple because we want to conserv the url in order to add it in the API
            self.responses.append(html.fromstring(await data.text()))
            print(f"Obtaining URLs from page Nº {number}")

        else:
            data = await session.get(f'{book_url}', headers = random.choice(basic_headers))
            #We convert it into HTML object
            self.responses.append((html.fromstring(await data.text()), book_url))
            print(f"Obtaining details in page {book_url}")            

    #This function will gather all the tasks in a list so then we can call the list and execute the tasks asynchronously
    async def defining_tasks(self, session, mode):
        tasks = []
        if mode == True:
            #We have 50 pages in the site
            for number in range(1,50):
                #With this syntaxis, we create the name of the tasks automatically
                task = self.get_books(session, mode, number)
                tasks.append(task)

        else:  
            for url in self.list_of_urls:
                task = self.get_books(session, mode, book_url = url)
                tasks.append(task)
        return tasks

    #With this funcion, we execute asynchronously the tasks
    async def executing_tasks(self, mode):
        async with aiohttp.ClientSession() as session:
            tasks = await self.defining_tasks(session, mode)
            await asyncio.gather(*tasks)

    #This function is which we will use each time we instance the class
    def main(self, mode:bool):
        i = time.time()
        if mode == True:
            asyncio.run(self.executing_tasks(mode))
        else:
            asyncio.run(self.executing_tasks(mode))
        print(time.time()-i)
        return self.responses

class Data_Transformation(Data_Extractor):
    
    def __init__(self, data_extractor_responses):
        self.responses = data_extractor_responses.responses
        self.url = []

    def __flatten_list(self):
        self.url = [item for sublist in self.url for item in sublist]
        
    def __text_to_int(self, rating:str):
        if rating == 'one':
            return 1
        if rating == 'two':
            return 2
        if rating == 'three':
            return 3
        if rating == 'four':
            return 4
        if rating == 'five':
            return 5

    def cleaning_html(self, mode:bool):
        #If mode = True, we parse for URLs, if False we scrape the details of each book url
        self.date = []
        self.upc_code = []
        self.title = []
        self.price = []
        self.stock_units = []
        self.category = []
        self.rating = []
        self.reviews = []
        self.links = []
        
        for response in self.responses:
            if mode == True:
                enlaces = response.xpath("//ol//li//div[@class='image_container']//a/@href")
                enlaces = list(map(lambda x :"https://books.toscrape.com/catalogue/" + x, enlaces))
                self.url.append(enlaces)
            
            else:
                #response is a tuple: in the first element we have the response, in the second the url of that resopnse
                category = response[0].xpath("//ul[@class='breadcrumb']//li[not(@class)]//a//text()")[-1]
                title = response[0].xpath("//h1/text()")[0]
                price = response[0].xpath("//div[contains(@class, 'product_main')]//p[@class='price_color']//text()")[0].replace("£", "") 
                stock_units = response[0].xpath("//div[contains(@class, 'product_main')]//p[contains(@class,'availability')]//text()")[-1].strip()
                stock_units = re.search('[0-9]{1,}', stock_units).group()
                stars = response[0].xpath("//div[contains(@class,'product_main')]//p[contains(@class, 'star-rating')]/@class")[0].replace("star-rating ", '').lower()
                stars = self.__text_to_int(stars)
                upc_code = response[0].xpath("//tr/th[contains(text(),'UPC')]//parent::tr//td//text()")[0]
                reviews = response[0].xpath("//tr/th[contains(text(),'Number of reviews')]//parent::tr//td//text()")[0]
                date = datetime.today().date()
                link = response[1]


                self.date.append(date)
                self.upc_code.append(upc_code)
                self.title.append(title)
                self.price.append(price)
                self.stock_units.append(stock_units)
                self.category.append(category)
                self.rating.append(stars)
                self.reviews.append(reviews)
                self.links.append(link)
                
        self.__flatten_list()


    def to_pandas(self):
        df = pd.DataFrame({
                    "last_update":self.date,
                    "upc_code":self.upc_code,
                    "title":self.title,
                    "price_in_eur":self.price,
                    "stock_units":self.stock_units,
                    "category": self.category,
                    "rating":self.rating,
                    "reviews": self.reviews,
                    "links": self.links
                    })
        df.to_csv('dataframe.csv')

    def return_urls(self):       
        return self.url
        

        

