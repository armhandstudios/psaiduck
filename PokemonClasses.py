#not used atm don't play yaself
class HeldItem:

    def __init__(self, nm):
        self.name = nm


class Move:

    def __init__(self, nm, tp, cat, pow, acc):
        self.name = nm
        self.type = tp
        self.cat = cat
        self.power = pow
        self.accuracy = acc
        #effects = []    #list of tuples of effect/chance pairs
        #print(self)

    def __str__(self):
        return "{}, {}, {}, {}, {}".format(self.name, self.type, self.cat, self.power, self.accuracy)

    def printFullInfo(self):
        print(self.name)
        print(self.type)
        print(self.power)
        print(self.accuracy)
        print(self.cat)

    #prolly wanna change params to just 1 pokemon rather than typename and 2 ptypes
    def effectiveness(self, movetype, ptype1, ptype2):
        typeIndices = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying",
                       "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]
        typeMatchups = [[1,1,1,1,1,1,1,1,1,1,1,1,.5,0,1,1,.5,1],
                        [1,.5,.5,1,2,2,1,1,1,1,1,2,.5,1,.5,1,2,1],
                        [1,2,.5,1,.5,1,1,1,2,1,1,1,2,1,.5,1,1,1],
                        [1,1,2,.5,.5,1,1,1,0,2,1,1,1,1,.5,1,1,1],
                        [1,.5,2,1,.5,1,1,.5,2,.5,1,.5,2,1,.5,1,.5,1],
                        [1,.5,.5,1,2,.5,1,1,2,2,1,1,1,1,2,1,.5,1],
                        [2,1,1,1,1,2,1,.5,1,.5,.5,.5,2,0,1,2,2,.5],
                        [1,1,1,1,2,1,1,.5,.5,1,1,1,.5,.5,1,1,0,2],
                        [1,2,1,2,.5,1,1,2,1,0,1,.5,2,1,1,1,2,1],
                        [1,1,1,.5,2,1,2,1,1,1,1,2,.5,1,1,1,.5,1],
                        [1,1,1,1,1,1,2,2,1,1,.5,1,1,1,1,0,.5,1],
                        [1,.5,1,1,2,1,.5,.5,1,.5,2,1,1,.5,1,2,.5,.5],
                        [1,2,1,1,1,2,.5,1,.5,2,1,2,1,1,1,1,.5,1],
                        [0,1,1,1,1,1,1,1,1,1,2,1,1,2,1,.5,1,1],
                        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,1,.5,0],
                        [1,1,1,1,1,1,.5,1,1,1,2,1,1,2,1,.5,1,.5],
                        [1,.5,.5,.5,1,2,1,1,1,1,1,1,2,1,1,1,.5,2],
                        [1,.5,1,1,1,1,2,.5,1,1,1,1,1,1,2,2,.5,1]]
        if ptype2 == None:
            return typeMatchups[typeIndices.index(movetype.lower())][typeIndices.index(ptype1.lower())]
        else:
            return typeMatchups[typeIndices.index(movetype.lower())][typeIndices.index(ptype1.lower())]*typeMatchups[typeIndices.index(movetype.lower())][typeIndices.index(ptype2.lower())]


