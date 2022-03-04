# Kinetic_Interactions
this repository creates a data warehouse to caculate allosteric regulation for each enzyme of each organism. This repository collects kinetic regulation from the in-house database and apply ML algorithms to estimate missing values. 


## Required modules:
__Please follow these steps to install all required packages on your device.__

* create a conda environment
> conda create -n my_new_env python
* check if the env is created
> conda env list
* activate env
> conda activate my_new_env
* add conda forge to channels:
> conda config --append channels conda-forge
* set channel priority
> conda config --set channel_priority strict
* pandas
> conda install pandas
* mysql connector
> pip install mysql-connector-python
* Install pycurl on your device
> pip install pycurl
* if the version of pycurl is not compatible with openssl, you will face this error:
> pycurl: libcurl link-time ssl backend (nss) is different from compile-time ssl backend (openssl)
* To debug, follow these steps:
> pip uninstall pycurl
 export PYCURL_SSL_LIBRARY=nss
 pip install --compile --install-option="--with-nss" --no-cache-dir pycurl


## References:
* [How to compute standard deviations from confidence intervals](https://handbook-5-1.cochrane.org/chapter_7/7_7_3_2_obtaining_standard_deviations_from_standard_errors_and.htm)
* [Propagation of error for multiple variables](https://www.itl.nist.gov/div898/handbook/mpc/section5/mpc553.htm)
* [assume 5% standard error for measurements without error]()
* [metabolomics dataser for E coli]()
* [Slides for data pipeline]()