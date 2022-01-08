# doing necessary imports
import threading
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure

from logger_class import getLog
from flask import Flask, render_template, request, jsonify, Response, url_for, redirect
from flask_cors import CORS, cross_origin
import pandas as pd
from mongoDBOperations import MongoDBManagement
from WikiScrapper import WikiScrapper
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

rows = {}
collection_name = None

logger = getLog('WikiScrapper.py')

free_status = True
db_name = 'Wiki-Scrapper'

app = Flask(__name__)  # initialising the flask app with the name 'app'

#For selenium driver implementation on heroku
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument("disable-dev-shm-usage")


#To avoid the time out issue on heroku
class threadClass:

    def __init__(self, searchString, scrapper_object):

        self.searchString = searchString
        self.scrapper_object = scrapper_object

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()  # Start the execution

    def run(self):
        global collection_name, free_status
        free_status = False
        collection_name = self.scrapper_object.getPageDetailsToDisplay(
                                                                   searchString=self.searchString, username='mongodb',
                                                                   password='mangodb'
                                                                   )
        logger.info("Thread run completed")
        free_status = True


@app.route('/', methods=['POST', 'GET'])
@cross_origin()
def index():
    if request.method == 'POST':
        global free_status
        ## To maintain the internal server issue on heroku
        if free_status != True:
            return "This website is executing some process. Kindly try after some time..."
        else:
            free_status = True
        searchString = request.form['content'].replace(" ", "")  # obtaining the search string entered in the form

        try:
            review_count = 0
            scrapper_object = WikiScrapper(executable_path=ChromeDriverManager().install(),
                                               chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='mongodb', password='mongodb')
            scrapper_object.openUrl("https://www.wikipedia.org/")
            logger.info("Url hitted")

            scrapper_object.searchTopic(searchString=searchString)
            logger.info(f"Search begins for {searchString}")
            if mongoClient.isCollectionPresent(collection_name=searchString, db_name=db_name):
                result = mongoClient.findAllRecords(db_name=db_name, collection_name=searchString)
                scrapper_object.saveDataFrameToFile(file_name="static/scrapper_data.csv",
                                                    dataframe=pd.DataFrame(result))
                logger.info("Data saved in scrapper file")

                return render_template('results.html', rows=result)  # show the results to user

            else:
                threadClass(searchString=searchString, scrapper_object=scrapper_object)
                return redirect(url_for('feedback'))

        except Exception as e:
            raise Exception("(app.py) - Something went wrong while rendering all the details of product.\n" + str(e))

    else:
        return render_template('index.html')


@app.route('/feedback', methods=['GET'])
@cross_origin()
def feedback():
    try:
        global collection_name
        if collection_name is not None:
            scrapper_object = WikiScrapper(executable_path=ChromeDriverManager().install(),
                                               chrome_options=chrome_options)
            mongoClient = MongoDBManagement(username='mongodb', password='mongodb')
            result = mongoClient.findAllRecords(db_name="Flipkrat", collection_name="Flipkart-Scrapper")

            return render_template('results.html', rows=result)
        else:
            return render_template('results.html', rows=None)
    except Exception as e:
        raise Exception("(feedback) - Something went wrong on retrieving feedback.\n" + str(e))


if __name__ == "__main__":
    app.run(port=8000)  # running the app on the local machine on port 8000
