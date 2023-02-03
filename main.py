from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium.webdriver.common.action_chains import ActionChains
import os
from bs4 import BeautifulSoup
import pandas as pd


# driver = webdriver.Chrome()
# WINDOW_SIZE = "1366,768"
options = webdriver.ChromeOptions()
# options.add_argument("--headless")
# options.add_argument("--window-size=%s" % WINDOW_SIZE)
options.add_argument('--disable-gpu')
# caps = DesiredCapabilities().CHROME
# caps["pageLoadStrategy"] = "eager"
# driver = webdriver.Chrome()

driver = uc.Chrome(use_subprocess=True)
driver.maximize_window()
driver.set_page_load_timeout(300)


def scraping_data(link):
    try:
        time.sleep(4)
        allContent = ""
        page = driver.page_source
        soup = BeautifulSoup(page, "html.parser")
        time.sleep(4)
        title = soup.find("h1", class_="text-h2 font-bold mb-2 m:mb-4")
        title = title.text
        print(title)
        author = soup.find("h2", class_="text-h5 font-bold mb-4 m:mb-6")
        author = author.text
        print(author)
        # x = soup.find("h4", class_ = "font-bold text-h4 mb-4 mx-4")
        # print(x.text)
        aboutBook = soup.find("div", class_="mb-8 mx-4")
        aboutBook.find("p")
        aboutBook = aboutBook.text
        print(aboutBook)
        aboutAuthor = soup.find(
            "div", class_="mx-4 border-b border-lightest-grey pb-6 m:pb-12")
        aboutAuthor.find("p")
        aboutAuthor = aboutAuthor.text
        print(aboutAuthor)
        driver.find_element(
            By.XPATH, "/html/body/div/div/div/div[2]/div[2]/div[2]/div/div/section/div/div/div[2]/div[4]/div[1]/a[1]").click()

        while 1:
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "p")))
            page = driver.page_source
            soup = BeautifulSoup(page, "html.parser")
            chapter = soup.find(
                "h2", class_="reader-content__headline mt-4 m:mt-0 m:mb-8")
            chapter = chapter.text
            print(chapter)
            content = soup.find(
                "span", class_="reader-content__text font-tisa-pro text-r2")
            content = soup.find_all("p")
            # print(content)

            # content = soup.find_all("strong")
            for para in content:
                x = para.text
                allContent = allContent + " " + x
            print(allContent)
            el = driver.find_element(
                By.XPATH, "//h2[@class = 'reader-content__headline mt-4 m:mt-0 m:mb-8']")
            tex = el.get_attribute("innerText")
            if not tex == "Final summary":
                try:
                    element = driver.find_element(
                        By.XPATH, "//button[@data-test-id = 'nextChapter']")
                    actions = ActionChains(driver)
                    actions.move_to_element(element).click().perform()
                except:
                    break

            else:
                # element = driver.find_element(
                #     By.XPATH, "//div[contains(text(), ' Mark as finished')]")
                # actions = ActionChains(driver)
                # actions.move_to_element(element).click().perform()
                break

        category = link.replace(
            "https://www.blinkist.com/en/content/categories/", "")
        if not os.path.isdir("./" + category):
            os.makedirs("./"+category)
            path = "./" + category + "//" + title + ".csv"
            bookData = pd.DataFrame([[title, author, aboutBook, aboutAuthor, allContent]], columns=[
                'Book Name', 'Author Name', "About Book", "About Author", "Summary "])
            bookData.to_csv(path)
        else:
            bookData = pd.DataFrame([[title, author, aboutBook, aboutAuthor, allContent]], columns=[
                'Book Name', 'Author Name', "About Book", "About Author", "Summary "])
            path = "./" + category + "//" + title + ".csv"
            bookData.to_csv(path)

    except WebDriverException as e:
        print(e)
        time.sleep(32423)


try:
    driver.get("https://www.blinkist.com")
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Change cookie settings')]")))
    element.click()
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Save selection')]")))
    element.click()
    time.sleep(2)
    # time.sleep(20)
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Log in')]")))
    element.click()
    time.sleep(1)
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "login-popup_login_email")))
    element.send_keys("email")

    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.ID, "login-popup_login_password")))
    element.send_keys("password")
    time.sleep(1)
    element = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@value = 'Log in with email']")))
    time.sleep(1)
    element.click()
    time.sleep(1)

except Exception as e:
    print(e)

try:
    category_url = pd.read_csv('links_categories.csv')
    print(len(category_url.category_links))
    for link in category_url.category_links:
        driver.get(link)
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div/div/div[2]/div[1]/section[5]/div[2]/div/div[@class = 'snap-start lg:snap-none first:ml-4 last:mr-4 m:first:ml-0 m:last:mr-0 ']")))
        elements = driver.find_elements(
            By.XPATH, "/html/body/div[1]/div/div/div[2]/div[1]/section[5]/div[2]/div/div[@class = 'snap-start lg:snap-none first:ml-4 last:mr-4 m:first:ml-0 m:last:mr-0 ']")
        print(len(elements))
        for bookNo in range(len(elements)):
            driver.get(link)
            WebDriverWait(driver, 20).until(
                EC.presence_of_element_located((By.TAG_NAME, "footer")))
            books = driver.find_elements(
                By.XPATH, "/html/body/div[1]/div/div/div[2]/div[1]/section[5]/div[2]/div/div[@class = 'snap-start lg:snap-none first:ml-4 last:mr-4 m:first:ml-0 m:last:mr-0 ']")
            actions = ActionChains(driver)
            actions.move_to_element(books[bookNo]).click().perform()
            # element.click()
            time.sleep(2)
            scraping_data(link)

        # for element in elements:
        #     driver.get(link)
        #     WebDriverWait(driver, 20).until(
        #         EC.presence_of_element_located((By.TAG_NAME, "footer")))
        #     actions = ActionChains(driver)
        #     actions.move_to_element(element).click().perform()
        #     # element.click()
        #     time.sleep(2)
        #     scraping_data(link)

    time.sleep(32423)

except WebDriverException as e:
    print(e)
    time.sleep(32423)
