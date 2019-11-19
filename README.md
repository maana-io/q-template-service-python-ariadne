# Maana Q TensorFlow Knowledge Microservice


## Build

It is recommended to use the [Conda](https://conda.io/projects/conda/en/latest/index.html) [environment](https://conda.io/projects/conda/en/latest/user-guide/concepts/environments.html) mechanism and ensure the right mix of `python`, `pip`, and packages are installed and active:

```
conda env create -f environment.yml
conda activate maana-tensorflow
```

To create an environment file:
```
conda env export > environment.yml
```