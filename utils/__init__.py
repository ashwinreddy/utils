import os
import pandas as pd
import matplotlib.pyplot as plt
# from colorhash import ColorHash
# ColorHash(exp.algo).hex

from utils.plotting import quicksave

def algo_to_color(alg):
    return {
        "SAC" : "C0",
        "DistAwareSAC": "C1"
    }[alg]
    

def compare_exps_on_metric(pair, metrics, ylabel = None, title = None, label_fn = False , color_fn = None):
    if not label_fn:
        label_fn = lambda x : str(x.algo)
    
    if title is None:
        title = pair[0].task

    if color_fn is None:
        color_fn = lambda exp: algo_to_color(exp.algo)

    if type(metrics) is str:
        metrics = [metrics] * len(pair)

    for i, exp in enumerate(pair):
        if callable(label_fn):
            label = label_fn(exp)
        else:
            label = label_fn[i]

        plt.plot(exp.table[exp.x_axis], exp.table[metrics[i]], label = label, ) #c =  color_fn(exp))

    plt.xlabel(exp.x_axis)
    if ylabel:
        plt.ylabel(ylabel)
    # plt.ylabel(metric)
    plt.title(title)
    plt.legend()

class Table(pd.DataFrame):
    """
    An extension to the pandas DataFrame with some handy utilities
    """
    
    @staticmethod
    def from_csv(csv):
        try:
            df = pd.read_csv(csv)
        except:
            print("Couldn't read {}".format(csv))
            return
 
        df.__class__ = Table
        return df

    factors = {'M': 1e-6, 'K': 1e-3}

    def scale(self, new_key, key, factor):
        """
        Scale a column of the table by a factor while preserving the old and new columns
        """
        factor = self.factors.get(factor, factor) 
        self[new_key] = self[key] * factor
        return self
    
    def process(self, rescales):
        for rescale in rescales:
            new_key, key, factor = rescale

            if type(key) is list:
                key = next(filter(lambda key: key in self.keys(), key))

            self.scale(new_key, key, factor)

class Experiment(object):
    x_axis = "epoch"
    time_key = "timesteps_total"

    common_reward_keys = ['evaluation/return-average', 'ext_reward-mean']


    default_rescales = [["Timesteps", time_key, "M"], ["Reward", common_reward_keys, "K"]]

    table_file = 'progress.csv'

    def __init__(self, contents):
        self.contents = contents        

    def __getitem__(self, key):
        return self.contents[key]
    
    @property
    def name(self):
        key = next(filter(lambda x: x.startswith('exp'), self.contents.keys()))

        return self[key]['checkpoints'][0]['local_dir']

    @property
    def env(self):
        if 'variant.json' in self.contents:
            return self['variant.json']['env_class']['$class'].split('.')[-1]
        else:
            return self['params.json']['environment_params']['training']['domain']

    @property
    def task(self):
        return f"{self.env}-{self['params.json']['environment_params']['training']['task']}"

    @property
    def algo(self):
        if 'variant.json' in self.contents:
            return self['variant.json']['algorithm']
        else:
            return self['params.json']['algorithm_params']['type']

    @property
    def reward_keys(self):
        return [key for key in self.table.keys() if "ret" in key.lower() or "rew" in key.lower()]
    
    @property
    def metrics(self):
        return list(self.table.keys())

    @property
    def table(self):
        return self[self.table_file]

    def plot(self, y, ax=None, title = None):
        if title is None:
            title = "{} on {}".format(self.algo, self.env) 
        self.ax = self.table.plot(x= self.x_axis, y= y, title = title, ax = ax, legend=True)
        return self.ax
    
    def plot_together(self, ys):
        """
        Used for plotting different metrics of a run on the same scale in a single plot.
        """
        self.plot(ys[0])

        for y in ys[1:]:
            self.plot(y, ax=self.ax)
    
    def __repr__(self):
        return repr(self.contents.keys())
     

def table(csv="progress.csv", rescales = []):
    df = pd.read_csv(csv)
    df.__class__ = Table
    df.process()
    
    return df
 
def autoplot():
    # TODO automatically get progress file, make table, process, and plot
    pass
