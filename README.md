# Kinetic_Interactions
this repository analyzes collected kinetic regulation in the in-house database and apply ML algorithms to estimate missing values. 


Requirements:
create a new conda env
conda create -n my_new_env python
conda activate my_new_env

add conda forge to channels:
conda config --append channels conda-forge
conda config --set channel_priority strict

required packages:
conda install pandas
pip install mysql-connector-python