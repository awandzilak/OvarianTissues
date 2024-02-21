# Classification of ovarian tissues based on their spectroscopic fingerprints

## Background
Ovarian cancer is a disease with high mortality rate. One of the techniques which can be useful in studying cancerous tissues is FTIR (Fourier Transform Infrared spectroscopy) because it enables studies of biomolecular composition. We had an access to big amount of historical samples (control and 3 types of diseased tissues) embedded in paraffin. However signal from paraffin overlaps with several vibrational bands from tissues. For this reason both samples in paraffine and after deparaffinization were studied.

## Goal
*	Compare usefulness of samples embedded in paraffine and after deparaffinization for classification of new cases.
*	Identify molecular features which play important role in separation between different types of diseased tissues.

## Data
The data contained information about intensity of FTIR vibrational bands representing groups such as: lipids, CH3 groups, CH2 groups, lipid saturation, alpha helix, beta forms and many other.
Thickness and density of specimens may vary. This issue could be addressed by normalization of FTIR spectra before fitting. However the data I had in hand were lacking this step. For this reason for further analysis selected ratios of intensities instead of intensities were used, which solved the lack of FTIR spectra normalization problem.
There were no missing values. The outliers were winsorized.

## EDA
For both paraffine and deparaffinized samples HGSC and MUC classes were much more represented comparing to CONTROL and ENDOM.

![cases distribution](https://github.com/awandzilak/OvarianTissues/blob/main/reports/cases_distribution.jpg)

After calculating the ratios we can see that in general CONTROL and ENDOM samples are well separated, however it may be a result of small population of samples. There are however some ratios which promising in terms of their ability to separate samples: lipid saturation, especially for separating between HGSC and MUC in deparaffinized samples and Amide III/Amide B ratio.

![Saturation of lipids](https://github.com/awandzilak/OvarianTissues/blob/main/reports/ratios_hist_1.jpg)
![Amide II/Amide B ratios](https://github.com/awandzilak/OvarianTissues/blob/main/reports/ratios_hist_16.jpg)

It can be noted that deparaffinization influenced lipid saturation significantly. It may be caused by washing out of lipids by the solvent used. Especially we can see a change in the saturation of lipids (CH2 vibrational band / CH3 vibrational band) which may suggest more efficient washing out of CH2 groups.

![Lipids/protein ratio](https://github.com/awandzilak/OvarianTissues/blob/main/reports/boxplot_lpratio.jpg)
![Lipids saturation](https://github.com/awandzilak/OvarianTissues/blob/main/reports/boxplot_lsat.jpg)

## Model building
For the purpose of classification Random Forest model was used. Both for the samples embedded in paraffine and samples after deparaffinization 3 approaches to building models were taken:
+	**A model classifying all 4 categories of samples: CONTROL, ENDOM, HGSC and MUC**

The model scored very well. Probably even too well for CONTROL and ENDOM categories. The small number of samples, coming from limited number of patients resulted in the risk that the model would learn how to recognize the patient rather than the disease.  For this reason, it was necessary to use a different method of splitting data into training and test sets than a completely random one. The new approach splits the samples so that all cases related to a specific patient go only to the training set or only to the test set. However, despite having ~1000 spectra for the CONTROL group and ~1700 spectra for ENDOM, the data originated from only two and four patients respectively. For this reason further models were built for HGSC and MUC samples only.
+ **A model classifying 2 categories of samples: HGSC and MUC**

This model was built to serve as a reference for the third model. Here the data were split randomly between the training and the test set – like in the previous model
+ **A model classifying 2 categories of samples: HGSC and MUC with patient-wise split**

The samples were split so that all cases related to a specific patient go only to the training set or only to the test set.

## Summary
### Model Performance

![F1 scores of all models](https://github.com/awandzilak/OvarianTissues/blob/main/reports/scores.jpg)

In the left side of the plot results for samples embedded in paraffine were presented. In the right side we can see data recorded after deparaffinization.

As we can see accuracy of CONTROL and ENDOM samples was the highest. This may be caused by the fact that all datapoints for these categories was originating from two and four patients respectively which could have made the model learn how to recognize the patient and not the disease.

Due to limited number of data for CONTROL and ENDOM and lack of possibility to collect more data the next two models considered only HGCS and MUC samples. The second model used the data randomly split between training and test sets, and the latter the data split in this way that all cases related to a specific patient go only to the training set or only to the test set. 

We can see that the second model (both for PAR and DEP) scores high - better than in the first model because binary classification is an easier problem. We can't exclude that the model is still learning to recognize the patients. 

In the third model we can see a decrease in the accuracy. It may be caused by the fact that now the model can't learn to recognize patients instead of the disease. It is also possible that the accuracy is smaller because the model was trained with smaller variety of data (coming from less patients). It is well visible when we compare scores for HGSC and MUC samples, knowing that despite using ~10 000 datapoints in each group the third model was trained on data coming from 17 patients for HGSC and 4 patients for MUC. Having the amount of data we have we can't say for sure if the model learned to recognize patients or the disease.

### Features conclusions

However we can say which features played the most important role for both types of samples: in paraffine and after deparaffinization.

For all models for the samples in paraffine, the most important features were ratios of 1080 cm-1 and 1240 cm-1 bands and their respective ratios with Amide I. Aforementioned bands are vibrations of phosphate groups and they are present in nucleic acids, so differences in their levels may be a result of increased replication in cancerous cells.

For the samples after deparaffinization the most important features for classification were: lipid saturation, which was masked by paraffine before and percentage of beta forms which carries information about changes in the secondary structure of proteines (which is known to change in cancerous tissues).
The plots below are plotted for the final model.

![Featires importance of the final model](https://github.com/awandzilak/OvarianTissues/blob/main/reports/features_importance_final_model.png)
