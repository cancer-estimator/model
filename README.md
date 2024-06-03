# cancer-estimator-model

Our model search repository to find the best model to calculate risk
of having lung cancer.

# How to setup

## Dependencies

You should have installed:

- [git] for code versioning
- [dvc] for data versioning
- [pdm] for project managing


[git]: https://git-scm.com/book/en/v2/Getting-Started-Installing-Git
[dvc]: https://dvc.org/doc/install
[pdm]: https://pdm-project.org/en/latest/#installation

## Install env and run notebooks

After cloning the repository, at the root of the repository call the
following commands.


Install the libraries necessary to run the code:

``` shell
pdm install
```

Mount datasets folder with proper data for analysis and model search:

``` shell
pdm run dvc pull
```

Run the jupyter notebook server with all libraries, including our lib `cancer_estimator_model`:


``` shell
pdm notebook
```

## Data integration

To perform data integration you will need the R environment installed
in your machine, then you can call as:

``` shell
pdm data-integration
```

It will integrate all data and write in the path `datasets/lung-cancer/dataset_integrated.csv`.

At first call it may take sometime to install all libraries.
