def add(x,y):
    return tuple(map(lambda ((a,b)): a+b, zip(x,y)))

def mult(a,x):
    return tuple(map(lambda i: a*i, x))

class RiskProbabilityCalculator:

    def __init__(self):
        def generate_dice_rolls(numDice):
            if numDice <= 0:
                return []
            diceRolls = [[(i,) for i in range(1,7)] for die in range(0,numDice)]
            diceRolls = reduce(lambda diceRolls, dieRolls:
                               [x + y for x in diceRolls for y in dieRolls], diceRolls)
            return diceRolls

        self.diceRolls = [generate_dice_rolls(i) for i in range(0, 4)]
        self.probabilities = self.generate_probabilities()
        pass

    def transition((num_attackers,num_defenders), (num_attackers_lost, num_defenders_lost)):
        print (num_attackers,num_defenders), (num_attackers_lost, num_defenders_lost)

    def computePTransition((num_attackers,num_defenders), (num_attackers_lost, num_defenders_lost)):
        pass

    def outcome(self, attackers, defenders):
        total_casualties = min(len(attackers), len(defenders))
        attackers = sorted(attackers, reverse=True)
        defenders = sorted(defenders, reverse=True)
        defenders_lost = sum([(1 if attacker > defender else 0) for (attacker, defender) in zip(attackers, defenders)])
        attackers_lost = total_casualties - defenders_lost
        return attackers_lost, defenders_lost

    def computeProb(self, (num_attackers, num_defenders), (attackers_lost, defenders_lost)):
        attackerRolls = self.diceRolls[min(num_attackers, 3)]
        defenderRolls = self.diceRolls[min(num_defenders, 2)]
        numEvents = sum([1 if self.outcome(attackers, defenders) == (attackers_lost, defenders_lost) else 0
             for attackers in attackerRolls
             for defenders in defenderRolls])
        return float(numEvents) / (len(attackerRolls) * len(defenderRolls))

    def generate_probabilities(self):
        probabilities = {}
        for num_attackers in range(1,4):
            for num_defenders in range(1,3):
                total_casualties = min(num_attackers, num_defenders)
                for attackers_lost in range(0, total_casualties+1):
                    defenders_lost = total_casualties-attackers_lost
                    given = (num_attackers, num_defenders)
                    outcome = (attackers_lost, defenders_lost)
                    probabilities[(given, outcome)] = self.computeProb(given, outcome)
        return probabilities

    def probability_when_attacking(self, (attackers_lost, defenders_lost), (num_attackers, num_defenders)):
        return self.probabilities[(num_attackers, num_defenders), (attackers_lost, defenders_lost)]

    def expected_armies_lost_when_attacking(self, num_attackers, num_defenders):
        result = (0.0, 0.0)
        numLosses = min(num_attackers, num_defenders)
        # E = sum P(attackers_lost,defenders_lost) * (attackers_lost, defenders_lost)
        for (attackers_lost, defenders_lost) in [(attackers_lost, defenders_lost) for attackers_lost in range(0,3) for defenders_lost in range(0,3)]:
            if attackers_lost + defenders_lost != numLosses:
                continue
            prob = self.probability_when_attacking((attackers_lost, defenders_lost), (num_attackers, num_defenders))
            result = add(result, mult(prob, (attackers_lost, defenders_lost)))
        return result

    def probability_when_attacking_territory(self, (attackers_left, defenders_left), (num_armies_in_attacking_territory, num_armies_in_defending_territory, attacking_strategy)):
        def Sa(num_armies_in_attacking_territory, num_armies_in_defending_territory):
            return min(3, num_armies_in_attacking_territory - 1, attacking_strategy(num_armies_in_attacking_territory, num_armies_in_defending_territory)) if (num_armies_in_defending_territory > 0 and num_armies_in_attacking_territory > 1) else 0
        a1 = num_armies_in_attacking_territory # initial number of units in attacking territory
        d1 = num_armies_in_defending_territory # initial number of units in defending territory
        a2 = attackers_left # number of attacking units left
        d2 = defenders_left # number of defending units left
        p = [[0.0]*(d1 - d2 + 1) for i in range(a1 - a2 + 1)]
        p[0][0] = 1 if Sa(a2, d2) == 0 else 0
        
        for i in range(0, a1 - a2 + 1): # i = num units in attacking territory - attackers_left
            for j in range(0, d1 - d2 + 1): # j = num units in defending territory - defenders_left
                if (i,j) == (0,0):
                    continue
                a = i + a2 # number of units in attacking territory
                d = j + d2 # number of units in defending territory
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
                    prob += self.probability_when_attacking((la, ld), (na, nd)) * p[a - la - a2][d - ld - d2]
                p[i][j] = prob
        return p[a1 - a2][d1 - d2]

    def probability_of_conquering_territory(self, (num_armies_in_attacking_territory, num_armies_in_defending_territory, attacking_strategy)):
        a1 = num_armies_in_attacking_territory
        d1 = num_armies_in_defending_territory
        return sum([self.probability_when_attacking_territory((a,0),(a1,d1,attacking_strategy)) for a in range(2,a1+1)])



