---
layout: post
title: "Dictionary of ML - Geometric Median"
date: 2025-05-12
seo_title: "Geometric Median – A Robust Alternative to the Mean in Machine Learning"
seo_description: "Understand the geometric median, a key concept in robust statistics and 
machine learning, minimizing total distance to data points and outperforming the mean under outliers."
markdown: kramdown

---

The **geometric median** $\boldsymbol{z}$ of a set of vectors $\boldsymbol{x}^{(1)}, \ldots, \boldsymbol{x}^{(n)}$ minimizes the total Euclidean distance:

$$
\boldsymbol{z} \in \arg\min_{\boldsymbol{y} \in \mathbb{R}^d} \sum_{i=1}^{n} \left\| \boldsymbol{y} - \boldsymbol{x}^{(i)} \right\|_2.
$$

This makes it a robust alternative to the mean when data includes outliers.

---

📚 This explanation is part of the [Aalto Dictionary of Machine Learning](https://AaltoDictionaryofML.github.io) — 
an open-access multi-lingual glossary developed at Aalto University to support 
accessible and precise communication in ML.
