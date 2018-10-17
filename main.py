import os
import sys
import yaml
import re
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def parse_yml():
	"""
	Parses the config file and returns dict
	"""
	with open('config.yml') as stream:
	    try:
	        config = yaml.load(stream)
	    except yaml.YAMLError as exc:
	        print(exc)
	return config

def init_driver():
	"""
	Initializes chromedriver
	"""
	options = webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")
	return driver

def upass_loadpage(config, driver):
	"""
	Loads upass page and selects university
	"""
	driver.get("https://upassbc.translink.ca/")
	option_visible_text = config["university"]
	select = driver.find_element_by_id("PsiId")
	driver.execute_script("var select = arguments[0]; for(var i = 0; i < select.options.length; i++){ if(select.options[i].text == arguments[1]){ select.options[i].selected = true; } }", select, option_visible_text);

	driver.find_element_by_name("PsiId").send_keys(Keys.RETURN)
	driver.find_element_by_name("PsiId").send_keys(Keys.RETURN)
	driver.find_element_by_name("PsiId").send_keys(Keys.DOWN)
	driver.find_element_by_name("PsiId").send_keys(Keys.UP)
	driver.find_element_by_name("PsiId").send_keys(Keys.TAB)
	element = driver.find_element_by_id("goButton")
	element.send_keys("RETURN")
	element.submit()


def ubc_auth(config, driver):
	"""
	Login to UBC portal
	"""
	driver.find_element_by_id("j_username").send_keys(config["username"])
	driver.find_element_by_id("password").send_keys(config["password"])
	driver.find_element_by_name("action").send_keys(Keys.RETURN)


def sfu_auth(config, driver):
	"""
	Login to SFU portal
	"""
	driver.find_element_by_id("username").send_keys(config["username"])
	driver.find_element_by_id("password").send_keys(config["password"])
	driver.find_element_by_tag_name("INPUT").send_keys(Keys.RETURN)


def request_pass(driver):

	driver.find_element_by_id("chk_1").click()
	driver.find_element_by_id("requestButton").click()


def main():
	
	config = parse_yml()
	driver = init_driver()

	if config["university"] == "University of British Columbia":
		upass_loadpage(config, driver)
		ubc_auth(config, driver)

	elif config["university"] == "Simon Fraser University":
		upass_loadpage(config, driver)
		sfu_auth(config, driver)

	else:
		print("Sorry, your university is not currently supported.")


	request_pass(driver)


if __name__=="__main__":
	main()