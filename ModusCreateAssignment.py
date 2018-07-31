
# import stuff
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select


browser = webdriver.Chrome()
actions = ActionChains(browser)


# verify that web page opened properly

def loadUrl(url='https://budget.modus.app/'):
    browser.get(url=url)
    message = 'Correct url loaded : '
    if browser.current_url == url:
        print('Correct url loaded : ', True)
    else:
        print('Correct url loaded : ', False)

# look up elements of item table
def verifyTable():
    message = 'Table verified : '
    try:
        table = browser.find_element_by_class_name('opmhI')
        table.find_elements_by_xpath("//*[text()[contains(., 'Category')]]"),
        table.find_elements_by_xpath("//*[text()[contains(., 'Description')]]"),
        table.find_elements_by_xpath("//*[text()[contains(., 'Amount')]]")
        print(message, True)

    except NoSuchElementException:
        print(message, False)

# checks and returns values of total inflow, total outflow, working balance
def findMoneyValues():
# find values of total inflow
    totalInflow = float((browser.find_element_by_xpath('//*[@id="root"]/main/section/div/div/div[1]/div/div[1]').text)\
        .replace('$', '').replace(',', ''))

    # find value of total outflow
    totalOutflow = float((browser. find_element_by_xpath('//*[@id="root"]/main/section/div/div/div[3]/div/div[1]').text)\
        .replace('$', '').replace(',', ''))

    # find total value of working balance
    totalWorkingBalance = float((browser.find_element_by_xpath('//*[@id="root"]/main/section/div/div/div[5]/div/div[1]')
                                 .text).replace('$', '').replace(',', ''))

    return totalInflow, totalOutflow, totalWorkingBalance


# add an item to the table
def addMoney(categoryName = 'School', descriptionText = 'muchQA', valueNum = 2000):
    # various messages and descriptions of tests
    messageTableSize = 'Table size changed : '
    messageCategory = 'Item category added : '
    messageDescription = 'Item description added : '

    # count items in order to verify that new line was added later
    tableLength = len(browser.find_elements_by_xpath("//*[text()[contains(., 'Category')]]"))
    itemsByCategory = browser.find_elements_by_xpath("//*[text()[contains(., '" + categoryName + "')]]")
    itemsByDescription = browser.find_elements_by_xpath("//*[text()[contains(., '" + descriptionText + "')]]")

    # save monetary values for future comparison
    totalInflow1, totalOutflow1, workingBalance1 = findMoneyValues()

    # find fields and enter data
    categoryMenu = Select(browser.find_element_by_name('categoryId'))
    categoryMenu.select_by_visible_text(categoryName)
    browser.find_element_by_name('description').send_keys(descriptionText)
    browser.find_element_by_name('value').send_keys(valueNum)

    # click add
    browser.find_element_by_xpath("//*[text()[contains(., 'Add')]]").click()

    # measure table length, compare to previous value
    tableLength2 = len(browser.find_elements_by_xpath("//*[text()[contains(., 'Category')]]"))
    if tableLength2 - tableLength == 1:
        print(messageTableSize, True)
    else:
        print(messageTableSize, False)

    # recount number of lines with category entered above, compare
    itemsByCategory2 = browser.find_elements_by_xpath("//*[text()[contains(., '" + categoryName + "')]]")
    if len(itemsByCategory2) - len(itemsByCategory) == 1:
        print(messageCategory, True)
    else:
        print(messageCategory, False)

    # recount number of items with description entered above, compare
    itemsByDescription2 = browser.find_elements_by_xpath("//*[text()[contains(., '" + descriptionText + "')]]")
    if len(itemsByDescription2) - len(itemsByDescription) == 1:
        print(messageDescription, True)
    else:
        print(messageDescription, False)

    # recheck monetary values, compare
    totalInflow2, totalOutflow2, workingBalance2 = findMoneyValues()
    messageMoneyFlow = 'Correct money flow : '

    if categoryName == 'Income':
        if totalInflow2 - totalInflow1 == valueNum and workingBalance2 - workingBalance1 == valueNum:
            print(messageMoneyFlow, True)
        else:
            print(messageMoneyFlow, False)

    else:
        if totalOutflow2 - totalOutflow1 == valueNum and workingBalance1 - workingBalance2 == valueNum:
            print(messageMoneyFlow, True)
        else:
            print(messageMoneyFlow, False )


loadUrl()
verifyTable()
addMoney(categoryName='Income', descriptionText='muchQA', valueNum=100)
addMoney()

browser.quit()
