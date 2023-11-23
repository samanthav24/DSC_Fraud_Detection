# Deep Symbolic Classification for Fraud Detection
<hr style="border:2px solid gray">

Deep Symbolic Classification (DSC) for Fraud Detection is an adjusted framework of Deep Symbolic Regression developed by  <a href="https://github.com/brendenpetersen/deep-symbolic-optimization"> Petersen et. al. </a> This modified framework is specifically tailored to address classification tasks that involve high class imbalance, such as fraud detection.

The framework utilizes deep reinforcement learning techniques to produce explainable mathematical equations that can be utilized to classify fraudulent transactions in an interpretable manner.

## Prerequisites
An installation of gcc is required, e.g. on ubuntu:
```
sudo apt install build-essential
```

## Installation
<hr>

First clone the Deep Symbolic Optimization Repository within the the code directory:
```
cd code
git clone https://github.com/brendenpetersen/deep-symbolic-optimization.git
```

Follow the <a href="https://github.com/brendenpetersen/deep-symbolic-optimization"> corresponding install instructions</a>. You only have to install the Core package for the classification task.

Copy the adjusted files into the Deep Symbolic Optimization Repository:
```
cd code
cp regression.py ./deep-symbolic-optimization-master/dso/dso/task/regression/
cp config_classification_paysim.json ./deep-symbolic-optimization-master/dso/dso/config/
cd ..
```


<!-- ## Experiments
<hr>

For conducting the experiments please go to the experiments directory from the root folder:
```
cd ..
cd experiments
```
This directory contains the scripts to prepare the corresponding Fraud Detection dataset and to run the different experiments. Below we elaborate on the different components.

<br> -->

## Dataset Preprocessing
<hr>

First download the PaySim dataset from <a href="https://www.kaggle.com/datasets/ealaxi/paysim1"> this Kaggle competition</a>. Change the filename into ```paysim.csv```, and move it to the root directory.

Data preproccessing is done by running from the root directory:
```
python data_preparation.py
```
This will create ```train_df.csv```, ```val_df.csv```,  and ```test_df.csv``` in ```/deep-symbolic-optimization-master/dso/dso/task/regression/data```.

<br>

<!-- ### Experiments

In order to replicate all experiments, please run from the root directory:
```
bash all_exp.sh
```
This will run all experiments. Below we will cover all the individual experiments: -->

## Train the model
<hr>

Before you train the model, adjust the parameters in the configuration JSON file ```config_classification_paysim.json``` (and copy to corresponding directory again). The parameters that we tweak in DSC are:
<ul>
  <li>sigmoid_threshold: float between 0.0 and 1.0</li>
  <li>metric: "inv_crossentropy" or "f1_score"</li>
</ul>  

Descriptions of the other parameters can be found <a href="https://github.com/brendenpetersen/deep-symbolic-optimization"> here</a>. 

Training the model with the given parameters can be done by running from the ```./code/deep-symbolic-optimization-master/dso``` folder:
```
srun -u python -m dso.run dso/config/config_classification_paysim.json
```
This will save a timestamped log directory in ```./code/deep-symbolic-optimization-master/dso/log```. The directory consists of several files that contain summary statistics of the run. The generated Pareto-front equations with corresponding complexities are listed in ```dso_ExperimnetName_0_pf.csv```. The reward over the complexity of these equations is visualized in ```dso_ExperimnetName_plot_pf.png```. 

## Test the generated equations
<hr>

To check how one of the generated equations performs on the train, validation or test set, you can run from the root directory: 

```
python evaluate_expression.py --equation --threshold --dataset
```

You can enter the following values:
<ul>
  <li>equation: string of the equation you want to evaluate, e.g. "sqrt(x17 + x20)*(-x14 + x2 + x23)"</li>
  <li>threshold: float between 0 and 1</li>
  <li>dataset: dataset name, "train_df", "val_df", or "test_df"</li>
</ul>  

By running this code a txt file is created in ```./evaluation_output```, which contains the log loss, accuracy, precision, recall and f1 score of the given equation of the given dataset for given threshold.