class Pokemon:

    #for own mons
    def __init__(self, pname, pnname, pitem, pability, pmoves, ptype1, ptype2, plevel, pstats):
        self.name = pname
        self.nickname = pnname
        self.item = pitem
        self.ability = pability
        self.moves = pmoves
        self.type1 = ptype1
        self.type2 = ptype2
        self.level = plevel
        self.stats = pstats
        self.pctHP = 100
        self.statBoosts = []
        self.active = False
        self.lastUsedMove = None

        if self.nickname is None:
            self.nickname = self.name

    def __str__(self):
        return "{}, {}, {}, {}, {}, {}, {}, {}".format(self.name, self.nickname, self.item, self.ability, self.type1, self.type2, self.level, self.stats)

    def setLevel(self, level):
        self.level = level

    def setActive(self, value):
        self.active = value

    def useMove(self, move):
        self.lastUsedMove = move

    def getEffectivePower(self, move):
        if move.type == self.type1 or move.type == self.type2:
            print(move.power)
            return float(move.power) * 1.5
        else:
            return float(move.power)

    #returns two values, the first is how effective you are against the opponent, the second is how effective it is against you
    #picks the max offensive types
    def monMatchup(self, opponent):
        typeIndices = ["normal", "fire", "water", "electric", "grass", "ice", "fighting", "poison", "ground", "flying",
                       "psychic", "bug", "rock", "ghost", "dragon", "dark", "steel", "fairy"]
        typeMatchups = [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, .5, 0, 1, 1, .5, 1],
                        [1, .5, .5, 1, 2, 2, 1, 1, 1, 1, 1, 2, .5, 1, .5, 1, 2, 1],
                        [1, 2, .5, 1, .5, 1, 1, 1, 2, 1, 1, 1, 2, 1, .5, 1, 1, 1],
                        [1, 1, 2, .5, .5, 1, 1, 1, 0, 2, 1, 1, 1, 1, .5, 1, 1, 1],
                        [1, .5, 2, 1, .5, 1, 1, .5, 2, .5, 1, .5, 2, 1, .5, 1, .5, 1],
                        [1, .5, .5, 1, 2, .5, 1, 1, 2, 2, 1, 1, 1, 1, 2, 1, .5, 1],
                        [2, 1, 1, 1, 1, 2, 1, .5, 1, .5, .5, .5, 2, 0, 1, 2, 2, .5],
                        [1, 1, 1, 1, 2, 1, 1, .5, .5, 1, 1, 1, .5, .5, 1, 1, 0, 2],
                        [1, 2, 1, 2, .5, 1, 1, 2, 1, 0, 1, .5, 2, 1, 1, 1, 2, 1],
                        [1, 1, 1, .5, 2, 1, 2, 1, 1, 1, 1, 2, .5, 1, 1, 1, .5, 1],
                        [1, 1, 1, 1, 1, 1, 2, 2, 1, 1, .5, 1, 1, 1, 1, 0, .5, 1],
                        [1, .5, 1, 1, 2, 1, .5, .5, 1, .5, 2, 1, 1, .5, 1, 2, .5, .5],
                        [1, 2, 1, 1, 1, 2, .5, 1, .5, 2, 1, 2, 1, 1, 1, 1, .5, 1],
                        [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 2, 1, .5, 1, 1],
                        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, .5, 0],
                        [1, 1, 1, 1, 1, 1, .5, 1, 1, 1, 2, 1, 1, 2, 1, .5, 1, .5],
                        [1, .5, .5, .5, 1, 2, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, .5, 2],
                        [1, .5, 1, 1, 1, 1, 2, .5, 1, 1, 1, 1, 1, 1, 2, 2, .5, 1]]
        #maxEffectiveness = 0
        #maxOppEffectiveness = 0
        #check first type matchup against opponents types
        maxEffectiveness = typeMatchups[typeIndices.index(self.type1.lower())][typeIndices.index(opponent.type1.lower())]
        if opponent.type2 is not None:
            maxEffectiveness *= typeMatchups[typeIndices.index(self.type1.lower())][typeIndices.index(opponent.type2.lower())]
        if self.type2 is not None:
            curEffectiveness = typeMatchups[typeIndices.index(self.type1.lower())][typeIndices.index(opponent.type1.lower())]
            if opponent.type2 is not None:
                curEffectiveness *= typeMatchups[typeIndices.index(self.type1.lower())][typeIndices.index(opponent.type2.lower())]
            if curEffectiveness > maxEffectiveness:
                maxEffectiveness = curEffectiveness

        maxOppEffectiveness = typeMatchups[typeIndices.index(opponent.type1.lower())][typeIndices.index(self.type1.lower())]
        if self.type2 is not None:
            maxOppEffectiveness *= typeMatchups[typeIndices.index(opponent.type1.lower())][typeIndices.index(self.type2.lower())]
        if opponent.type2 is not None:
            curEffectiveness = typeMatchups[typeIndices.index(opponent.type1.lower())][typeIndices.index(self.type1.lower())]
            if self.type2 is not None:
                curEffectiveness *= typeMatchups[typeIndices.index(opponent.type1.lower())][typeIndices.index(self.type2.lower())]
            if curEffectiveness > maxOppEffectiveness:
                maxOppEffectiveness = curEffectiveness

        return maxEffectiveness, maxOppEffectiveness




class FieldSide:
    hazards = []
    tailwind = None
    reflect = None
    lightScreen = None
    auroraVeil = None


class Field:
    weather = None
    weatherTurns = None
    terrain = None
    terrainTurns= None
    trickRoom = None


class Trainer:

    def __init__(self):
        self.maxMons = 6
        self.monsLeft = 6
        self.knownMons = []
        self.deadMons = []

    def addKnownMon(self, mon):
        self.knownMons.append(mon)
        #first mon sent out starts active
        if len(self.knownMons) == 1:
            mon.setActive(True)
        print(mon)

    def getActive(self):
        for x in self.knownMons:
            if x.active:
                return x
        return None

    def switch(self, mon):
        self.getActive().setActive(False)
        mon.setActive(True)

    def remainingPokemon(self):
        rem = []
        print("Remaining:")
        for x in self.knownMons:
            if x not in self.deadMons:
                rem.append(x)
                print(x)
        return rem

    def faintActive(self):
        self.deadMons.append(self.getActive())
        self.getActive().pctHP = 0
        print("{} fainted".format(self.getActive()))





