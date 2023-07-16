from selenium import webdriver
from selenium.webdriver.common.by import By
import time

driver = webdriver.Chrome()
driver.get("https://orteil.dashnet.org/experiments/cookie/")
driver.maximize_window()

button = driver.find_element(By.ID, "cookie")
store = driver.find_elements(By.CSS_SELECTOR, "#store b")
items = driver.find_elements(By.CSS_SELECTOR, "#store div")

item_ids = [item.get_attribute("id") for item in items]
item_price_list = [int(item.text.split("-")[1].strip().replace(",", "")) if item.text != "" else item for item in store]
cookie_upgrades = {item_price_list[n]: item_ids[n] for n in range(len(item_price_list))}

timeout = time.time() + 5
five_min = time.time() + 5 * 60


def check_my_money():
	money_element = driver.find_element(By.ID, "money").text

	if "," in money_element:
		money_element = money_element.replace(",", "")

	money_element = int(money_element)
	return money_element


def buyable_item(money_have):
	buyable_item_list = []
	for item_cost in cookie_upgrades:
		if money_have > item_cost:
			buyable_item_list.append(item_cost)
	max_price_item = max(buyable_item_list)
	item_name = cookie_upgrades[max_price_item]
	return item_name


def buy_item(item_name):
	item_check = driver.find_element(By.ID, item_name)
	item_check.click()


while True:
	button.click()

	if time.time() > timeout:
		money_have = check_my_money()
		max_price_item = buyable_item(money_have)
		buy_item(max_price_item)

		timeout = time.time() + 5

	if time.time() > five_min:
		output = driver.find_element(By.CSS_SELECTOR, "#saveMenu #cps")
		print(output.text)
		five_min = time.time() + 5 * 60
