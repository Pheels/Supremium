import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

#Fill in the details here exactly as you would on Supreme
fname = "Harambe McHarambeFace"
email = "harambe@apemail.com"
phone = "07813256629"
address = "10 yagyal"
city = "dodge"
country = "UK"
postcode = "W11 2BS"
cctype = "Visa"  # "Master" "Visa" "American Express"
ccnumber = "65743046833095843"
ccmonth = "06"
ccyear = "2018"
cccvc = "739"

#Details for the first item your after... obviously chose the item you want most
item1 = 'Shadow'
colour1 = '2'
size1 = 'Large'
#Url to start at. If you don't know what section it will be in go for http://www.supremenewyork.com/shop/all/new.
url1 = 'http://www.supremenewyork.com/shop/all/new'

#Details for second item
item2 = 'Cargo'
colour2 = '1'
size2 = '30'
url2 = 'http://www.supremenewyork.com/shop/all/pants'


foundurl = ''

#formatting the cc number as chrome driver has a mind of it's own
lasdig = ccnumber[-1]
ccnumber = lasdig + ccnumber

#Setup the chrome drive
driver = webdriver.Chrome()

def find(url, t, item, colour, size):

    driver.get(url)
    try:
        element = WebDriverWait(driver, 100000).until(
            EC.presence_of_element_located((By.XPATH, "//*[contains(text(), '"+ item +"')]"))
        )
    finally:
        driver.find_element_by_xpath("//*[contains(text(), '"+ item +"')]").click()

    global foundurl
    foundurl = driver.current_url
    start = time.time()
    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, "//*[@id='details']/ul/li["+ colour +"]/a[1]/img"))
        )
    finally:
        driver.find_element_by_xpath("//*[@id='details']/ul/li["+ colour +"]/a[1]/img").click()

    select = Select(driver.find_element_by_name('size'))
    select.select_by_visible_text(size)
    time.sleep(0.5)
    ouelem = driver.find_element_by_name("commit").click()

    try:
        element = WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.LINK_TEXT, "checkout now"))
        )
    finally:
        driver.find_element_by_link_text("checkout now").click()

    done = time.time()
    elapsed = done - start
    print 'time to find item: '
    print elapsed

def main(url, t, item, colour, size):
    find(url, t, item, colour, size);
    time.sleep(t)
    start = time.time()

    #Enter details
    nam = driver.find_element_by_id("order_billing_name")
    nam.send_keys(fname)
    mail = driver.find_element_by_id("order_email")
    mail.send_keys(email)
    phon = driver.find_element_by_id("order_tel")
    phon.send_keys(phone)
    addr = driver.find_element_by_id("bo")
    addr.send_keys(address)
    cit = driver.find_element_by_id("order_billing_city")
    cit.send_keys(city)
    pc = driver.find_element_by_id("order_billing_zip")
    pc.send_keys(postcode)
    select2 = Select(driver.find_element_by_id('order_billing_country'))
    select2.select_by_visible_text(country)
    select3 = Select(driver.find_element_by_id('credit_card_type'))
    select3.select_by_visible_text(cctype)

    cnb = driver.find_element_by_id("cnb")
    for num in ccnumber:
        cnb.send_keys(num)

    select4 = Select(driver.find_element_by_id('credit_card_month'))
    select4.select_by_visible_text(ccmonth)
    select5 = Select(driver.find_element_by_id('credit_card_year'))
    select5.select_by_visible_text(ccyear)
    vval = driver.find_element_by_id("vval")
    vval.send_keys(cccvc)

    #tick terms and conditions
    driver.find_element_by_xpath('//*[@id="cart-cc"]/fieldset/p/label/div/ins').click()
    #check out
    commintelem = driver.find_element_by_name("commit").click()

    done = time.time()
    elapsed = done - start
    print 'time taken to checkout: '
    print elapsed

if __name__ == "__main__":
    main(url1, 0.3, item1, colour1, size1)
    time.sleep(1)
    #driver.get(foundurl)
    main(url2, 0.3, item2, colour2, size2)
