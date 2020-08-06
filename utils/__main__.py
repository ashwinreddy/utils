import utils
import matplotlib.pyplot as plt
import argparse
from pathlib import Path
from rich import print
import json
import pandas as pd
from IPython import embed




def exp_results(directory, priority=0):
    if priority == 0:
        search = "**/progress.csv"
    else:
        search = "**/*"
    
    path = Path().absolute() / Path(directory)
    experiment_contents = path.glob(search)
    
    experiment_results = {}

    for path in experiment_contents:
        obj = None
        if path.suffix == ".json" and priority > 0:
            try:
                obj = json.loads(path.open().read())
            except json.decoder.JSONDecodeError as e:
                pass
                #print("Could not parse", path)
        elif path.suffix == ".csv":
            obj = utils.Table.from_csv(str(path.absolute()))
        
        if obj is not None:
            experiment_results[path.name] = obj

    exp = utils.Experiment(experiment_results)
    # exp.table.process(utils.Experiment.default_rescales)
    return exp
    

def main(args):
    experiments = []
    for directory in args.directories:
        experiments.append(exp_results(directory, 1))
    
    #fig = plt.figure()

    if args.interactive:
        if len(experiments) == 1:
            exp = experiments[0]
        embed()
    else:
        metric = 'training/env_infos/distance_to_target-last-mean'
        for exp in experiments:
            plt.plot(exp.table[exp.x_axis], exp.table[metric], label = input(f"Label for {exp.name}? ") or exp.name.split("-")[-1])


    #ax = experiments[0].plot()
    #experiments[1].plot(ax = ax)

        params = experiments[0]['params.json']['environment_params']['evaluation']
        domain, task = params['domain'], params['task']
        title = f"{domain}-{task}" 

        plt.title(title)
        plt.ylabel(metric)

        plt.legend()

        if args.save:
            import utils.plotting
            utils.plotting.quicksave()
        else:
            plt.show()

    #plt.show()

    #table = exp["progress.csv"]
    #table.process(bb.default_rescales)
    #from IPython import embed; embed()

    #ax = bb.plot(table)
    #plt.title(exp["params.json"]['environment_params']['evaluation']['domain'])
    #plt.show()


def parse_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument('directories', nargs='+')
    parser.add_argument('--save', action='store_true')
    parser.add_argument('--interactive', action='store_true')
    return parser.parse_args()

if __name__ == "__main__":
    arguments = parse_arguments()
    main(arguments) 
