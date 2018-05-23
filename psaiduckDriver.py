# The purpose of this class is to interact directly with the components of Pokemon Showdown and its Pokedex
# All methods that function data already obtained, or that merely use the drivers to check elemeents of the page for
# readiness, shall be grouped into HelperFunctions for added readability and to allow other classes to import them
# without import loops

#Imports
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.action_chains import ActionChains
import time
from PokemonClasses import *
from BattleStyle import *
import random
import json
from HelperFunctions import *


def opponentsName(driver):
    return driver.find_element_by_xpath(".//div[@class='rightbar']/div[1]").text

#find a battle, return when battle found
def findBattle(driver):
    driver.find_element_by_name("search").click()
    while elementExists(driver, ".//div[@class='switchmenu']") == False:
        time.sleep(2)

def challengeUser(driver, username):
    driver.find_element_by_name("finduser").click()
    driver.find_element_by_name("data").send_keys(username)
    driver.find_element_by_name("data").send_keys(Keys.ENTER)
    driver.find_element_by_name("challenge").click()
    driver.find_element_by_name("makeChallenge").click()
    while elementExists(driver, ".//div[@class='switchmenu']") == False:
        time.sleep(2)

def acceptChallenge(driver):
    while not elementExists(driver, ".//button[@name='acceptChallenge']"):
        time.sleep(1)
    driver.find_element_by_xpath(".//button[@name='acceptChallenge']").click()
    return

def getPokemonInfo(infoDriver, pkmnName):
    trimmedPkmnName = pkmnName.replace(" ", "")
    infoDriver.get("https://dex.pokemonshowdown.com/pokemon/{}".format(trimmedPkmnName))
    #get types
    type1 = infoDriver.find_element_by_xpath(".//dl[@class='typeentry']/dd/a[1]").text
    if elementExists(infoDriver, ".//dl[@class='typeentry']/dd/a[2]"):
        type2 = infoDriver.find_element_by_xpath(".//dl[@class='typeentry']/dd/a[2]").text
    else:
        type2 = None
    #getStats
    hp = infoDriver.find_element_by_xpath(".//table[@class='stats']/tbody/tr[2]/td").text
    atk = infoDriver.find_element_by_xpath(".//table[@class='stats']/tbody/tr[2]/td").text
    defense = infoDriver.find_element_by_xpath(".//table[@class='stats']/tbody/tr[4]/td").text
    spatk  = infoDriver.find_element_by_xpath(".//table[@class='stats']/tbody/tr[5]/td").text
    spdef = infoDriver.find_element_by_xpath(".//table[@class='stats']/tbody/tr[6]/td").text
    spd = infoDriver.find_element_by_xpath(".//table[@class='stats']/tbody/tr[7]/td").text
    stats = [hp, atk, defense, spatk, spdef, spd]
    print(stats)
    return Pokemon(pkmnName, None, None, None, None, type1, type2, None, stats)

def getMoveInfo(infoDriver, moveName):
    trimmedMoveName = moveName.replace(" ", "")
    infoDriver.get("https://dex.pokemonshowdown.com/moves/{}".format(trimmedMoveName))
    moveType = infoDriver.find_element_by_xpath(".//dl[@class='movetypeentry']/dd/a[1]").text
    moveCat = infoDriver.find_element_by_xpath(".//dl[@class='movetypeentry']/dd/a[2]").text
    if moveCat.lower() == "status":
        movePow = None
    else:
        movePow = infoDriver.find_element_by_xpath(".//dl[@class='powerentry']/dd/strong").text
    moveAcc = infoDriver.find_element_by_xpath(".//dl[@class='accuracyentry']/dd").text
    return Move(moveName, moveType, moveCat, movePow, moveAcc)

#Log-in to showdown (maybe make functions)
#TODO: Do i want notifications on or off?
def getDriver():
    profile = webdriver.FirefoxProfile()
    profile.set_preference("dom.webnotifications.enabled", False)
    driver = webdriver.Firefox(profile)
    driver.implicitly_wait(10)
    return driver

def login(driver, username, password):
    driver.get("http://play.pokemonshowdown.com")
    driver.find_element_by_name("login").click()
    driver.find_element_by_name("username").send_keys(username)
    driver.find_element_by_name("username").send_keys(Keys.ENTER)
    driver.find_element_by_name("password").send_keys(password)
    driver.find_element_by_name("password").send_keys(Keys.ENTER)
    time.sleep(1) #will prompt for username if login does not wait for a sec

def getActiveMoves(driver):
    moves = []
    for x in range(4):
        if elementExists(driver, ".//div[@class='movemenu']/button[{}]".format(x + 1)):
            moveButton = driver.find_element_by_xpath(".//div[@class='movemenu']/button[{}]".format(x + 1))
        elif elementExists(driver, ".//div[@class='movebuttons-noz']/button[{}]"):
            moveButton = driver.find_element_by_xpath(".//div[@class='movebuttons-noz']/button[{}]".format(x + 1))
        hover = ActionChains(driver).move_to_element(moveButton)
        hover.perform()
        moveName = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/h2").text
        moveType = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/h2/img[1]").get_attribute("alt")
        moveCat = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/h2/img[2]").get_attribute("alt")
        movePow = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/p[1]").text.split(':')[1].strip()
        moveAcc = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/p[2]").text.split(':')[1].strip()
        moves.append(Move(moveName, moveType, moveCat, movePow, moveAcc))
    return moves

