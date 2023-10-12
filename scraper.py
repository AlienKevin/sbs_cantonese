from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import json

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

driver.get("https://www.sbs.com.au/language/chinese/zh-hant/podcast/sbs-cantonese")

max_items = 30

output_file = open("metadata.jsonl", "w+")

for i in range(max_items):
    print(f"i = {i}")

    radio_items_path = "div[data-testid='radio-item']"
    radio_items = driver.find_elements(by=By.CSS_SELECTOR, value=radio_items_path)
    
    if i > len(radio_items) - 1:
        # fetch more items
        load_more_button_path ="button[data-testid='episodes-load-more-button']"
        load_more_button = driver.find_element(by=By.CSS_SELECTOR, value=load_more_button_path)
        load_more_button.click()
        driver.implicitly_wait(0.5)
        wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, load_more_button_path)))
        radio_items = driver.find_elements(by=By.CSS_SELECTOR, value=radio_items_path)

    radio_item = radio_items[i]

    scraped_item = {}
    
    radio_title = radio_item.find_element(by=By.CSS_SELECTOR, value="div[data-testid='play-item-title']")
    title = radio_title.find_element(by=By.CSS_SELECTOR, value=":scope > span:first-child").text
    scraped_item["title"] = title
    date = radio_title.find_element(by=By.CSS_SELECTOR, value=":scope > div > span:first-child").text
    scraped_item["date"] = date
    
    # Open menu
    more_button = radio_item.find_element(by=By.CSS_SELECTOR, value="button[data-testid='moreVertical']")
    more_button.click()
    
    # Adding explicit wait for menu items to appear
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "a[data-testid='view more']")))

    view_more_link = driver.find_element(by=By.CSS_SELECTOR, value="a[data-testid='view more']").get_attribute('href')
    scraped_item["view_more_link"] = view_more_link

    download_link = driver.find_element(by=By.CSS_SELECTOR, value="a[data-testid='download']").get_attribute('href')
    scraped_item["download_link"] = download_link

    output_file.write(json.dumps(scraped_item, ensure_ascii=False) + "\n")
    output_file.flush()

    driver.implicitly_wait(1)

    # close the menu
    background = driver.find_element(by=By.CSS_SELECTOR, value="div[data-testid='more-popover'] > div")
    background.click()

output_file.close()
