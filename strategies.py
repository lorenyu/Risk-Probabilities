def all_in(numUnitsInAttackingCountry, numUnitsInDefendingCountry):
    return min(numUnitsInAttackingCountry - 1, 3) if numUnitsInDefendingCountry > 0 else 0

def advantage(numUnitsInAttackingCountry, numUnitsInDefendingCountry):
    return min(numUnitsInAttackingCountry - 1, 3) if (numUnitsInAttackingCountry - 1 > min(numUnitsInDefendingCountry, 2)) and (numUnitsInDefendingCountry > 0) else 0

def outnumber(numUnitsInAttackingCountry, numUnitsInDefendingCountry):
    return min(numUnitsInAttackingCountry - 1, 3) if (numUnitsInAttackingCountry - 1 > numUnitsInDefendingCountry) and (numUnitsInDefendingCountry > 0) else 0

