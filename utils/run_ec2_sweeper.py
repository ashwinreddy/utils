import doodad as dd
from doodad.easy_sweep.hyper_sweep import Sweeper
from pathlib import Path
from argparse import ArgumentParser
import toml
from rich import print


def load_config(config_file: str) -> dict:
    """
    Reads a TOML file with all the variable configurations into a dictionary
    """
    return toml.loads(open(config_file).read())


def local_mount(mount_point):
    """
    Automatically mounts the current directory under the folder specified by the config
    """
    return dd.mount.MountLocal(local_dir=str(Path.cwd()), mount_point=mount_point)


def parse_config(config: dict, debug: bool):
    """
    Creates the kwargs that can be fed into a doodad shell command
    """
    mounts = [
        local_mount(mount_point=config['local_directory_mount'])
    ]

    for key, mount_params in config['mounts'].items():
        if key == "output":
            mount_params['output'] = True

        if key == "output" and not debug:
            mount_type = dd.mount.MountS3
            mount_params = {
                's3_path': config['s3']['path'],
                's3_bucket': config['s3']['bucket'],
                'mount_point': mount_params['mount_point'],
                'output': True
            }
        else:
            mount_type = dd.mount.MountLocal

        mounts.append(mount_type(**mount_params))

    hold = False
    if debug:
        mode = dd.mode.LocalDocker(image=config['docker_image'])
    else:
        hold = True
        mode = dd.mode.EC2AutoconfigDocker(
            image=config['docker_image'],
            region=config['ec2']['region'],
            instance_type=config['ec2']['instance_type'],
            spot_price=config['ec2']['spot_price'],
        )

    kwargs = {
        'command': config['command'],
        'mode': mode,
        'mount_points': mounts,
        'runner': config['runner']
        # 'verbose': True
    }
    print(kwargs)
    return kwargs, hold

def run_sweep_doodad_command(run_command, runner, params, run_mode, mounts, repeat=1, test_one=False):
    sweeper = Sweeper(params, repeat)
    for config in sweeper:
        run_command_curr = runner #"softlearning run_example_local examples.classifier_rl"
        for k, v in config.items():
            run_command_curr += " --" + str(k) + "=" + str(v)
        run_command_curr = " \"" + run_command_curr + "\""
        run_command_full = run_command + run_command_curr
        dd.launch_shell(
                command=run_command_full,
                mode=run_mode,
                mount_points=mounts)
        if test_one:
            break


def main(args):
    config = load_config(args.config)
    kwargs, hold = parse_config(config, args.debug)

    should_launch = "y"
    if hold:
        should_launch = input("Launch trial? (yes/no) ")
    # test
    sweep_params = config['hyperparams']
    if should_launch.lower().startswith("y"):
        run_sweep_doodad_command(run_command=kwargs['command'],
                                    runner = kwargs['runner'],
                                    params=sweep_params,
                                    run_mode=kwargs['mode'],
                                    mounts=kwargs['mount_points'])


if __name__ == "__main__":
    parser = ArgumentParser(description='Run arbitrary scripts in the cloud')
    parser.add_argument('config', help='location of run configuration TOML file')
    parser.add_argument('--args', help='arguments passed to command')
    parser.add_argument('--debug', action='store_true', help='run locally')
    args = parser.parse_args()
    main(args)
