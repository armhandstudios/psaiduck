from PokemonClasses import *
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains

def elementExists(driver, xpath):
    driver.implicitly_wait(0)
    try:
        driver.find_element_by_xpath(xpath)
    except NoSuchElementException:
        driver.implicitly_wait(10)
        return False
    driver.implicitly_wait(10)
    return True

def actionSucceeded(driver):
    if elementExists(driver, ".//div[@class='whatdo']"):
        return False
    else:
        return True

def printBothActiveMons(me, scrub):
    print("printBothActiveMons")
    print(me.getActive().name)
    print(scrub.getActive().name)

def isGameOver(driver):
    if elementExists(driver, ".//button[@name='closeAndRematch']"):
        return True
    return False

def attack(driver, move):
    if elementExists(driver, ".//button[@data-move='{}']".format(move.name)):
        driver.find_element_by_xpath(".//button[@data-move='{}']".format(move.name)).click()
    if actionSucceeded(driver):
        return True
    else:
        return False

#perform a likely valid switch
def switch(driver, trainer, pkmn):
    driver.find_element_by_xpath(".//button[@name='chooseSwitch' and text()[contains(., '{}')]]".format(pkmn.nickname)).click()
    if actionSucceeded(driver):
        trainer.switch(pkmn)
        return True
    else:
        return False