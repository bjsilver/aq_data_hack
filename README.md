## Air Quality Data Hack

This page contains all the code needed to generate the figures in the Air Qualiy Data Hack lecture on the SOEE 3431 module at the University of Leeds

Feel free to clone the repository so you can experiment with the code and perform your own analysis.

## Notebooks
The code is split into three notebooks

### [Exploring OpenAQ data](https://github.com/bjsilver/aq_data_hack/blob/master/explore_openaq_data.ipynb)
How to use OpenAQ API with the [OpenAQ Python wrapper](https://github.com/openaq/openaq-python) to obtain the list of the air quality monitoring locations available on OpenAQ and use it to make a world map

### [Downloading OpenAQ data](https://github.com/bjsilver/aq_data_hack/blob/master/download_openaq_leeds.ipynb)
Demonstrating how to obtain a list of the air quality monitoring locations in and around Leeds, and use this to download all the available air quality data from OpenAQ

### [Visualising OpenAQ data](https://github.com/bjsilver/aq_data_hack/blob/master/visualise_openaq_data.ipynb)
Using Python to analyse the Leeds air quality data, including
* Plotting maps of staiton locations
* Creating time series plots with different averaging times
* Creating plots of the diurnal and seasonal average pollutant concentrations
* Visualising long-term trends
* Plotting correlations with meteorological data
