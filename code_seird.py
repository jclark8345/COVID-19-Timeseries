"""
Justin Clark
CS 387
Date: 08/01/2020
code_seird.py

This scrpit will work with the stochastic dynamical models
related to infectious disease

Script Outline:
    1. Imports
    2. Functions
    3. Declaration of Model Parameters
    4. Social Distancing Simulation
    5. Estimation of R0
"""

#######################################
### 1. IMPORTS ###
import os
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as spi
import pandas as pd
import lmfit
######################################


#####################################
### 2. FUNCTIONS ###
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

def diff_eqs(initial_cond,t,beta,k,gamma,delta):
    '''
    The main set of differential equations for SEIRD model
    Inputs:
        initial_cond: List of population values for SEIRD comparments
        t: Array of values representing time (days)
        beta,k,gamma,delta: SEIRD model parameters
    Return:
        Y: Changes in compartment values for timestep
    '''
    S,E,I,R,D,C = initial_cond
    N = S+E+I+R+D
    dS = - beta * S * (I/N)
    dE = beta * S * (I/N) - (k*E)
    dI = (k*E) - ((gamma+delta)*I)
    dR = gamma*I
    dD = delta*I
    dC = k*E
    Y = [dS,dE,dI,dR,dD,dC]
    return Y 

def diff_eqs_quar(initial_cond,t,beta,k,gamma,delta,lamda):
    '''
    The main set of differential equations for SEIRD model
    with the inclusion of social distancing parameter lambda
    Input:  
        initial_cond: List of population values for SEIRD comparments
        t: Array of values representing time (days)
        beta,k,gamma,delta: SEIRD model parameters
    Return:
        Y: Changes in compartment values for timestep
    '''
    S,E,I,R,D = initial_cond
    N = S+E+I+R+D
    dS = -lamda* beta * S * (I/N)
    dE = lamda*beta * S * (I/N) - (k*E)
    dI = (k*E) - ((gamma+delta)*I)
    dR = gamma*I
    dD = delta*I
    Y = [dS,dE,dI,dR,dD]
    return Y   # For odeint
    
def resids(model_parameters,initial_conditions,t,data):
    """
    Calculate residual errors from model fit and physical data
    to attempt optimization of model parameters through the minimization
    of residuals
    Inputs:
        model_parameters: lmfit.Parameters() =  parameters to be optimized
        initial_conditions population values for SEIRD compartments
        t: time range
        data: data to compare model fit with
    Output:
        residuals of model to be minimized
    """
    beta = model_parameters['beta'].value
    k = model_parameters['k'].value
    gamma = model_parameters['gamma'].value
    delta = model_parameters['delta'].value
    solution = spi.odeint(diff_eqs,initial_cond,t_range,args =(beta,k,gamma,delta))#,E,I))
    return (solution[:,-1]-data['Confirmed']).ravel()


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
########################################
    

#################################################
### DATA AQUISITION FOR LATER MODEL FITS 

# Read in initial data for Global Confirmed/Recovered/Deaths
confirmed_df = pd.read_csv(os.getcwd()+'/data/time_series_covid19_confirmed_global.csv')
recovered_df = pd.read_csv(os.getcwd()+'/data/time_series_covid19_recovered_global.csv')
deaths_df = pd.read_csv(os.getcwd()+'/data/time_series_covid19_deaths_global.csv')
# Initialize United States Data
US = Make_Country_Dictionary('US',confirmed_df,recovered_df,deaths_df)
#Create Dataframe
crd_df = pd.DataFrame(list(zip(US['c'],US['r'],US['d'])),columns = ['Confirmed','Recovered','Dead'])
### SHORTEN ANALYSIS FOR Expoential Growth Phase
crd_df = crd_df.iloc[:50,:]
##################################################

#############################################
#CFP = Mean Case Fatality Proportion
CFP = [i/j for i,j in zip(US['d'],US['c'])]
plt.plot(CFP)
#############################################

##########################################
### 3. Declaration of Initial Population Values Based on Data ###
#N: Population Size
N=10000
#I: Initial Infected Individuals
I= 0
#E: Initial Exposed Individuals
E= 1
#R: Initial Recovered Individuals
R =  0
#S: Initial Dead Individuals
D=  0
C = E
S = N-E-I-R-D
initial_cond = [S,E,I,R,D,C]
#########################################

#############################################
### Declaration of SEIRD Model Parameters
#Beta: Transmission/Infection Rate/Contact Rate
beta = 1.75
#k: Rate E --> I (1/k = mean latent period) / Incubation Period
k = .2
#Gamma:Recovery Rate
gamma=.2
#Delta: Death rate
delta = .02
model_params = (beta,k,gamma,delta)
###########################################

##########################################
### BASELINE SEIRD MODEL ANALYSIS WITH PARAMETERS
ND = 100
TS = 1
t_start = 0.0
t_end = ND 
t_inc = TS
t_range = np.arange(t_start, t_end+t_inc, t_inc)
sim_results = spi.odeint(diff_eqs,initial_cond,t_range,args = model_params)

