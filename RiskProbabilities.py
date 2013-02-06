from RiskProbabilityCalculator import RiskProbabilityCalculator
import argparse
import strategies

p = RiskProbabilityCalculator()

def attack(args):
    print p.expected_armies_lost_when_attacking(args.num_attackers, args.num_defenders)

def win_territory(args):
    if args.strategy == 'all-in':
        strategy = strategies.all_in
    elif args.strategy == 'advantage':
        strategy = strategies.advantage
    elif args.strategy == 'outnumber':
        strategy = strategies.outnumber
    else:
        strategy = strategies.all_in
    print p.probability_of_conquering_territory((args.num_attackers, args.num_defenders, strategy))

def win_territory_path(args):
    print p.probability_of_conquering_territory_path((args.num_attackers, args.num_defenders))

def expected_territory_path(args):
    print p.expected_armies_left_when_attacking_territory_path((args.num_attackers, args.num_defenders))

parser = argparse.ArgumentParser(description='Compute probabilities within the game of Risk.')

subparsers = parser.add_subparsers()
attack_parser = subparsers.add_parser('single-attack', help='Compute expected value of (attacking units lost, defending units lost) by attacking a territory once')
attack_parser.add_argument('num_attackers', type=int, help='Number of units participating in the attack', choices=range(1,3+1))
attack_parser.add_argument('num_defenders', type=int, help='Number of units defending', choices=range(1,2+1))
attack_parser.set_defaults(func=attack)

win_territory_parser = subparsers.add_parser('win-territory', help='Compute probability of winning a territory given a particular strategy')
win_territory_parser.add_argument('num_attackers', type=int, help='Number of units in attacking territory')
win_territory_parser.add_argument('num_defenders', type=int, help='Number of units in defending territory')
win_territory_parser.add_argument('-s', '--strategy', choices=['all-in', 'advantage', 'outnumber'], default='all-in', help="""Attacking strategy.

    all-in:     Attack with as many units as possible until victory or unable to attack.
    advantage:  Attack with as many units as possible as long as the number of units in the attacking territory, excluding the 1 unit you have to leave in the territory, outnumbers the number of units in the defending territory.""")
win_territory_parser.set_defaults(func=win_territory)

win_territory_path_parser = subparsers.add_parser('win-territory-path', help='Compute probability of winning a territory path')
win_territory_path_parser.add_argument('num_attackers', type=int, help='Number of units in attacking territory')
win_territory_path_parser.add_argument('num_defenders', type=int, nargs='*', help='Number of units in defending territories in order of territory path')
win_territory_path_parser.set_defaults(func=win_territory_path)

expected_territory_path_parser = subparsers.add_parser('expected-territory-path', help='Compute expected number of armies remaining when attacking a territory path')
expected_territory_path_parser.add_argument('num_attackers', type=int, help='Number of units in attacking territory')
expected_territory_path_parser.add_argument('num_defenders', type=int, nargs='*', help='Number of units in defending territories in order of territory path')
expected_territory_path_parser.set_defaults(func=expected_territory_path)

args = parser.parse_args()
args.func(args)
