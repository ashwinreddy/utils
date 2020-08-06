import utils
import utils.experiments
from pathlib import Path
import matplotlib.pyplot as plt
import tempfile


def quicksave(dir = '/Users/adreddy/Plots'):
    plt.savefig(tempfile.NamedTemporaryFile(dir=dir, suffix='.png').name)

def main():
    p = Path('./')

    exps = []
    tasks = set()

    for f in filter(Path.is_dir, p.iterdir()):
        exp = utils.experiments.exp_results(f, 1)
        exps.append(exp)
        print(exp.task)
        tasks.add(exp.task)


    for task in tasks:
        print(task)
        pair = list( filter( lambda x: x.task == task, exps ) )
        if len(pair) > 1:
            # from IPython import embed; embed()
            utils.compare_exps_on_metric(pair, 'evaluation/return-average', label_fn = lambda x: "AWAC" if not x['params.json']['policy_params']['kwargs']['squash'] else "SAC")
            # plt.show()
            quicksave()
            plt.clf()
        # plt.show()


# from IPython import embed; embed()

if __name__ == "__main__":
    main()
