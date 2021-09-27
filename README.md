# COVID-19-Timeseries
Analysis of COVID-19 Data. For a full writeup of anaylsis, please see [article.pdf](https://github.com/jclark8345/COVID-19-Timeseries/blob/main/article.pdf)

## Contents

- [Project Introduction](#project-introduction)
- [File Directory](#file-directory)
- [Data](#data)
- [Results](#results)
- [References](#references)

## Project Introduction

The study of infectious diseases has been of great interest within the field of epidemiology for many years due to unique characteristics of emergence and reemergence innately related to these viruses. Infectious diseases demonstrate numerous characteristics distinct from other human disease including a potential for unpredictable and explosive global impact, human to human transmission, prevention potential, and dependence on the nature and complexity of human behavior. The transmission rate and potential impact of infectious disease have been directly related to human behavior and lifestyle due to modes of transmission such as social gatherings, public transportation, occupation, and the current healthcare environment.

Mathematical models in combination with the field of epidemiology have been identified as useful experimental tools for hypothesis evaluation, answering disease specific questions, and estimating key dynamic quantities from the data related to infectious disease. This type of modeling effort can identify important data, highlight hidden trends, forecast incidence and quantify uncertainty within model forecasts. Inherently, the reliability of public health surveillance and model forecasts depends upon the ability of models to make the extrapolations necessary to predict the most likely course of a public health emergency given the incoming, recorded information.

In this piece, we propose multiple methods as techniques for predicting incidence of 2019-nCoV in the United States and the transmission potential of the virus. The discussed mathematical and statistical methods are those able to estimate or predict key epidemiological parameters from available, physical data. 

First, we propose and define a compartmental SEIRD model out of the classical deterministic epidemiological toolkit as a baseline analysis of the exponential growth phase of the current epidemic. Moreover, we look to employ this type of compartmental model to analyze short term incidence and estimate the basic reproductive number $R_0$. This epidemiological parameter is of interest due to its ability to quantify infectious disease transmission over a population. Simply put, the value of this parameter will describe epidemic severity based on novel transmission. 

Second, we look to forecast the cumulative number of confirmed cases within the United States. This type of data is reported daily by numerous organizations around the globe with the caveat that the number of confirmed or recovered cases on a specific day have strong correlations with the values of previous days. Therefore, we look to implement a statistical based method to aid in forecasting confirmed disease incidence within the United States based on the use of these previous values. The different types of auto regressive time series models have proven to be strong, flexible tools for analyzing overall patterns within time series data and have been used to estimate and forecast many practical problems. Specifically, the ARIMA model is often used for the prediction of infectious disease.

## File Directory

### **Individual Files**

    - article.pdf: comprehensive report of entire analysis including data,methodology,results,all figures,discussion, etc
    
    - code_arima.py: time series modeleling script
    
    - code_seird.py: compartmental SEIRD Model script

### **Folders/Contents**

**Data**

    -time_series_covid19_confirmed_global.csv: Global confirmed COVID-19 cases partitioned by time/location
    
    -time_series_covid19_deaths_global.csv: Global deaths due to COVID-19 partioned by time/location
    
    -time_series_covid19_recovered_global.csv: Global cases recovered from COVID-19 partitioned by time/location
    
## Data

The 2019-nCoV data used for analysis was drawn from the Johns Hopkins CSSE Github Repository. This data source contains daily updated files relaying location specific information of the confirmed, recovered, and death incidence of 2019-nCoV cases. This data set categorizes information by relevant characteristics such as country, city and coordinate location and contains novel coronavirus information for 249 locations,for both individual cities and entire countries. The time series data contains case numbers for a majority of the outbreak beginning in January 2020 (01/22/2020). The discussed data is available for each day with the cutoff for analysis within this report being June 2020(06/26/2020). This data will be used to summarize location relationships related to 2019-nCoV and to evaluate conclusions drawn from appropriate model derivation.

The time series data was divided into a training and testing subset where the size of the test subset was equal to ten percent of the total number of days within the initial data set. Therefore, the size of the training set was determined to be 100 days and the size of the testing set was 12 days. The identification of the optimal ARIMA model order, which is based upon discussed parameters, was assessed using  Akaike Information Criterion (AIC) and Bayesian Information Criterion (BIC). These two objective metrics of model suitability seek to leverage the trade off between the fit of the model and its complexity. These two criterion differ based on penalization that occurs due to increasing the complexity of the model.

It is important to note the fact these these information criterion for optimizing model performance are not strong indications of the appropriate order of time series difference, parameter d, within the ARIMA model. This is due to the definition of differencing such that the value of parameter d changes the data which is used for computation of the maximum value of likelihood of the model, intrinsic to the definition of both discussed criterion.
Due to the inherent importance of time series forecasting and its application to real-world scenarios, numerous performance metrics are necessary to estimate forecast accuracy and aid in the comparison of different, unique models. The selected metrics were chosen based off their ability to measure both bias and accuracy of forecast performance. These performance metrics are measured as a function of the expected and observed values within the time series.

## Results

Initial diagnostics of the time series data demonstrated a clear lack of stationary behavior due to a constantly increasing trend (Figure (3a)). This behavior was expected due to the intrinsic growth rate related to infectious disease. Numerous transformations and differencing strategies were applied to the initial data to obtain and verify stationary behavior within the data. These strategies included taking the logarithm of the initial time series, and both the first and second-order differences of the transformed, logarithmic data. The initial logarithmic transformation (Figure 3b) and logarithmic transformation with first-order differencing (Figure 3c) both failed to obtain stationary behavior of the time series data. The logarithmic transformation combined with second-order differencing (Figure 3d) appears to show stationary behavior.
Statistical hypothesis tests of stationarity within the data were applied to determine whether the transformation of the time series was successful in obtaining stationary behavior. Two unit root tests, the Augmented Dickey-Fuller(ADF) and Kwiatkowski-Phillips-Schmidt-Shin(KPSS) test, were implemented with opposite null and alternative hypothesis. 


The contents of Table (2) summarize the test results of both the ADF and KPSS tests for stationarity on the twice differenced logarithmic series (Figure 1(d)). With a significance level $\alpha = 0.05$ and associated p-value $< \alpha$ for the ADF test we reject the null hypothesis and assume of the modified time series data to be stationary.Similarly, p-value $> \alpha$ for the KPSS test, we fail to reject the null hypothesis and assume to transformed time series data to be stationary. Therefore, given the results displayed in Table (2), we are able to begin the implementation of decomposition methods such as the ARIMA model.
The inherent noise within the 2019-nCoV confirmed data outlines the possibility for several strong ARIMA models with varying values of parameters (p,q) to be computed. Therefore, the selection of the optimum model occurred through the evaluation of varying models based upon previously discussed performance metrics, the Akaike Information Criterion (AIC) and Bayesian Information Criterion (BIC).



The optimal model was found to be an ARIMA model with parameter $p = 5$ and parameter $q = 2$. The best choice for parameter d was found to be 2 based upon the discussed stationarity diagnostics above. This ARIMA(5,2,2) model was fit to the training subset of the original data containing 100 observations with associated informative diagnostics AIC = -328.594 and BIC = -305.147. This model was further selected due to the model coefficients being significantly different from zero based on t-test with $\alpha = 0.05$.
Once we have identified the optimal model, we look to analyze the residuals of the fitted model to check whether our model has captured or included all available information from the data. More specifically, we look to ensure that the model residuals remain uncorrelated with a mean of zero. Additionally, we look to further verify that the fitted model residuals have a constant variance and are normally distributed with mean equal to zero. These additional two properties will make the calculation of prediction intervals easier. The results of Figure (5) verify the required assumptions of residual diagnostics demonstrating a lack of correlation between residuals such that the model residuals are normally distributed with mean of zero. 

## References

    Adam, D. (2020). Special report: The simulations driving the world’s response to COVID-19. Nature, 580(7803), 316–318. https://doi.org/10.1038/d41586-020-01003-6

    Bettencourt, L. M. A., Ribeiro, R. M., Chowell, G., Lant, T., & Castillo-Chavez, C. (2007). Towards Real Time Epidemiology: Data Assimilation, Modeling and Anomaly Detection of Health Surveillance Data Streams. In D. Zeng, I. Gotham, K. Komatsu, C. Lynch, M. Thurmond, D. Madigan, B. Lober, J. Kvach, & H. Chen (Eds.), Intelligence and Security Informatics: Biosurveillance (Vol. 4506, pp. 79–90). Springer Berlin Heidelberg. https://doi.org/10.1007/978-3-540-72608-1\_8

    Biggerstaff, M., Kniss, K., Jernigan, D. B., Brammer, L., Bresee, J., Garg, S., Burns, E., & Reed, C. (2018). Systematic Assessment of Multiple Routine and Near Real-Time Indicators to Classify the Severity of Influenza Seasons and Pandemics in the United States, 2003–2004 Through 2015–2016. American Journal of Epidemiology, 187(5), 1040–1050. https://doi.org/10.1093/aje/kwx334

    Chae, S., Kwon, S., & Lee, D. (2018). Predicting Infectious Disease Using Deep Learning and Big Data. International Journal of Environmental Research and Public Health, 15(8), 1596. https://doi.org/10.3390/ijerph15081596

    Chen, N., Zhou, M., Dong, X., Qu, J., Gong, F., Han, Y., Qiu, Y., Wang, J., Liu, Y., Wei, Y., Xia, J., Yu, T., Zhang, X., & Zhang, L. (2020). Epidemiological and clinical characteristics of 99 cases of 2019 novel coronavirus pneumonia in Wuhan, China: A descriptive study. The Lancet, 395(10223), 507–513. https://doi.org/10.1016/S0140-6736(20)30211-7

    Chowell, G., Nishiura, H., & Bettencourt, L. M. A. (2007). Comparative estimation of the reproduction number for pandemic influenza from daily case notification data. Journal of The Royal Society Interface, 4(12), 155–166. https://doi.org/10.1098/rsif.2006.0161

    Cintron-Arias, A., Castillo-Chavez, C., Bettencourt, L. M. A., Lloyd, A., & Banks, H. T. (2009). The estimation of the effective reproductive number from disease outbreak data. Mathematical Biosciences and Engineering, 6(2), 261–282. https://doi.org/10.3934/mbe.2009.6.261

    Dukic, V., Lopes, H. F., & Polson, N. G. (2012). Tracking Epidemics With Google Flu Trends Data and a State-Space SEIR Model. Journal of the American Statistical Association, 107(500), 1410–1426. https://doi.org/10.1080/01621459.2012.713876

    Dureau, J., Kalogeropoulos, K., & Baguelin, M. (2013). Capturing the time-varying drivers of an epidemic using stochastic dynamical systems. Biostatistics, 14(3), 541–555. https://doi.org/10.1093/biostatistics/kxs052

    Erraguntla, M., Zapletal, J., & Lawley, M. (2019). Framework for Infectious Disease Analysis: A comprehensive and integrative multi-modeling approach to disease prediction and management. Health Informatics Journal, 25(4), 1170–1187. https://doi.org/10.1177/1460458217747112

    Fattah, J., Ezzine, L., Aman, Z., El Moussami, H., & Lachhab, A. (2018). Forecasting of demand using ARIMA model. International Journal of Engineering Business Management, 10, 184797901880867. https://doi.org/10.1177/1847979018808673

    Fauci, A. S., & Morens, D. M. (2012). The Perpetual Challenge of Infectious Diseases. New England Journal of Medicine, 366(5), 454–461. https://doi.org/10.1056/NEJMra1108296

    Fountain‐Jones, N. M., Machado, G., Carver, S., Packer, C., Recamonde‐Mendoza, M., & Craft, M. E. (2019). How to make more from exposure data? An integrated machine learning pipeline to predict pathogen exposure. Journal of Animal Ecology, 88(10), 1447–1461. https://doi.org/10.1111/1365-2656.13076

    Gambhir, M., Bozio, C., O’Hagan, J. J., Uzicanin, A., Johnson, L. E., Biggerstaff, M., & Swerdlow, D. L. (2015). Infectious Disease Modeling Methods as Tools for Informing Response to Novel Influenza Viruses of Unknown Pandemic Potential. Clinical Infectious Diseases, 60(suppl\_1), S11–S19. https://doi.org/10.1093/cid/civ083

    Halloran, M. E., & Longini, I. M. (2014). Emerging, evolving, and established infectious diseases and interventions. Science, 345(6202), 1292–1294. https://doi.org/10.1126/science.1254166

    Hethcote, H. W. (1989). Three Basic Epidemiological Models. In S. A. Levin, T. G. Hallam, & L. J. Gross (Eds.), Applied Mathematical Ecology (Vol. 18, pp. 119–144). Springer Berlin Heidelberg. https://doi.org/10.1007/978-3-642-61317-3\_5

    Hethcote, H. W. (2000). The Mathematics of Infectious Diseases. SIAM Review, 42(4), 599–653. https://doi.org/10.1137/S0036144500371907

    Huang, C., Wang, Y., Li, X., Ren, L., Zhao, J., Hu, Y., Zhang, L., Fan, G., Xu, J., Gu, X., Cheng, Z., Yu, T., Xia, J., Wei, Y., Wu, W., Xie, X., Yin, W., Li, H., Liu, M., … Cao, B. (2020). Clinical features of patients infected with 2019 novel coronavirus in Wuhan, China. The Lancet, 395(10223), 497–506. https://doi.org/10.1016/S0140-6736(20)30183-5

    Imai, C., Armstrong, B., Chalabi, Z., Mangtani, P., & Hashizume, M. (2015). Time series regression model for infectious disease and weather. Environmental Research, 142, 319–327. https://doi.org/10.1016/j.envres.2015.06.040

    Koehler, A. B., & Murphree, E. S. (1988). A Comparison of the Akaike and Schwarz Criteria for Selecting Model Order. Applied Statistics, 37(2), 187. https://doi.org/10.2307/2347338

    Kucharski, A. J., Russell, T. W., Diamond, C., Liu, Y., Edmunds, J., Funk, S., Eggo, R. M., Sun, F., Jit, M., Munday, J. D., Davies, N., Gimma, A., van Zandvoort, K., Gibbs, H., Hellewell, J., Jarvis, C. I., Clifford, S., Quilty, B. J., Bosse, N. I., … Flasche, S. (2020). Early dynamics of transmission and control of COVID-19: A mathematical modelling study. The Lancet Infectious Diseases, S1473309920301444. https://doi.org/10.1016/S1473-3099(20)30144-4

    Kwiatkowski, D., Phillips, P. C. B., Schmidt, P., & Shin, Y. (1992). Testing the null hypothesis of stationarity against the alternative of a unit root. Journal of Econometrics, 54(1–3), 159–178. https://doi.org/10.1016/0304-4076(92)90104-Y

    Li, Q., Guan, X., Wu, P., Wang, X., Zhou, L., Tong, Y., Ren, R., Leung, K. S. M., Lau, E. H. Y., Wong, J. Y., Xing, X., Xiang, N., Wu, Y., Li, C., Chen, Q., Li, D., Liu, T., Zhao, J., Liu, M., … Feng, Z. (2020). Early Transmission Dynamics in Wuhan, China, of Novel Coronavirus–Infected Pneumonia. New England Journal of Medicine, 382(13), 1199–1207. https://doi.org/10.1056/NEJMoa2001316

    Liu, T., Hu, J., Xiao, J., He, G., Kang, M., Rong, Z., Lin, L., Zhong, H., Huang, Q., Deng, A., Zeng, W., Tan, X., Zeng, S., Zhu, Z., Li, J., Gong, D., Wan, D., Chen, S., Guo, L., … Ma, W. (2020). Time-varying transmission dynamics of Novel Coronavirus Pneumonia in China [Preprint]. Systems Biology. https://doi.org/10.1101/2020.01.25.919787

    Mallapaty, S. (2020). What the cruise-ship outbreaks reveal about COVID-19. Nature, 580(7801), 18–18. https://doi.org/10.1038/d41586-020-00885-w

    Meloni, S., Perra, N., Arenas, A., Gómez, S., Moreno, Y., & Vespignani, A. (2011). Modeling human mobility responses to the large-scale spreading of infectious diseases. Scientific Reports, 1(1), 62. https://doi.org/10.1038/srep00062

    Metcalf, C. J. E., & Lessler, J. (2017). Opportunities and challenges in modeling emerging infectious diseases. Science, 357(6347), 149–152. https://doi.org/10.1126/science.aam8335

    Mizumoto, K., & Chowell, G. (2020). Transmission potential of the novel coronavirus (COVID-19) onboard the diamond Princess Cruises Ship, 2020. Infectious Disease Modelling, 5, 264–270. https://doi.org/10.1016/j.idm.2020.02.003

    Prem, K., Liu, Y., Russell, T. W., Kucharski, A. J., Eggo, R. M., Davies, N., Jit, M., Klepac, P., Flasche, S., Clifford, S., Pearson, C. A. B., Munday, J. D., Abbott, S., Gibbs, H., Rosello, A., Quilty, B. J., Jombart, T., Sun, F., Diamond, C., … Hellewell, J. (2020). The effect of control strategies to reduce social mixing on outcomes of the COVID-19 epidemic in Wuhan, China: A modelling study. The Lancet Public Health, S2468266720300736. https://doi.org/10.1016/S2468-2667(20)30073-6

    Ratnadip Adhikari, & R. K. Agrawal. (2013). An Introductory Study on Time series Modeling and Forecasting. LAP Lambert Academic Publishing. https://doi.org/10.13140/2.1.2771.8084

    Sun, Y., Koh, V., Marimuthu, K., Ng, O. T., Young, B., Vasoo, S., Chan, M., Lee, V. J. M., De, P. P., Barkham, T., Lin, R. T. P., Cook, A. R., & Leo, Y. S. (2020). Epidemiological and Clinical Predictors of COVID-19. Clinical Infectious Diseases, ciaa322. https://doi.org/10.1093/cid/ciaa322

    Wu, Z., & McGoogan, J. M. (2020). Characteristics of and Important Lessons From the Coronavirus Disease 2019 (COVID-19) Outbreak in China: Summary of a Report of 72 314 Cases From the Chinese Center for Disease Control and Prevention. JAMA, 323(13), 1239. https://doi.org/10.1001/jama.2020.2648

    Yang, E., Park, H., Choi, Y., Kim, J., Munkhdalai, L., Musa, I., & Ryu, K. (2018). A Simulation-Based Study on the Comparison of Statistical and Time Series Forecasting Methods for Early Detection of Infectious Disease Outbreaks. International Journal of Environmental Research and Public Health, 15(5), 966. https://doi.org/10.3390/ijerph15050966

    Zhang, X., Zhang, T., Young, A. A., & Li, X. (2014). Applications and Comparisons of Four Time Series Models in Epidemiological Surveillance Data. PLoS ONE, 9(2), e88075. https://doi.org/10.1371/journal.pone.0088075
