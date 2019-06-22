from splinter import Browser
from bs4 import BeautifulSoup


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/Users/Renee/Downloads/chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():
    browser = init_browser()
    review = {}

    url = "https://www.amazon.com/dp/B076WSB81F/"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    review["price"] = soup.find("span", class_="a-size-mini twisterSwatchPrice").get_text()
    #listings["price"] = soup.find("span", class_="result-price").get_text()
    #listings["hood"] = soup.find("span", class_="result-hood").get_text()

    print (review)
