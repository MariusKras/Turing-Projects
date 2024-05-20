# Modeling Mental Health Status: Predicting Disorder Presence

![network header](header.png)

## Dataset

The dataset for this project can be found on [Kaggle](https://www.kaggle.com/datasets/tangodelta/api-access-behaviour-anomaly-dataset/data](https://www.kaggle.com/datasets/anth7310/mental-health-in-the-tech-industry)https://www.kaggle.com/datasets/anth7310/mental-health-in-the-tech-industry](https://www.kaggle.com/datasets/anth7310/mental-health-in-the-tech-industry)https://www.kaggle.com/datasets/anth7310/mental-health-in-the-tech-industry) (licensed under CC BY-SA 4.0).

This dataset comprises survey data from Open Source Mental Illness (OSMI) spanning the years 2014, 2016, 2017, 2018, and 2019. Conducted through convenience sampling, the survey gathers general information while focusing primarily on workplace attitudes toward mental health, with a particular emphasis on the experiences of individuals diagnosed with mental health disorders.

A notable feature of this dataset is the presence of numerous questions with similar or duplicated meanings. This repetition occurs due to the survey's branching logic, where specific responses lead respondents down different question paths. Although questions may appear similar, each is counted separately, with unanswered questions receiving a value of "-1".

## Objectives

The main objective of this project is:

> **Create a predictive model for identifying individuals with mental health disorders based on survey data.**

To achieve this objective, it was further broken down into the following 3 sub-objectives:

1. Conduct exploratory data analysis to identify good predictor features for modeling mental health status.
2. Develop a supervised classification model to predict whether individuals have a mental health disorder, do not have one, or have uncertain status.
3. Assess the performance of the developed model by evaluating key metrics such as precision, recall, and F1-score on the test and train datasets.

## Constraints

My goal is to introduce myself to machine learning, and I will simplify the task. 

* I will use logistic regression, one of the simplest methods for classification.
* Only five features will be selected based on my judgment of their potential as predictors. I will then conduct an analysis to validate their significance.
* The focus will not be on achieving high classification accuracy.

## Insights From EDA

Differences between individuals with and without a disorder:

* Individuals diagnosed with a mental condition typically have a family history of mental illness, while those without a diagnosis are usually without such a history.
* There is no apparent connection between workers mental state and the importance employers place on mental health.
* At work, individuals with disorders tend to report experiencing more well-handled responses to mental health issues themselves, but have observed fewer instances of such well-handled responses. In contrast, those without disorders mostly indicate they haven't experienced satisfactory responses.

## Model Evaluation and Potential Enhancements

Training Classification Report:

|           | Precision | Recall | F1-Score |
|-----------|-----------|--------|----------|
| No        | 0.56      | 0.54   | 0.55     |
| Uncertain | 0.49      | 0.22   | 0.31     |
| Yes       | 0.59      | 0.81   | 0.68     |


Testing Classification Report:

|           | Precision | Recall | F1-Score |
|-----------|-----------|--------|----------|
| No        | 0.56      | 0.45   | 0.50     |
| Uncertain | 0.40      | 0.20   | 0.27     |
| Yes       | 0.55      | 0.80   | 0.66     |

The overall accuracy is low. The model performs relatively well for the "Yes" category, however, it struggles with the "Uncertain" class. The "No" class shows moderate performance.

Possible immediate improvements:

1. Remove the 'Uncertain' category since it does not provide meaningful information. The presence of a disorder is a binary distinction.
2. Improve predictor selection by building a pipeline that assesses all features and identifies those with the most significant impact.

### A Note:

This project uses Plotly for plotting. Plotly visualizations are not visible on GitHub. To view the plots, you will need to run the notebook on your machine, Google Colab, or open the HTML file in the repository using your web browser.
