import seaborn as sns
import os
import pandas as pd
import matplotlib.pyplot as plt

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
    x_axis = "Timesteps"

    common_reward_keys = ['evaluation/return-average', 'ext_reward-mean']


    default_rescales = [["Timesteps", "timesteps_total", "M"], ["Reward", common_reward_keys, "K"]]

    def __init__(self, contents, rescales):
        self.contents = contents
        self.table.process(rescales)

    def __getitem__(self, key):
        return self.contents[key]
    
    @property
    def name(self):
        key = next(filter(lambda x: x.startswith('exp'), self.contents.keys()))

        return self[key]['checkpoints'][0]['local_dir']

    @property
    def env(self):
        return self['params.json']['environment_params']['training']['domain']

    @property
    def reward_keys(self):
        return [key for key in self.table.keys() if "ret" in key or "rew" in key]

    @property
    def table(self):
        return self['progress.csv']

    def plot(self, y, ax=None):
        self.ax = self.table.plot(x= self.x_axis, y= y, title = self.env, ax = ax, legend=True)
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
