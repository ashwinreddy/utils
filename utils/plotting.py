import utils
import utils.experiments
from pathlib import Path
import matplotlib.pyplot as plt
import tempfile


def quicksave(dir = '/home/ashwin/Plots'):
    plt.savefig(tempfile.NamedTemporaryFile(dir=dir, suffix='.png').name)

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
    # from IPython import embed; embed()
    utils.compare_exps_on_metric(pair)
    quicksave()
    # plt.show()


# from IPython import embed; embed()
