"""
Justin Clark
CS 387
Date: 08/01/2020
code_arima.py

This script will use the ARIMA model to forecast confirmed 
cases in the United States

Script Outline:
    1. Imports
    2. Functions
    3. Data/Time Series Transformations
    4. ADF/KPSS Test
    5. Optimized Model
    6. Residual Summary
    7. Forecast
"""
#########################################################
### IMPORTS###
import os
import matplotlib.pyplot as plt
from pmdarima.arima import auto_arima,ndiffs
from sklearn.model_selection import TimeSeriesSplit
import numpy as np
import pandas as pd
from statsmodels.tsa.stattools import kpss
from statsmodels.graphics.tsaplots import plot_acf,plot_pacf
from statsmodels.tsa.stattools import acf,pacf
from pandas.plotting import lag_plot
from sklearn import linear_model 
from statsmodels.tsa.arima_model import ARIMA
from statsmodels.tsa.stattools import adfuller
from sktime.forecasting.arima import AutoARIMA
from sktime.forecasting.model_selection import SlidingWindowSplitter
from sktime.forecasting.model_selection import ForecastingGridSearchCV
from sktime.forecasting.theta import ThetaForecaster
from sktime.forecasting.naive import NaiveForecaster
###################################################


#################################################
### 2. FUNCTIONS #######
def Make_Country_Dictionary(label,c,r,d):
    """    
    Function to make dictionary of confirmed, recovered,dead cases
    for any country or region within the datasets
    Inputs:
        label: Country Label (i.e. 'Japan')
        c,r,d: confirmed,recoverd,death dateframes
    Return:
        dictonary of lists ofconfirmed,recovered,dead time series
    """
    row_index = c[c['Country/Region'] == label].index.item() 
    dictionary = {'label': label,
                  'c': c.iloc[row_index].tolist()[45:],
                  'r': r.iloc[row_index].tolist()[45:],
                  'd': d.iloc[row_index].tolist()[45:]}
    return dictionary

def adf_test(series,alpha):
    """
    Function to calulate and display results of ADF test on 
    time series data
    Input:
        series: time series to be analyzed
        alpha: critical value for test statistic
    """
    print('DF Stationarirty Test Results')
    dftest = adfuller(series, autolag='AIC')
    dfoutput = pd.Series(dftest[0:4], index=['Test Statistic','p-value','#Lags Used','#  Observations Used'])
    for key,value in dftest[4].items():
        dfoutput['Critical Value (%s)'%key] = value
    print (dfoutput)
    if dfoutput['p-value'] < critical_value:
        print('Reject the null hypothesis --> time series is stationary')

def kpss_test(series, **kw):    
    """
    Function to calculate and display results of KPSS test
    on time series data
    Input:
        series: time series data
    
    """
    statistic, p_value, n_lags, critical_values = kpss(series, **kw)
    print('KPSS Statistic: {}'.format(statistic))
    print('p-value: {}'.format(p_value))
    print('# Lags: {}'.format(n_lags))
    print('Critial Values:')
    for key, value in critical_values.items():
        print('   {} : {}'.format(key,value))
    if p_value < 0.05:
        print('Reject the null hypothesis --> time series is not stationary')


def RMSE(predicted,observed):
    """
    Calculate the Root Mean Square Error from 
    predicted and observed values
    Input:
        predicted: list of forecasted values drawn from fitted model
        observed: list of observed values drawn from physical data
    Return:
        RMSE: Value of performance metric for RMSE
    """
    RMSE = np.sqrt(((predicted-observed)**2).mean())
    return RMSE

def MAPE(predicted,observed):
    """
    Calculate the mean absolute percentage error from
    predicted and obserbed values
    Input:
        predicted: list of forecasted values drawn from fitted model
        observed: list of observed values drawn from physical data
    Return:
        RMSE: Value of performance metric for RMSE
    """
    MAPE = (np.abs((observed-predicted)/observed).mean())*100
    return MAPE

