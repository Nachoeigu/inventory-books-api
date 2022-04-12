from fastapi import FastAPI
from model import Data_Extractor, Data_Transformation

app = FastAPI()

data_extraction = Data_Extractor()
data_extraction.main()
data_transformation = Data_Transformation(data_extraction)
data_transformation.cleaning_html()

@app.get('/get-books')
def get_books():
    return {"Name":data_transformation.items}
