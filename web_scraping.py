import requests
import os
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time

driver = webdriver.Chrome(ChromeDriverManager().install())

driver.get("https://www.phoenixopendata.com/")

wait = WebDriverWait(driver, 10)
search_box = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "input.search")))

search_box.send_keys("gun pointed")

search_box.send_keys(Keys.ENTER)

time.sleep(5)

link1 = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[text()='Officer Pointed Gun at Person (PGP)']")))
link1.click()

time.sleep(5)

link2 = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[@class='heading'][contains(@href, '/dataset/pgp/resource/')][@title='Pointed Gun at Person Details']")))
link2.click()

time.sleep(5)

download_link = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.btn.btn-primary.resource-url-analytics.resource-type-None")))
download_url = download_link.get_attribute("href")

response = requests.get(download_url)
file_name = os.path.basename(download_url)

new_file_name = "gun_pointed"
file_name_parts = os.path.splitext(file_name)
new_file_name_with_extension = new_file_name + file_name_parts[1]

with open(new_file_name_with_extension, "wb") as file:
    file.write(response.content)

driver.quit()