#################################################
#Read data in from csvs
confirmed_df = pd.read_csv(os.getcwd()+'/data/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv(os.getcwd()+'/data/time_series_covid19_recovered_global.csv')
deaths_df = pd.read_csv(os.getcwd()+'/data/time_series_covid19_deaths_global.csv')

#Iniitalize US dictionary
US = Make_Country_Dictionary('US',confirmed_df,recovered_df,deaths_df)

##############################
#First oder difference
USconf_daily = np.diff(US['c'])
USrecov_daily = np.diff(US['r'])
USdeaths_daily = np.diff(US['d'])
##############################

#Transformation/Differencing Strategies
USlog = np.log(US['c'])
US_log_diff = np.diff(USlog)
US_log_2diff = np.diff(USlog,2)


#List of Dates
dates = confirmed_df.columns.tolist()[45:]
#list of day ranges
datas = list(range(1,len(US['c'])+1))


#Plot of confirmed Cases in United States
plt.plot(datas,US['c'],label = 'Confirmed')
plt.title("United States Confirmed Cases",fontsize = 16)
plt.xlabel("Time (Days)",fontsize = 16)
plt.ylabel("Confirmed Cases(Yt)",fontsize = 16)
plt.savefig(os.getcwd() + '/FinalProjectPlots/US_C.png', dpi=300,bbox_inches='tight')
plt.show()


### Create dataframe of Days and Transformed Data
datas = list(range(1,len(US_log_2diff)+1))
# Create dictionary of dates and US cases 
d = {'Date': datas, 'Log_2_Diff': US_log_2diff}
US_dataframe = pd.DataFrame(d)
US_series = US_dataframe['Log_2_Diff']



#### Plots of transformation strategies
plt.plot(USlog)
plt.xlabel("Time (Days)",fontsize = 16)
plt.ylabel("Log(Yt)",fontsize = 16)
plt.title("Log Transformation",fontsize = 16)
plt.savefig(os.getcwd() + '/FinalProjectPlots/log.png', dpi=300)
plt.show()

plt.plot(US_log_diff)
plt.xlabel("Time (Days)",fontsize = 16)
plt.ylabel("Log((1-B)Yt)",fontsize = 16)
plt.title("Log with First Difference",fontsize = 16)
plt.savefig(os.getcwd() + '/FinalProjectPlots/logdifferenced.png', dpi=300)
plt.show()

plt.plot(US_log_2diff)
plt.xlabel("Time (Days)",fontsize = 16)
plt.ylabel("Log((1-B)^2 Yt)",fontsize = 16)
plt.title("Log with Second Difference",fontsize = 16)
plt.savefig(os.getcwd() + '/FinalProjectPlots/log2differenced.png', dpi=300)
plt.show()


######################################
# TESTS FOR STATIONARY BEHAVIOR
critical_value = 0.05
adf_test(US_series,critical_value)
kpss_test(US_series,regression='ct')
####################################
   

    
##############################################
#ACF AND PACF PLOTS
plot_acf(US_series,lags = 20)
plt.xlabel("Lags",fontsize = 16)
plt.ylabel("Correlation",fontsize = 16)
plt.savefig(os.getcwd() + '/FinalProjectPlots/ARIMA_ACF.png', dpi=300)
plt.show()

plot_pacf(US_series,lags = 20)
plt.xlabel("Lags",fontsize = 16)
plt.ylabel("Correlation",fontsize = 16)
plt.savefig(os.getcwd() + '/FinalProjectPlots/ARIMA_PACF.png', dpi=300)
plt.show()
#######################################################


#Create dataframe of log(confirmed cases)
datas = list(range(1,len(US['c'])+1))
# Create dictionary of dates and US cases 
d = {'Date': datas, 'Incidence': np.log(US['c'])}
US_dataframe = pd.DataFrame(d)
US_series = US_dataframe['Incidence']


### TRAIN TEST SPLIT ###
X = US_series
train_size = 0.9
train_instances = int(len(X) * train_size)
train,test = X[0:train_instances],X[train_instances:len(X)]
########################################

#######################################
### ARIMA STATS MODEL with Optimal Parameters###
model = ARIMA(train,order = (5,2,2))
fitted_model = model.fit(disp=0)
print(fitted_model.summary())
forecast,std_error,conf = fitted_model.forecast(len(test),alpha = .05)
#######################################



#####################################
### FITTED MODEL RESIDUAL SUMMARY ###
resids = pd.DataFrame(fitted_model.resid)
resids.plot(title = 'Fitted Model Residuals',fontsize = 16)
plt.hlines(np.mean(resids),0,len(train),label = 'Mean',color = 'red')
plt.legend(fontsize = 'large')
plt.savefig(os.getcwd() + '/FinalProjectPlots/ARIMA_resids.png', dpi=300)
plt.show()
resids.plot(kind = 'kde',title = 'Kernel Density Estimation',fontsize = 16)
plt.savefig(os.getcwd() + '/FinalProjectPlots/ARIMA_residskde.png', dpi=300)
plt.show()
#####################################

########################
#Residual Numericial Sumamry
print("Residual Numerical Summary")
print(resids.describe())
################################


#Make forecast into panda series
forecast_series = pd.Series(forecast,index = test.index)

#Intialize confidence interval series
lower_CL = pd.Series(conf[:,0])
upper_CL = pd.Series(conf[:,1])


### Performance Metrics
RMSE = RMSE(list(forecast_series),test)
print("RMSE = {}".format(RMSE))
MAPE = MAPE(list(forecast_series),test)
print("MAPE = {}".format(MAPE))

### FORECAST PLOT
plt.plot(test,label = 'Observed')
plt.plot(forecast_series,label = 'Forecast')
plt.fill_between(test.index,lower_CL,upper_CL,color = 'grey',alpha = 0.25)
plt.xlabel("Time (Days)",fontsize = 16)
plt.ylabel("Log(Confirmed Cases)",fontsize = 16)
plt.legend(loc = 'upper left',fontsize = 'large')
plt.title('Forecast using Optimized ARIMA Model',fontsize = 16)
plt.grid()
plt.savefig(os.getcwd() + '/FinalProjectPlots/ARIMA_ForecastPlot.png', dpi=300)
plt.show()

### Big Picture Figure  ###
plt.plot(train,label = 'Training')
plt.plot(test,label = 'Observed')
plt.plot(forecast_series,label = 'Forecast')
plt.fill_between(test.index,lower_CL,upper_CL,color = 'grey',alpha = 0.25)
plt.vlines(len(train),0,16,label = 'Train/Test Split',color = 'black')
plt.title("ARIMA(5,2,2)  Results",fontsize = 16)
plt.xlabel("Time (Days)",fontsize = 16)
plt.ylabel("Log(Confirmed Cases)",fontsize = 16)
plt.ylim(4,16)
plt.legend(loc = 'upper left',fontsize = 'large')
plt.grid()
plt.savefig(os.getcwd() + '/FinalProjectPlots/ARIMA_522_ForecastPlot.png', dpi=300)
plt.show()



