import os
import sys
import yaml
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def parse_yml():
	"""
	Parses the config file and returns dict
	"""
	with open('config.yml') as stream:
		try:
			config = yaml.safe_load(stream)
		except yaml.YAMLError as exc:
			print(exc)
	return config

def init_driver():
	"""
	Initializes chromedriver
	"""
	options = webdriver.ChromeOptions()
	options.add_argument("--start-maximized")
	driver = webdriver.Chrome()
	return driver

def upass_loadpage(config, driver):
	"""
	Loads upass page and selects university
	"""
	driver.get("https://upassbc.translink.ca/")
	option_visible_text = config["university"]
	select = driver.find_element(by="id", value="PsiId")
	driver.execute_script("var select = arguments[0]; for(var i = 0; i < select.options.length; i++){ if(select.options[i].text == arguments[1]){ select.options[i].selected = true; } }", select, option_visible_text)

	driver.find_element(by="name", value="PsiId").send_keys(Keys.RETURN)
	driver.find_element(by="name", value="PsiId").send_keys(Keys.RETURN)
	driver.find_element(by="name", value="PsiId").send_keys(Keys.DOWN)
	driver.find_element(by="name", value="PsiId").send_keys(Keys.UP)
	driver.find_element(by="name", value="PsiId").send_keys(Keys.TAB)
	element = driver.find_element(by="id", value="goButton")
	element.send_keys("RETURN")
	element.submit()


def ubc_auth(config, driver):
	"""
	Login to UBC portal
	"""
	driver.find_element(by="id", value="username").send_keys(config["username"])
	driver.find_element(by="id", value="password").send_keys(config["password"])
	driver.find_element(by="name", value="_eventId_proceed").send_keys(Keys.RETURN)


def sfu_auth(config, driver):
	"""
	Login to SFU portal
	"""
	driver.find_element(by="id", value="username").send_keys(config["username"])
	driver.find_element(by="id", value="password").send_keys(config["password"])
	driver.find_element_by_tag_name("INPUT").send_keys(Keys.RETURN)


def request_pass(driver):

	try:
		driver.find_element(by="id", value="chk_1").click()
		driver.find_element(by="id", value="requestButton").click()
	except:
		print("No pass available for request.")

def send_email():
	# Load the email and password from the YAML file
    with open('config.yml') as file:
        config = yaml.safe_load(file)
    email = config['email']
    password = config['password']

    msg = MIMEMultipart()
    msg['From'] = email
    msg['To'] = email
    msg['Subject'] = 'Action was successful'
    msg.attach(MIMEText('The action was successful.', 'plain'))

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(email, password)
    text = msg.as_string()
    server.sendmail(email, 'recipient-email@gmail.com', text)
    server.quit()

def check_stats(driver, email=0):
	# Check status to ensure that the pass has been requested
	status_divs = driver.find_elements(by="class name", value="status")
	for div in status_divs:
		if "Processed" not in div.text and "Requested" not in div.text:
			print("Action was not successful")
			return
	print("Action was successful")
	if email == 1:
		send_email()


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


	# Wait for 10 seconds
	time.sleep(10)

	request_pass(driver)

	# Wait for 10 seconds 
	time.sleep(10)

	check_stats(driver)


if __name__=="__main__":
	main()