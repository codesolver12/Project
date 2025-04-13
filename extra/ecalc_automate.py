import csv
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from bs4 import BeautifulSoup

def automate_ecalc():
    # Specify the path to the chromedriver.exe file
    chromedriver_path = r"C:\Users\Administrator\Desktop\Falcons\chromedriver.exe"

    # Initialize the Selenium WebDriver with executable_path parameter
    driver = webdriver.Chrome(executable_path=chromedriver_path)

    # driver = webdriver.Chrome(executable_path=chromedriver_path)

    # Navigate to the Ecalc website
    driver.get('https://www.ecalc.ch/motorcalc.php')

    # Read the HTML source code
    html_source = driver.page_source

    # Use BeautifulSoup to parse the HTML
    soup = BeautifulSoup(html_source, 'html.parser')

    # Input values based on the structure of the HTML
    driver.find_element(By.NAME, 'weight').send_keys('16000')
    driver.find_element(By.NAME, 'wingspan').send_keys('64')
    driver.find_element(By.NAME, 'wingarea').send_keys('165')

    # Select 'Configuration' under 'Battery Cell' and write 6 in the first column
    select_battery_config = Select(driver.find_element(By.NAME, 'batterymounting'))
    select_battery_config.select_by_visible_text('Configuration')
    driver.find_element(By.NAME, 'batterycount').send_keys('6')

    # Select 'Manufacturer' under 'Motor' and choose Scorpion and A-5524-205 (194)
    select_motor_manufacturer = Select(driver.find_element(By.NAME, 'motor-manufacturer'))
    select_motor_manufacturer.select_by_visible_text('Scorpion')
    select_motor_model = Select(driver.find_element(By.NAME, 'motor-model'))
    select_motor_model.select_by_visible_text('A-5524-205 (194)')

    # Select 'Type' under 'Battery Cell' and choose HV-LiPo 4500 mAh - 45/60C
    select_battery_type = Select(driver.find_element(By.NAME, 'batterytype'))
    select_battery_type.select_by_visible_text('HV-LiPo 4500 mAh - 45/60C')

    # Select max 90A from the dropdown menu under 'Controller'
    select_controller = Select(driver.find_element(By.NAME, 'controller'))
    select_controller.select_by_visible_text('max 90A')

    # Select 'Manufacturer' under 'Propeller' and choose APC Electric E
    select_propeller_manufacturer = Select(driver.find_element(By.NAME, 'prop-manufacturer'))
    select_propeller_manufacturer.select_by_visible_text('APC Electric')
    
    # Select 'Type' under 'Propeller' and choose APC Electric E
    select_propeller_type = Select(driver.find_element(By.NAME, 'prop-type'))
    select_propeller_type.select_by_visible_text('APC Electric E')

    # Input values for Diameter and Pitch under 'Propeller'
    driver.find_element(By.NAME, 'prop-diameter').send_keys('22')
    driver.find_element(By.NAME, 'prop-pitch').send_keys('12')

    # Click on the Calculate button
    driver.find_element(By.NAME, 'calcbutton').click()

    # Wait for the calculation to complete
    time.sleep(5)

    # Read and extract values of electric Power, Static Thrust, and Specific thrust
    electric_power = driver.find_element(By.ID, 'power_value').text.strip()
    static_thrust = driver.find_element(By.ID, 'thrust_value').text.strip()
    specific_thrust = driver.find_element(By.ID, 'specific_thrust_value').text.strip()

    # Save the results to a CSV file
    with open('ecalc_results.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Motor', 'Battery', 'Controller', 'Diameter', 'Pitch', 'Electric Power', 'Static Thrust', 'Specific Thrust'])
        writer.writerow(['Scorpion', 'HV-LiPo 4500 mAh - 45/60C', 'max 90A', '22', '12', electric_power, static_thrust, specific_thrust])

    # Close the browser
    driver.quit()

if __name__ == "__main__":
    automate_ecalc()