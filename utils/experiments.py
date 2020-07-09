from pathlib import Path
import json
import utils

def exp_results(directory, priority=0):
    """
    Returns an experiment object from a directory with optional priority controls for which files to read
    """
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

    return utils.Experiment(experiment_results, rescales=utils.Experiment.default_rescales)
    