#todo: fails for pokemon with less than four moves (ditto, unown, etc)
#assumes required pokemon is hovered over
def getBenchedMoves(driver, infoDriver):
    moves = []
    movesListText = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/p[4]").text
    movesList = movesListText.splitlines()
    for x in movesList:
        moveName = x[2:].strip()
        moves.append((getMoveInfo(infoDriver, moveName)))
    return moves

#expects all pokemon to be lvl 10-99
def getMyPokemon(driver, infoDriver, trainer):
    for x in range(trainer.maxMons):
        switchbutton = driver.find_element_by_xpath(".//div[@class='switchmenu']/button[{}]".format(x+1))
        hover = ActionChains(driver).move_to_element(switchbutton)
        hover.perform()
        nickname = None
        #get NAME
        if(elementExists(driver, ".//div[@id='tooltipwrapper']/div/div/h2/span")):
            name = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/h2/span").get_attribute("title")
            #need nickname, since this case covers pokemon with forms, whose switch button is their base name
            nicknameText = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/h2/span").text
            nickname = nicknameText.split('(')[0].strip()
        else:
            name = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/h2").text[:-4]
        #get ITEM and ABILITY
        itemAbilityText = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/p[2]").text
        itemAbilityPair = itemAbilityText.split('/')
        if len(itemAbilityPair) == 2:
            #get ITEM
            colonIndex =  itemAbilityPair[1].find(":")
            item = itemAbilityPair[1][colonIndex + 2:] #skip the colon and the space after
            #get ABILITY
            colonIndex = itemAbilityPair[0].find(":")
            ability = itemAbilityPair[0][colonIndex + 2:-1]
        else:
            item = None
            ability = "Pickup"
        #get TYPE1
        type1 = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/h2/img[1]").get_attribute("alt")
        if type1 == "M" or type1 == "F":
            gender = type1
            type1 = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/h2/img[2]").get_attribute("alt")
        else:
            gender = None
        #get TYPE2
        if gender == None:
            if elementExists(driver, ".//div[@id='tooltipwrapper']/div/div/h2/img[2]"):
                type2 = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/h2/img[2]").get_attribute("alt")
            else:
                type2 = None
        else:
            if elementExists(driver, ".//div[@id='tooltipwrapper']/div/div/h2/img[3]"):
                type2 = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/h2/img[3]").get_attribute("alt")
            else:
                type2 = None
        #get LEVEL
        level = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/h2/small").text[1:]
        #get STATS
        #get HP
        hpText = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/p[1]").text
        hp = hpText.split('/')[1][:-1]
        #get rest of stats
        statsText = driver.find_element_by_xpath(".//div[@id='tooltipwrapper']/div/div/p[3]").text
        statsList = statsText.split(' ') #returns atkstat + Atk + / + defstat + Def + / +
        stats = [hp, statsList[0], statsList[3], statsList[6], statsList[9], statsList[12]]
        #get MOVES
        if x == 0:
            moves = getActiveMoves(driver)
        else:
            moves = getBenchedMoves(driver, infoDriver)
        mon = Pokemon(name, nickname, item, ability, moves, type1, type2, level, stats)
        trainer.addKnownMon(mon)

#expects all pokemon to be lvl 10-99
def getOpponentsPokemon(driver, infoDriver, trainer):
    nameLevelText = driver.find_element_by_xpath(".//div[@class='statbar lstatbar']/strong").text
    name = nameLevelText[:-4]
    lvl = nameLevelText[-2:]
    mon = getPokemonInfo(infoDriver, name)
    mon.setLevel(lvl)
    trainer.addKnownMon(mon)
    print("in get opponents pokemon")
    print(trainer)
    print(trainer.knownMons[0])
    return mon

def debugPopup(driver):
    xpathsToCheck = [".//div[@id='tooltipwrapper']/div/div/h2", ".//div[@id='tooltipwrapper']/div/div/h2/span", ".//*[@class='battle-nickname-foe']", ".//div[@id='tooltipwrapper']/div/div/p[2]",
                     ".//div[@id='tooltipwrapper']/div/div/h2/img[1]", ".//div[@id='tooltipwrapper']/div/div/h2/small", ".//div[@id='tooltipwrapper']/div/div/p[3]"]
    switchbutton = driver.find_element_by_xpath(".//div[@class='switchmenu']/button[1]")
    hover = ActionChains(driver).move_to_element(switchbutton)
    hover.perform()
    for x in(xpathsToCheck):
        if elementExists(driver, x):
            print("{} s there".format(x))
        else:
            print("{} is not there".format(x))

