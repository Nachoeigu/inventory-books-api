from model import Data_Extractor, Data_Transformation
import time
#First we make requests in the catalog
data_extraction = Data_Extractor()
data_extraction.main(mode = True)

#Then we parse the data so we obtain the URL of each book
data_transformation = Data_Transformation(data_extraction)
data_transformation.cleaning_html(mode = True)
urls = data_transformation.return_urls() #List of urls to requests again but in this case its for each book


#We make a request for each book url
books_extraction = Data_Extractor(urls)
books_extraction.main(mode = False)

#Then we parse the data so we obtain the details of each book
data_transformation = Data_Transformation(books_extraction)
data_transformation.cleaning_html(mode = False)
data_transformation.to_pandas()
