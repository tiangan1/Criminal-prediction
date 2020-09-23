# Criminal-prediction

## Data Preparation
### This is a crime dataset of NYC. Recording informations such as the time of complaint happened, the location of complaint happened, the type of complaint, the age, sex, and race of suspect, the age, sex, and race of victim, etc. 
### We have total 108,753 observations and 30 variables in this dataset. Most of our variables are string value, witch need to be transformed to numeric value to do the deep learning. Also, a lot of missing value need to be filled.

## Data Visualization
### Mapping Cases and finding the Hot Spot on MYC
### Compute t-SNE and UMAP data of normalized sample data. (Perplexity of t-SNE is 30;Number of neighbors of UMAP are 20, and we used manhattan distance.)

## Deep Learning
### Training and testing.(Split training and testing data with years.Then normalize data.)
### Result of CNN (0.94, 0.88, 0.94)
### Result of LSTM (0.994, 0.992, 0.994)
### Result of Extra Trees (0.998, 0.998)
