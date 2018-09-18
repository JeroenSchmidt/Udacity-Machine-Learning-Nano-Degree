# Machine Learning Engineer Nanodegree
## Specializations
## Project: Capstone Proposal and Capstone Project


This capstone project sought to see if it was possible to use Reddit and Twitter sentiment analysis related to Etherium and Bitcoin to predict price movement. This project consisted of three major parts;

1) Acquiring the data through a combination of large-scale web scraping and downloading public data repositories
2) Shaping and moulding the data to fit my objectives
3) Performing analysis on the data
4) Building and evaluating models based on the data I obtained 


## Reproducing the work contained within

#### Libraries Required
It is strongly encoraged to install the following libraries through conda:

* `pyspark 2.3.1`
* `keras`
* `seaborn`
* `matplotlib`
* `numpy`
* `scikit-learn`
* `arrow`

**NOTE: For pyspark to work correctly you need to have java8 set as your default java environment**

#### Before you get started - DATA
You will have to download preprocessed data required to reproduce the analysis and modelling results from the following [mega link](https://mega.nz/#F!6P4F2SyS!uoysyVGVysVy0UU-DJFx7Q), all the contents should be inserted into the data directory.

The tree structure should look as follows:

```
data
|-features
    |-sentiment_features
|-reddit-crypto
    |-parquet
        |-complete_sentiment
            |-part-*.snappy.parquet
|-ticker_data
    |-USDT_BTC.csv
    |-USDT_ETH.csv
|-tweets
    |-ethereum
        |-parquet
            |-sentiment
    |-bitcoin
        |-parquet
            |-sentiment
```

#### Explination of Notebooks

##### Primary Notebooks
The following notebooks are directly related to the report that was written. The models, insights and graphs produced within these notebooks were used directly in the report. These notebooks can be run to reproduce the results discussed, assuming the processed data from the [mega link](https://mega.nz/#F!6P4F2SyS!uoysyVGVysVy0UU-DJFx7Q) is present in the data folder.

1) The `analysis` folder contains notebooks that were used to understand better the data that was acquired. In it, you will find 3 notebooks, each dealing with a separate topic. Ticker price movement, sentiment scores, and ingested data volumes.  
2) The `Main Project (ML + Feature Creation).ipynb` notebook is where the models were built and assessed. 


##### Auxilary Notebooks
These notebooks are not necessary to reproduce the work but are included for those who are curious. Apologies in advance for the mess contained within. 


1) The `get-data` folder contains notebooks and snippets of code that were used to acquire, scrub and wrangle the data used in this project. A lot of work in this folder was done on an ad-hoc basis and will not be easily re-runnable. I made a conscious decision not to make this section reproducible as it would require many days worth of work to make it "production"/reproducible code, this is especially true when I would have to make it all automatic with the AWS cloud infrastructure I used.
2) The `experimentation` folder contains notebooks that were used to help familiarise myself with the libraries and ideas I was exploring, this can be thought of as my scratch space. 
