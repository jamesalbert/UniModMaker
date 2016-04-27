from configparser import ConfigParser, ExtendedInterpolation
from selenium import webdriver
from os import environ, path

conf = ConfigParser()
conf._interpolation = ExtendedInterpolation()
conf.read('./conf.ini')

environ['PATH'] += ':{}'.format(path.dirname(path.abspath(__file__)))
driver = webdriver.Chrome()
driver.get('http://localhost:5000')

for label, content in conf.items("auto"):
    driver.find_element_by_name(label).send_keys(content)
driver.find_element_by_name('download').click()
# driver.close()
