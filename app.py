from fastapi import FastAPI
import pandas as pd

df = pd.read_csv('dataframe.csv')

app = FastAPI()

#With this query you retrieve all the books with its IDs
@app.get('/')
async def root():
    return {
        'Data':'Welcome to Book Store API. Use the /docs path so you can know our endpoints :)'
    }

#With this query you retrieve all the books with its IDs
@app.get('/get-books')
async def get_books():
    list_of_combinations = []
    for index in range(0,len(df)):
        item = {str(df.iloc[index]['upc_code']) : df.iloc[index]['title']}
        list_of_combinations.append(item)

    return {
        'last_update': df.last_update.iloc[0],
        'data': {
        'id_and_books': list_of_combinations
    }}

#With this query you obtain the details of the specific book you look for
@app.get('/get-details/{id}')
def book_details(id:str):
    for idx in range(0,len(df)):
        product_id = df['upc_code'].iloc[idx]
        if str(product_id) == str(id):
            return {
                'last_update': df.last_update.iloc[0],
                'data': { 
                'name': df['title'].iloc[idx],
                'price_in_eur': str(df['price_in_eur'].iloc[idx]),
                'rating': str(df['rating'].iloc[idx]),
                'stock_units': str(df['stock_units'].iloc[idx]),
                'link': df['links'].iloc[idx]
                }
                }
    return {
        'Data': 'Sorry, we couldn´t find that ID'
        }

#With this query you obtain the books that matches with the rating you want: you should type /books-rating?number={number}
@app.get('/books-rating')
def books_with_your_desired_rating(number:int):
    cases_with_rating = []
    for idx in range(0,len(df)):
        rating = int(df['rating'].iloc[idx])
        if rating == number:
            case = { 
                'id': str(df.iloc[idx]['upc_code']),
                'book': df['title'].iloc[idx],
                'price_in_eur': str(df['price_in_eur'].iloc[idx]),
                'rating': str(df['rating'].iloc[idx]),
                'stock_units': str(df['stock_units'].iloc[idx]),
                'link': df['links'].iloc[idx]
                }
            cases_with_rating.append(case)
        else:
            continue

    if len(cases_with_rating) == 0:
        return {
            'Data': 'Sorry, we couldn´t find books with that rating. Remember they should be between 1-5'
            }    
    else:
        return {
            'last_update': df.last_update.iloc[0],
            'data':  
            cases_with_rating
            }

#With this query you obtain the book you want in the range you want
@app.get('/price_in_eur')
def books_by_prices(less_than:int=None, more_than:int=None,equal:int=None):
    prices = []
    if less_than is not None:
        for idx in range(0,len(df)):
            price = int(df['price_in_eur'].iloc[idx])
            if price < less_than:
                case = { 
                'id': str(df.iloc[idx]['upc_code']),
                'name': df['title'].iloc[idx],
                'price_in_eur': df['price_in_eur'].iloc[idx],
                'rating': str(df['rating'].iloc[idx]),
                'stock_units': str(df['stock_units'].iloc[idx]),
                'link': df['links'].iloc[idx]
                }
                prices.append(case)

    if more_than is not None:
        for idx in range(0,len(df)):
            price = int(df['price_in_eur'].iloc[idx])
            if price > more_than:
                case = { 
                'id': str(df.iloc[idx]['upc_code']),
                'name': df['title'].iloc[idx],
                'price_in_eur': df['price_in_eur'].iloc[idx],
                'rating': str(df['rating'].iloc[idx]),
                'stock_units': str(df['stock_units'].iloc[idx]),
                'link': df['links'].iloc[idx]
                }
                prices.append(case)
    if equal is not None:
        for idx in range(0,len(df)):
            price = int(df['price_in_eur'].iloc[idx])
            if price == equal:
                case = { 
                'id': str(df.iloc[idx]['upc_code']),
                'name': df['title'].iloc[idx],
                'price_in_eur': df['price_in_eur'].iloc[idx],
                'rating': str(df['rating'].iloc[idx]),
                'stock_units': str(df['stock_units'].iloc[idx]),
                'link': df['links'].iloc[idx]
                }
                prices.append(case)
    
    if len(prices) == 0:
        return {
            'Data': 'Sorry, we couldn´t find books that match your needs'
            }    
 
    else:
        return {
            'last_update': df.last_update.iloc[0],
            'data':  
            prices
            }
    
@app.get('/books-without-stock')
def books_without_stock():
    cases = []
    for idx in range(0,len(df)):
        stock_units = int(df['stock_units'].iloc[idx])
        if stock_units == 0:
            case = { 
            'id': str(df.iloc[idx]['upc_code']),
            'name': df['title'].iloc[idx],
            'price_in_eur': df['price_in_eur'].iloc[idx],
            'rating': str(df['rating'].iloc[idx]),
            'stock_units': str(df['stock_units'].iloc[idx]),
            'link': df['links'].iloc[idx]
            }
            cases.append(case)

    if len(cases) == 0:
        return {
            "Data": "We don´t have products without stock! :)"
        }
    else:
        return {
            "last_update": df.last_update.iloc[0],
            "data":cases
        }
        
