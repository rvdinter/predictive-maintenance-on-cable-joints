# Predictive maintenance on cable joints
Within Alliander, challenges in operations are rising due to the energy transition. In order to facilitate Dutch electricity users, we have to not only work harder, but also smarter. Knowing when a cable will fail will help with plannability and research for electricity grid improvements. Sioux Technologies is supporting Alliander in this research.

## Setting up the environment
Use Conda to create a new environment:
```commandline
conda create -n alliander python=3.8 setuptools=63.4
conda activate alliander
```

And install the repository in editable mode:
```commandline
# go to root folder
pip install --editable .
# or
pip install -e .
```
As such, we can use the most recent (edited) version of the `alliander_predictive_maintenance` module.


## Arcitecture
The architecture is based on the 5C principle. This is also how the folders are structured.

![5C architecture](\doc\img\5C-architecture-for-Cyber-Physical-Systems-16.png)

## Coding style conventions
To make sure we obey the code style rules consistently, make it a habit to run `flake8` before pushing.
To run `flake8`:
```commandline
# go to root folder
flake8 .
```

## License

See the [LICENSE](LICENSE) file for license rights and limitations (MIT).
