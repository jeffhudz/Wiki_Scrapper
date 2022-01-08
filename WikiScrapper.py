import random
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException

from selenium import webdriver
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait

from RepositoryForObject import ObjectRepository
from selenium.webdriver.common.by import By
import pandas as pd

from mongoDBOperations import MongoDBManagement


class WikiScrapper:

    def __init__(self, executable_path, chrome_options):
        """
        This function initializes the web browser driver
        :param executable_path: executable path of chrome driver.
        """
        try:
            self.driver = webdriver.Chrome(executable_path=executable_path, chrome_options=chrome_options)
        except Exception as e:
            raise Exception(f"(__init__): Something went wrong on initializing the webdriver object.\n" + str(e))

    def waitExplicitlyForCondition(self, element_to_be_found):
        """
        This function explicitly for condition to satisfy
        """
        try:
            ignored_exceptions = (NoSuchElementException, StaleElementReferenceException,)
            WebDriverWait(self.driver, 2, ignored_exceptions=ignored_exceptions).until(
                expected_conditions.presence_of_element_located((By.CLASS_NAME, element_to_be_found)))
            return True
        except Exception as e:
            return False

    def getCurrentWindowUrl(self):
        """
        This function returns the url of current window
        """
        try:
            current_window_url = self.driver.current_url
            return current_window_url
        except Exception as e:
            raise Exception(f"(getCurrentWindowUrl) - Something went wrong on retrieving current url.\n" + str(e))

    def getLocatorsObject(self):
        """
        This function initializes the Locator object and returns the locator object
        """
        try:
            locators = ObjectRepository()
            return locators
        except Exception as e:
            raise Exception(f"(getLocatorsObject) - Could not find locators\n" + str(e))
    def findElementByXpath(self, xpath):
        """
        This function finds the web element using xpath passed
        """
        try:
            element = self.driver.find_element(By.XPATH, value=xpath)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByXpath) - XPATH provided was not found.\n" + str(e))

    def findElementByClass(self, classpath):
        """
        This function finds web element using Classpath provided
        """
        try:
            element = self.driver.find_element(By.CLASS_NAME, value=classpath)
            return element
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(findElementByClass) - ClassPath provided was not found.\n" + str(e))

    def findElementByTag(self, tag_name):
        """
        This function finds web element using tag_name provided
        """
        try:
            element = self.driver.find_elements_by_tag_name(tag_name)
            return element
        except Exception as e:
            raise Exception(f"(findElementByTag) - ClassPath provided was not found.\n" + str(e))

    def findingElementsFromPageUsingClass(self, element_to_be_searched):
        """
        This function finds all element from the page.
        """
        try:
            result = self.driver.find_elements(By.CLASS_NAME, value=element_to_be_searched)
            return result
        except Exception as e:
            raise Exception(
                f"(findingElementsFromPageUsingClass) - Something went wrong on searching the element.\n" + str(e))

    def findingElementsFromPageUsingCSSSelector(self, element_to_be_searched):
        """
        This function finds all element from the page.
        """
        try:
            result = self.driver.find_elements(By.CSS_SELECTOR, value=element_to_be_searched)
            return result
        except Exception as e:
            raise Exception(
                f"(findingElementsFromPageUsingClass) - Something went wrong on searching the element.\n" + str(e))
    def openUrl(self, url):
        """
        This function open the particular url passed.
        :param url: URL to be opened.
        """
        try:
            if self.driver:
                self.driver.get(url)
                return True
            else:
                return False
        except Exception as e:
            raise Exception(f"(openUrl) - Something went wrong on opening the url {url}.\n" + str(e))


    def searchTopic(self, searchString):
        """
        This function helps to search product using search string provided by the user
        """
        try:
            locator = self.getLocatorsObject()
            search_box_path = self.findElementByXpath(xpath=locator.getInputSearchArea())
            search_box_path.send_keys(searchString)
            search_button = self.findElementByXpath(xpath=locator.getSearchButton())
            search_button.click()
            return True
        except Exception as e:
            # self.driver.refresh()
            raise Exception(f"(searchTopic) - Something went wrong on searching.\n" + str(e))

    def topicSearched(self, search_string):
        """
        This function returns the name of product searched
        """
        try:
            return search_string
        except Exception as e:
            raise Exception(f"(topicSearched) - Something went wrong on searching.\n" + str(e))

    def getTopicIDs(self):
        """
        This function returns all the topic topic ids
        """
        try:
            ids = [self.findElementByXpath('//*[@id]')]

            return ids
        except Exception as e:
            raise Exception(f"(getTopicIDs) - Something went wrong on getting ids from the page.")

    def getTopicLinks(self):
        """
        This function returns all the list of links.
        """
        try:
            links = []
            all_links = self.findElementByTag('a')
            for link in all_links:
                links.append(link.get_attribute('href'))
            return links
        except Exception as e:
            raise Exception(f"(getProductLinks) - Something went wrong on getting link from the page.")

    def getImages(self):
        """
        This function returns all the list of links.

        """
        try:
            images = []
            all_images = self.findElementByTag('img')
            for image in all_images:
                url = self.getCurrentWindowUrl()
                images.append(url + image['src'])
            return images
        except Exception as e:
            raise Exception(f"(getImages) - Something went wrong on getting link from the page.")

    def getParagraphs(self):
        try:
            paragraphs = []
            all_paragraphs = self.findElementByTag('p')
            for paragraph in all_paragraphs:
                paragraphs.append(paragraph.text)
            return paragraphs
        except Exception as e:
            raise Exception(f"(getImages) - Something went wrong on getting link from the page.")

    def topicsInPage(self):
        """
        This function returns the topics in the page
        """
        try:
            topics = []
            headers = ["h1", "h2", "h3", "h4", "h5", "h6"]
            for header in headers:
                topics.append(self.findElementByTag(header).text())
            return topics
        except Exception as e:
            raise Exception(f"(topicsInPage) - Something went wrong with getting topic from the page.")

    def linksbyTopic(self):
        """
        This function returns links by ID
        """
        try:
            topic_links = {}
            topics = self.getTopicLinks()
            for topic in topics:
                topic_links[topic] = self.getTopicLinks()
            return topic_links
        except Exception as e:
            raise Exception(f"(linksbyTopic) - Something went wrong on getting link from the page.")

    def wait(self):
        """
        This function waits for the given time
        """
        try:
            self.driver.implicitly_wait(2)
        except Exception as e:
            raise Exception(f"(wait) - Something went wrong.\n" + str(e))

    def generatingResponse(self, paragraphs, topics, ids, images, links):
        """
        This function generates the final response to send.
        """
        try:
            response_dict = {"paragraphs": [], "topics": [], "ids": [], "images": [], "links": []}

            response_dict["paragraphs"] = paragraphs
            response_dict["topics"] = topics
            response_dict["ids"] = ids
            response_dict["links"] = links
            response_dict["images"] = images
            return response_dict
        except Exception as e:
            raise Exception(f"(generatingResponse) - Something went wrong on generating response")

    def generateDataForColumnAndFrame(self, response_dict):
        """
        This function generates data for the column where only single data is presented. And then frames it in data frame.
        """
        try:
            data_frame = pd.DataFrame(response_dict)


            print(data_frame)
            return data_frame
        except Exception as e:
            raise Exception(
                f"(dataGeneration) - Something went wrong on creating data frame and data for column.\n" + str(e))


    def saveDataFrameToFile(self, dataframe, file_name):
        """
        This function saves dataframe into filename given
        """
        try:
            dataframe.to_csv(file_name)
        except Exception as e:
            raise Exception(f"(saveDataFrameToFile) - Unable to save data to the file.\n" + str(e))

    def closeConnection(self):
        """
        This function closes the connection
        """
        try:
            self.driver.close()
        except Exception as e:
            raise Exception(f"(closeConnection) - Something went wrong on closing connection.\n" + str(e))

    def getPageDetailsToDisplay(self, searchString, username, password):
        """
        This function returns the review and other details of product
        """
        try:
            search = searchString
            mongoClient = MongoDBManagement(username=username, password=password)
            locator = self.getLocatorsObject()

            db_search = mongoClient.findfirstRecord(db_name="Wiki-Scrapper",
                                                    collection_name=searchString,
                                                    query={searchString})
            print(db_search)
            if db_search is not None:
                print("Yes present" + str(len(db_search)))
            else:
                self.openUrl(url)
                topic_searched = self.topicSearched(search_string=searchString)

                ids = self.getTopicIDs()
                links = self.getTopicLinks()
                images = self.getImages()
                paragraphs = self.getParagraphs()
                topics = self.topicsInPage()
                links_by_topics = self.linksbyTopic()

                result = {'topic_searched': topic_searched,
                          'topic ids': ids,
                          'links': links,
                          'images': images,
                          'paragraphs': paragraphs,
                          'topics': topics,
                          }

                mongoClient.insertRecord(db_name="Flipkrat",
                                         collection_name=searchString,
                                         record=result)
                mongoClient.insertRecord(db_name="Flipkrat",
                                         collection_name=searchString + " " + "images",
                                         record=images)
                mongoClient.insertRecord(db_name="Flipkrat",
                                         collection_name=searchString + " " + "Topic_IDs",
                                         record=links_by_topics)
                print(result)

            return search
        except Exception as e:
            raise Exception(f"(getPageDetailsToDisplay) - Something went wrong on yielding data.\n" + str(e))