################################################
plt.plot(sim_results[:,1],label = 'Exposed',color = 'blue')
plt.plot(sim_results[:,2],label = 'Infected',color = 'red')
plt.legend()
plt.grid()
plt.title('SEIRD Model Simulation(beta={},k={},gamma={},delta = {})'.format(beta,k,gamma,delta),fontsize = 12)
plt.xlabel('Time (Days)',fontsize = 16)
plt.ylabel('Population Incidence',fontsize = 16)
plt.savefig(os.getcwd() + '/FinalProjectPlots/initSEIRD.png', dpi=300)
plt.show()
#############################################

#######################################
#4: Lamda: Effect of Quarantine Measures
initial_cond = [S,E,I,R,D]
lamda_list = [1.0,0.66,0.33]
for l in lamda_list:
    lamda = l
    model_params = (beta,k,gamma,delta,lamda)
    sim_results = spi.odeint(diff_eqs_quar,initial_cond,t_range,args = model_params)
    plt.plot(sim_results[:,1],label = 'Exposed(lamda = {})'.format(lamda))
    plt.plot(sim_results[:,2],label = 'Infected(lamda = {})'.format(lamda))
plt.legend()
plt.grid()
plt.title('SEIRD Model with Parameter Lamda',fontsize = 16)#(beta={},k={},gamma={},delta = {})'.format(beta,k,gamma,delta),fontsize = 12)
plt.xlabel('Time (Days)',fontsize = 16)
plt.ylabel('Case Numbers',fontsize = 16)
plt.savefig(os.getcwd() + '/FinalProjectPlots/quarSEIRD.png', dpi=300)
plt.show()

##########################################


#################################################
#### 5: LMFIT MINZIMIATION Simulation

##########################################
### Declaration of Initial Population Values Based on Data ###
#S: Initial Susceptible Individuals
N=300000000
#I: Initial Infected Individuals
I= US['c'][0]
#E: Initial Exposed Individuals
E= US['c'][0]
#R: Initial Recovered Individuals
R =  US['r'][0]
#S: Initial Dead Individuals
D=  US['d'][0]
C=E
S = N-E-I-R-D
initial_cond = [S,E,I,R,D,C]
#########################################

##########################################
#ND: Numer of Days of Simulation
ND = crd_df.shape[0]-1
#TS: Size of Time Step (Day Intervals)
TS = 1
########################################

#########################################
# Definition of Model Parameters to be Minimized
model_parameters = lmfit.Parameters() 
model_parameters.add('beta',value = beta,min=0,max =3)
model_parameters.add('k',value = k,vary = False)
model_parameters.add('gamma',value = gamma,min=0,max =1)
model_parameters.add('delta',value = delta,min=0,max =1)
#########################################

### TIME RANGE DECLARATION
t_start = 0.0
t_end = ND 
t_inc = TS
t_range = np.arange(t_start, t_end+t_inc, t_inc)

#Minimization of model residuals through parameter optimization
result = lmfit.minimize(resids,model_parameters,args=(initial_cond,t_range,crd_df))

#Make list of optimized params
optimized_params = (result.params['beta'].value,result.params['k'].value,result.params['gamma'].value,result.params['delta'].value)
print(optimized_params)
#Simulate SEIRD model using params
RES = spi.odeint(diff_eqs,initial_cond,t_range,args =optimized_params)


### CALCUALTE BASIC REPRODUCTIVE NUMBER
R0 = result.params['beta'].value/(result.params['gamma'].value+result.params['delta'].value)
print("Basic Reproduction Number (R0): {}".format(R0))


### Performance Metrics
RMSE = RMSE(RES[:,-1],US['c'][0:50])
print("RMSE = {}".format(RMSE))
MAPE = MAPE(RES[:,-1],US['c'][0:50])
print("MAPE = {}".format(MAPE))

###################################################
### SEIRD PLOT WITH OPTIMIZED PARAMETERS ###
plt.plot(US['c'][0:50],label = 'US Confirmed')
plt.plot(US['r'][0:50],label = 'US Recovered')
plt.plot(US['d'][0:50],label = 'US Dead')
plt.plot(RES[:,-1],label = 'Simulated Confirmed')
plt.plot(RES[:,2],label = 'Infected',color = 'blue')
plt.plot(RES[:,3],label = 'Recovered',color = 'red')
plt.plot(RES[:,4],label = 'Death',color = 'black')
plt.legend()
plt.grid()
plt.title('SEIRD Model Simulation',fontsize = 16)
plt.xlabel('Time (Days)',fontsize = 16)
plt.ylabel('Case Numbers',fontsize = 16)
plt.savefig(os.getcwd() + '/FinalProjectPlots/SEIRD.png', dpi=300,bbox_inches='tight')
plt.show()
####################################################