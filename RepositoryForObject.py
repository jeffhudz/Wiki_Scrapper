class ObjectRepository:

    def __init__(self):
        print()

    def getUsernameforMongoDB(self):
        username = "kavimaurya1997@gmail.com"
        return username

    def getPasswordforMongoDB(self):
        password = "Kavita@123"
        return password

    def getLoginCloseButton(self):
        login_close_button = "//body[1]/div[2]/div[1]/div[1]/button[1]"
        return login_close_button

    def getInputSearchArea(self):
        search_input_area = "(//span[text()='haseł']/following::input)[3]"
        return search_input_area


    def getSearchButton(self):
        search_button = "//i[@data-jsl10n='search-input-button']"
        return search_button













