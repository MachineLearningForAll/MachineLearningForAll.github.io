---
layout: post
title: "Aalto Dictionary of ML – cross-entropy"
date: 2025-12-07
seo_title: "Generalization – How Machine Learning Models Handle Unseen Data"
seo_description: "Explore the concept of generalization in machine learning: how models trained on a dataset perform on new, unseen data."
markdown: kramdown
---

Consider a multi-class classification problem with feature space
 and finite label space . A
data point with feature vector  is represented by a probability
mass function (pmf)

over , where  denotes the probability that
the label of a randomly chosen data point with feature vector ,
equals . A hypothesis  outputs a predicted probability
mass function (pmf) . The associated cross-entropy loss is (Cover
and Thomas 2006)  The cross-entropy loss
quantifies the dissimilarity between the true probability mass function
(pmf)  and the predicted probability mass function (pmf)
. It is also a measure for the expected number of bits
required to encode labels drawn from the true probability mass function
(pmf)  when using a coding scheme optimized for the predicted
probability mass function (pmf)  (Cover and Thomas
2006).\
**Note.** For binary classification (with ), the cross-entropy
loss reduces to the logistic loss when employing a parametric model with
model parameters  such that
. Note that the representation
[](#equ_log_loss_gls_dict){reference-type="eqref"
reference="equ_log_loss_gls_dict"} of logistic loss requires encoding
the label space  by the values  and .\
See also: classification, logistic loss, probability mass function
(pmf).

Cover, T. M., and J. A. Thomas. 2006. *Elements of Information Theory*.
2nd ed. Hoboken, NJ, USA: Wiley.

---

📚 This explanation is part of the [Aalto Dictionary of Machine Learning](https://AaltoDictionaryofML.github.io) — 
an open-access multi-lingual glossary developed at Aalto University to support 
accessible and precise communication in ML.