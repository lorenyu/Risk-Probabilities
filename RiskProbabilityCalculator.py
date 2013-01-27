def add(x,y):
    return tuple(map(lambda ((a,b)): a+b, zip(x,y)))

def mult(a,x):
    return tuple(map(lambda i: a*i, x))

class RiskProbabilityCalculator:

    def __init__(self):
        def generateDiceRolls(numDice):
            if numDice <= 0:
                return []
            diceRolls = [[(i,) for i in range(1,7)] for die in range(0,numDice)]
            diceRolls = reduce(lambda diceRolls, dieRolls:
                               [x + y for x in diceRolls for y in dieRolls], diceRolls)
            return diceRolls

        self.diceRolls = [generateDiceRolls(i) for i in range(0, 4)]
        self.probabilities = self.generateProbabilities()
        pass

    def transition((numAttackers,numDefenders), (numAttackersLost, numDefendersLost)):
        print (numAttackers,numDefenders), (numAttackersLost, numDefendersLost)

    def computePTransition((numAttackers,numDefenders), (numAttackersLost, numDefendersLost)):
        pass

    def outcome(self, attackers, defenders):
        totalCasualties = min(len(attackers), len(defenders))
        attackers = sorted(attackers, reverse=True)
        defenders = sorted(defenders, reverse=True)
        defendersLost = sum([(1 if attacker > defender else 0) for (attacker, defender) in zip(attackers, defenders)])
        attackersLost = totalCasualties - defendersLost
        return attackersLost, defendersLost

    def computeProb(self, (numAttackers, numDefenders), (attackersLost, defendersLost)):
        attackerRolls = self.diceRolls[min(numAttackers, 3)]
        defenderRolls = self.diceRolls[min(numDefenders, 2)]
        numEvents = sum([1 if self.outcome(attackers, defenders) == (attackersLost, defendersLost) else 0
             for attackers in attackerRolls
             for defenders in defenderRolls])
        return float(numEvents) / (len(attackerRolls) * len(defenderRolls))

    def generateProbabilities(self):
        probabilities = {}
        for numAttackers in range(1,4):
            for numDefenders in range(1,3):
                totalCasualties = min(numAttackers, numDefenders)
                for attackersLost in range(0, totalCasualties+1):
                    defendersLost = totalCasualties-attackersLost
                    given = (numAttackers, numDefenders)
                    outcome = (attackersLost, defendersLost)
                    probabilities[(given, outcome)] = self.computeProb(given, outcome)
        return probabilities

    def prob(self, (numAttackers, numDefenders), (attackersLost, defendersLost)):
        return self.probabilities[(numAttackers, numDefenders), (attackersLost, defendersLost)]

    def expected(self, numAttackers, numDefenders):
        result = (0.0, 0.0)
        numLosses = min(numAttackers, numDefenders)
        # E = sum P(attackersLost,defendersLost) * (attackersLost, defendersLost)
        for (attackersLost, defendersLost) in [(attackersLost, defendersLost) for attackersLost in range(0,3) for defendersLost in range(0,3)]:
            if attackersLost + defendersLost != numLosses:
                continue
            prob = self.prob((numAttackers, numDefenders),(attackersLost, defendersLost))
            result = add(result, mult(prob, (attackersLost, defendersLost)))
        return result

    def p2(self, (attackersLeft, defendersLeft), (attackingCountry, defendingCountry, attackingStrategy)):
        def Sa(attackingCountry, defendingCountry):
            return min(3, attackingCountry - 1, attackingStrategy(attackingCountry, defendingCountry)) if (defendingCountry > 0 and attackingCountry > 1) else 0
        a1 = attackingCountry # initial number of units in attacking country
        d1 = defendingCountry # initial number of units in defending country
        a2 = attackersLeft # number of attacking units left
        d2 = defendersLeft # number of defending units left
        p = [[0.0]*(d1 - d2 + 1) for i in range(a1 - a2 + 1)]
        p[0][0] = 1 if Sa(a2, d2) == 0 else 0
        
        for i in range(0, a1 - a2 + 1): # i = num units in attacking country - attackersLeft
            for j in range(0, d1 - d2 + 1): # j = num units in defending country - defendersLeft
                if (i,j) == (0,0):
                    continue
                a = i + a2 # number of units in attacking country
                d = j + d2 # number of units in defending country
                na = Sa(a, d) # num attackers
                if na <= 0:
                    continue
                nd = min(d, 2) # num defenders
                n = min(na, nd) # total casualties
                #print a, d, '\t', na, nd

                prob = 0.0
                for la in range(0,n+1): # la = attackers lost
                    ld = n - la # ld = defenders lost
                    if (a - la - a2 < 0) or (d - ld - d2 < 0):
                        continue
                    #print '\t', la, ld
                    prob += self.prob((na, nd), (la, ld)) * p[a - la - a2][d - ld - d2]
                p[i][j] = prob
        return p[a1 - a2][d1 - d2]

    def p2win(self, (attackingCountry, defendingCountry, attackingStrategy)):
        a1 = attackingCountry
        d1 = defendingCountry
        return sum([self.p2((a,0),(a1,d1,attackingStrategy)) for a in range(2,a1+1)])
