---
layout: post
title: "Aalto Dictionary of ML – Sample"
date: 2025-10-28
seo_title: "Generalization – How Machine Learning Models Handle Unseen Data"
seo_description: "Explore the concept of generalization in machine learning: how models trained on a dataset perform on new, unseen data."
markdown: kramdown
---

In the context of machine learning (ML), a sample is a finite sequence
(of length ) of data points, .
The number  is called the sample size. Empirical risk minimization
(ERM)-based methods use a sample to train a model (or learn a
hypothesis) by minimizing the average loss (the empirical risk) over
that sample. Since a sample is defined as a sequence, the same data
point may appear more than once. By contrast, some authors in statistics
define a sample as a set of data points, in which case duplicates are
not allowed (Everitt and Skrondal 2010; Upton and Cook 2014). These two
views can be reconciled by regarding a sample as a sequence of
feature--label pairs, . The -th pair consists of the
features  and the label  of an unique underlying
data point . While the underlying data points
 are unique,
some of them can have identical features and labels.

<figure id="fig:sample-sequence_dict">
<div class="center">
<img src="../images/sample_tikz.png" style="width:80.0%" />
</div>
<figcaption>A sample viewed as a finite sequence. Each element of this
sample consists of the feature vector and the label of a data point from
an underlying population. The same data point may occur more than once
in the sample. <span id="fig:sample-sequence_dict"
data-label="fig:sample-sequence_dict"></span></figcaption>
</figure>

For the analysis of machine learning (ML) methods, it is common to
interpret (the generation of) a sample as the realization of a
stochastic process indexed by . A widely used assumption
is the independent and identically distributed assumption
(i.i.d. assumption), where sample elements
, for , are
independent and identically distributed (i.i.d.) random variables (RVs)
with a common probability distribution.\
See also: dataset, sequence, independent and identically distributed
assumption (i.i.d. assumption).

Everitt, B. S., and A. Skrondal. 2010. *The Cambridge Dictionary of
Statistics*. 4th ed. Cambridge, U.K.: Cambridge Univ. Press.

Upton, Graham, and Ian Cook. 2014. *A Dictionary of Statistics*. 3rd ed.
Oxford Univ. Press.

---

📚 This explanation is part of the [Aalto Dictionary of Machine Learning](https://AaltoDictionaryofML.github.io) — 
an open-access multi-lingual glossary developed at Aalto University to support 
accessible and precise communication in ML.