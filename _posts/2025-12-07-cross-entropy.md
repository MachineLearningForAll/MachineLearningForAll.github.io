---
layout: post
title: "Aalto Dictionary of ML – Cross-Entropy"
date: 2025-12-07
seo_title: "Cross-Entropy"
seo_description: "Cross-Entropy"
markdown: kramdown
---



Consider a multi-class classification problem with feature space
$\mathcal{X}$ and finite label space $\mathcal{Y}= \{1,\ldots,k\}$. A
data point with feature vector ${\bf x}$ is represented by a probability
mass function (pmf)
${\bf y}= (\truelabel_{1},\ldots,\truelabel_{k})^{T}$
over $\mathcal{Y}$, where $\truelabel_{c}$ denotes the probability that
the label of a randomly chosen data point with feature vector ${\bf x}$,
equals $c$. A hypothesis $h({\bf x})$ outputs a predicted probability
mass function (pmf) {% raw %}$\hat{{\bf y}} = (\predictedlabel_{1},\ldots,
 \predictedlabel_{k})^{T}${% endraw %}. The associated cross-entropy loss is (Cover
and Thomas 2006) {% raw %}$$\nonumber
 L\left(({\bf x},\hat{{\bf y}}),h\right)
 :=- \sum_{c=1}^{k}
 \truelabel_{c}\,\log \predictedlabel_{c}.$${% endraw %} The cross-entropy loss
quantifies the dissimilarity between the true probability mass function
(pmf) ${\bf y}$ and the predicted probability mass function (pmf)
{% raw %}$\hat{{\bf y}}${% endraw %}. It is also a measure for the expected number of bits
required to encode labels drawn from the true probability mass function
(pmf) ${\bf y}$ when using a coding scheme optimized for the predicted
probability mass function (pmf) {% raw %}$\hat{{\bf y}}${% endraw %} (Cover and Thomas
2006).\
**Note.** For binary classification (with $k= 2$), the cross-entropy
loss reduces to the logistic loss when employing a parametric model with
model parameters ${\bf w}$ such that
$\predictedlabel_{2}/\predictedlabel_{1}
 = \exp({\bf w}^{T}{\bf x})$. Note that the representation
[\[equ_log_loss_gls_dict\]](#equ_log_loss_gls_dict){reference-type="eqref"
reference="equ_log_loss_gls_dict"} of logistic loss requires encoding
the label space $\{1,2\}$ by the values $-1$ and $1$.\
See also: classification, logistic loss, probability mass function
(pmf).

Cover, T. M., and J. A. Thomas. 2006. *Elements of Information Theory*.
2nd ed. Hoboken, NJ, USA: Wiley.

---

📚 This explanation is part of the [Aalto Dictionary of Machine Learning](https://AaltoDictionaryofML.github.io) — 
an open-access multi-lingual glossary developed at Aalto University to support 
accessible and precise communication in ML.