#checks whatdo's existence to handle picking invalid attack (i.e. choice band, encore, taunt)
def makeMove(driver, me, scrub, battleStyle):
    #buffer in case actions not available yet
    while actionSucceeded(driver):
        time.sleep(1)
    for x in range(10):
        if actionSucceeded(driver):
            break
        useMove = battleStyle.makeMove(me, scrub)
        attack(driver, useMove)
        time.sleep(1)
    while not actionSucceeded(driver): #will not go through this if previous attempt succeeded
        useMove = randomMakeMove(me, scrub)
        attack(driver, useMove)
        time.sleep(1)
    print("attacked with move {}".format(useMove.name))
    time.sleep(1)

def waitForNextTurn(driver, infoDriver, me, scrub, bs, battleStyle):
    triedSwitching = False
    while not elementExists(driver, ".//div[@class='battle-log']/div[2]/h2[{}]".format(bs.turn+1)):
        #did game end?
        if isGameOver(driver):
            return
        #check if need to switch
        if elementExists(driver, ".//div[@class='whatdo']"):
            #did a pokemon die?
            whatHappened(driver, infoDriver, me, scrub, bs)
            #switch the next pokemon, make this random ffs
            if triedSwitching:
                mon = randomMakeSwitch(me, scrub)
            else:
                mon = battleStyle.makeSwitch(me, scrub)
                triedSwitching = True
            switch(driver, me, mon)
        time.sleep(1)
    bs.turn += 1
    return bs.turn + 1

#get log for data of turn specified, return where it left off
def whatHappened(driver, infoDriver, me, scrub, bs):
    atNextTurn = False
    while not atNextTurn:
        nextText = driver.find_element_by_xpath(".//*[@class='battle-history'][{}]".format(bs.lastTurnIndex)).text
        print("{}".format(nextText))
        #did anyone faint?
        if "fainted!" in nextText:
            if "The opposing" in nextText:
                scrub.faintActive()
            else:
                me.faintActive()
        #did anyone switch?
        #if "Go!" in nextText:
            #do nothing, taken care of when we switch
        if "sent out" in nextText:
            mon = getOpponentsPokemon(driver, infoDriver, scrub)
            scrub.switch(mon)
        if nextText == "Turn {}".format(bs.turn) or not elementExists(driver, ".//*[@class='battle-history'][{}]".format(bs.lastTurnIndex + 1)):
            atNextTurn = True
        bs.lastTurnIndex += 1
    return

#do later
def turnOffTheFuckingMusic(driver):
    driver.find_element_by_name("openSounds").click()
    for x in range(50):
        driver.find_element_by_name("effectvolume").send_keys(Keys.LEFT)
    for x in range(50):
        driver.find_element_by_name("musicvolume").send_keys(Keys.LEFT)
    for x in range(50):
        driver.find_element_by_name("notifvolume").send_keys(Keys.LEFT)
    return


class BattleState:
    def __init__(self):
        self.turn = 1
        self.lastTurnIndex = 3


def battle(driver, infoDriver, battleStyle):
    me = Trainer()
    scrub = Trainer()
    bs = BattleState()
    getMyPokemon(driver, infoDriver, me)
    getOpponentsPokemon(driver, infoDriver, scrub)
    #print(me)
    #print(scrub)
    while not isGameOver(driver): #need to elegantly check this in steps
        #printBothActiveMons(me, scrub)
        makeMove(driver, me, scrub, battleStyle)
        waitForNextTurn(driver, infoDriver, me, scrub, bs, battleStyle)
        whatHappened(driver, infoDriver, me, scrub, bs)

def getBattleStyle(key):
    styleDictionary = {
        'random':getRandomBattleStyle,
        'basic':getBtaBattleStyle
    }
    return styleDictionary.get(key)()


#this is gonna be a lot of refactoring...
def run(filename):
    username = 'insertUsernameHere'
    password = 'insertPasswordHere'
    challengeUsername = 'insertChallengeUserHere'
    battleMode = 'accept'
    battleStyleKey = 'random'
    try:
        with open(filename) as json_data:
            data = json.load(json_data)
        username = data['username']
        password = data['password']
        challengeUsername = data['challengeUser']
        battleMode = data['battleMode']
        battleStyleKey = data['battleStyle']
    except Exception as e:
        print("Error importing: {}".format(e))
    battleStyle = getBattleStyle(battleStyleKey)
    infoDriver = getDriver()
    driver = getDriver()
    login(driver, username, password)
    turnOffTheFuckingMusic(driver)
    if battleMode == "accept":
        acceptChallenge(driver)
    if battleMode == "challenge":
        challengeUser(driver, challengeUsername)
    battle(driver, infoDriver, battleStyle)
    infoDriver.close()
    driver.close()

#todo: make roar work
#todo: 1 atk pkmn
#todo: track megas somehow
#todo: battle styles
#todo: taunts