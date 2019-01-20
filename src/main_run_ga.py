from ga.optimize import run_genetics
import json
import sys


CONFIGURATION = 'configuration.json'


if __name__ == '__main__':
    sys.setrecursionlimit(10000)

    with open(CONFIGURATION) as f:
        data = json.load(f)

    if 'simulation' not in data or 'map' not in data or 'ga' not in data:
        print('Configuration does not contain all parameters')
        sys.exit(0)
    
    # Run
    run_genetics(map=data['map'], hyperparameters=data['ga'], simulation=data['simulation'])
