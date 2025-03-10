---
layout: post
title: "Explainable AI for Weather Prediction" 
date: 2024-11-28
seo_title: "Explainable AI for Weather Prediction: Enhancing Trust and Accuracy"
seo_description: "Explore how explainable AI models can improve weather prediction accuracy using data from the Finnish Meteorological Institute. Learn about user signals and data augmentation."
---

An essential requirement for trustworthy artificial intelligence (AI) is its explainability to human users [[^1]]. 
One principled approach to explainable AI is via the concept of simulatability: Roughly speaking, 
the better a specific human user can anticipate the behaviour of an AI, the more explainable it 
is (to this particular user). 

In the context of machine learning (ML), which is at the core of many current AI systems, we can formalize 
explainability by the notion of a user signal [[^2]]. The user signal is some subjective characteristic of 
data points. We can think of a user signal as a specific feature that a user assigns to a data point. 
We denote the user signal u(x) as a function of the raw features x of a data point. 


In this blog post, we explore explainable ML using a straightforward weather prediction example based 
on real-world data from the Finnish Meteorological Institute (FMI). The data was recorded at a FMI weather 
station near *Kustavi Isokari*

<iframe
  src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d2000.1234567890!2d21.123456!3d60.123456!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x1234567890abcdef%3A0xabcdef1234567890!2sIsokari%2C%20Kustavi%2C%20Finland!5e0!3m2!1sen!2sfi!4v1695775176803!5m2!1sen!2sfi&z=6"
  width="600"
  height="450"
  style="border:0;"
  allowfullscreen=""
  loading="lazy"
  referrerpolicy="no-referrer-when-downgrade">
</iframe>

We aim to create an explainable weather prediction model that aligns with human 
intuition. Some user signal models this intuition.

---

## Predicting Maximum Daytime Temperature with Explainable AI: A Real-World Example

Given historical weather data, we want to learn to predict the **maximum daytime temperature** (maxtemp)
solely from the **minimum daytime temperature** (mintemp). To this end, we first download weather recordings 
from the [FMI website](https://en.ilmatieteenlaitos.fi/download-observations)

![Finnish Meteorological Institute weather data download site](assets/PostEERM/FMIDownloadSite.jpg)

into a csv file `KustaviIsokari.csv`. The following code snippet reads in the downloaded data from the csv file 
and stores their features and labels in the variables `X` and `y`, respectively [[^3]], 
```python
# Load the data from the CSV file
file_path = "KustaviIsokari.csv"  # Replace with the actual file path
data = pd.read_csv(file_path)

# Extract relevant columns
data = data[["Maximum temperature [°C]", "Minimum temperature [°C]"]]

# Randomly select a specified number of data points
num_data_points = 15  # Specify the number of data points to select
data = data.sample(n=num_data_points, random_state=42)

# build feature matrix (with one column in this case) and label vector
X = data[["Minimum temperature [°C]"]]  
y = data["Maximum temperature [°C]"]    
```

Using the features `X` and labels `y`, we next train two basic ML models: 
a decision tree regressor and a polynomial regressor [[^4]]. 
```python
# Train a Decision Tree Regressor
maxdep=3 
dt_model = DecisionTreeRegressor(random_state=42, max_depth=maxdep)
dt_model.fit(X, y)

# Train a Polynomial Regression model
poly_degree = 7  # Specify the degree of the polynomial
poly_features = PolynomialFeatures(degree=poly_degree)
X_train_poly = poly_features.fit_transform(X)

poly_model = LinearRegression()
poly_model.fit(X_train_poly, y)  
```
We then plot the predictions of the trained models along with training data.

![AI models for weather prediction: Decision Tree and Polynomial Regression](assets/PostEERM/dtpolyreg.png)

How do you like the behaviour of the trained models? Both models predict increasing maxtemp for 
decreasing mintemp for very cold days (towards the left in the above plot). Moreover, the polynomial 
regressor predicts decreasing maxtemp with increasing mintemp for warm days (towards the right in 
the above plot). Predicting a decreasing maxtemp for increasing mintemp is counter-intuitive.


---

## Enhancing Explainability in AI with Data Augmentation

It seems reasonable to assume that higher min. temps. result in higher max.temps. 
We can exploit this intuition (or user knowledge) to regularize the above model training 
via data augmentation [[^5]]:

For each original data point, with mintemp x and maxtemp y, we add two 
additional data points: 
1. one with mintemp x+1 and maxtemp y+1
2. one with mintemp x-1 and maxtemp y-1 

Note that this data augmentation strategy can be interpreted as 
a specific choice for a user signal u(x). In particular, the user signal 
satisfies u(x+1)=y+1 and u(x-1)=y-1 for any data point (x,y) 
in the original training set. 

The following code snippet implements the above data augmentation and 
then retrains the decision tree and polynomial regression model.  
```python
# Augment the training set
augmented_data = data.copy()
augmented_data["Minimum temperature [°C]"] = data["Minimum temperature [°C]"] + 1
augmented_data["Maximum temperature [°C]"] = data["Maximum temperature [°C]"] + 1

augmented_data_minus = data.copy()
augmented_data_minus["Minimum temperature [°C]"] = data["Minimum temperature [°C]"] - 1
augmented_data_minus["Maximum temperature [°C]"] = data["Maximum temperature [°C]"] - 1

# Combine original and augmented data
data_augmented = pd.concat([data, augmented_data, augmented_data_minus], ignore_index=True)

# Split augmented data into predictors and target
X_augmented = data_augmented[["Minimum temperature [°C]"]]
y_augmented = data_augmented["Maximum temperature [°C]"]

# Train a Decision Tree Regressor
dt_model = DecisionTreeRegressor(random_state=42, max_depth=3)
dt_model.fit(X_augmented, y_augmented)

# Train a Polynomial Regression model
poly_degree = 7  # Specify the degree of the polynomial
poly_features = PolynomialFeatures(degree=poly_degree)
X_train_poly = poly_features.fit_transform(X_augmented)

poly_model = LinearRegression()
poly_model.fit(X_train_poly, y_augmented)
```

And here are the resulting trained DT and polynomial regressor, along with the 
original and augmented data points. Carefully note that the trained models 
now respect my (your?) intuition that maxtemp is monotonically increasing 
with mintemp. In this sense, these models can be considered more explainable 
than the trained models without data augmentation. 

![Improved weather prediction models with data augmentation](assets/PostEERM/dtpolyregexplainable.png)

## References and Further Reading on Explainable AI 

[^1]: High-Level Expert Group on Artificial Intelligence. (2019). Ethics guidelines for trustworthy AI. European Commission. [click here](https://digital-strategy.ec.europa.eu/en/library/ethics-guidelines-trustworthy-ai)

[^2]: A. Jung and P. H. J. Nardelli, "An Information-Theoretic Approach to Personalized Explainable Machine Learning," in IEEE Signal Processing Letters, vol. 27, pp. 825-829, 2020, doi: 10.1109/LSP.2020.2993176.  

[^3]: You can find a Python script to reproduce the presented results here: [click me](assets/PostEERM/ExplainableML.py) 

[^4]: A. Jung, *Machine Learning: The Basics,* Springer, 2022. https://doi.org/10.1007/978-981-16-8193-6

[^5]: L. Zhang, G. Karakasidis, A. Odnoblyudova, et al., "Explainable empirical risk minimization," in Neural Comput & Applic 36, 3983–3996 (2024). https://doi.org/10.1007/s00521-023-09269-3




