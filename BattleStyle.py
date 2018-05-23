#Imports
from HelperFunctions import *
import time
import random


class BattleStyle:
    def __init__(self, makeMoveFunction, makeSwitchFunction):
        self.makeMove = makeMoveFunction
        self.makeSwitch = makeSwitchFunction


#########################
###Random Battle Style###
#########################

def getRandomBattleStyle():
    return BattleStyle(randomMakeMove, randomMakeSwitch)

#randomly makes move
def randomMakeMove(me, scrub):
    if me.getActive().item is not None and "choice" in me.getActive().item.lower() and me.getActive().lastUsedMove is not None:
        return me.getActive().lastUsedMove
    else:
        return me.getActive().moves[random.randint(0, 3)]

#randomly makes switch
def randomMakeSwitch(me, scrub):
    mon = me.remainingPokemon()[random.randint(0, len(me.remainingPokemon()) - 1)]
    while mon.active:
        mon = me.remainingPokemon()[random.randint(0, len(me.remainingPokemon()) - 1)]
    return mon


################################
###Basic Type Advantage Style###
################################

def getBtaBattleStyle():
    return BattleStyle(btaMakeMove, btaMakeSwitch)

#uses the move which does the most damage. If only status moves are available, randomly selects one
def btaMakeMove(me, scrub):
    maxPower = 0
    maxMove = None
    for m in me.getActive().moves:
        print("checking {}".format(m))
        if m.cat.lower() != "status":
            if (me.getActive().getEffectivePower(m) * Move.effectiveness(None, m.type, scrub.getActive().type1, scrub.getActive().type2)) > maxPower:
                print("{} is better than {}. Considering using {}".format(m, maxMove, m))
                maxPower = me.getActive().getEffectivePower(m) * Move.effectiveness(None, m.type, scrub.getActive().type1, scrub.getActive().type2)
                maxMove = m
    if maxPower > 20:
        print("Decided to use {}".format(maxMove))
        return maxMove
    else:
        return randomMakeSwitch(me, scrub)

def btaMakeSwitch(me, scrub):
    #for now, which of our pokemon is most effective with stab attacks against the opponents active pokemon
    maxEffectiveness = 0
    maxMon = None
    for mon in me.remainingPokemon(): #currently uses how strong mon is against enemy, not how strong he is against you
        if not mon.active:
            if mon.monMatchup(scrub.getActive())[0] >= maxEffectiveness:
                maxEffectiveness = mon.monMatchup(scrub.getActive())[0]
                maxMon = mon
    return maxMon
