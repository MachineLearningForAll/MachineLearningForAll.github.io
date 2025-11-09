---
layout: post
title: "Aalto Dictionary of ML – Markov's inequality"
date: 2025-11-09
seo_title: "Generalization – How Machine Learning Models Handle Unseen Data"
seo_description: "Explore the concept of generalization in machine learning: how models trained on a dataset perform on new, unseen data."
markdown: kramdown
---



Consider a real-valued non-negative random variable (RV) $x$ for which
the expectation $\mathbb{E} \{ x\}$ exists. Markov's inequality provides
an upper bound on the probability $\mathbb{P}\left(x\geq a\right)$ that
$x$ exceeds a given positive threshold $a>0$. In particular,
{% raw %}$$\mathbb{P}\left(x \geq a\right) \leq \frac{\mathbb{E} \{ x\}}{a} \qquad \mbox{ holds for any } a > 0.
 \label{eq:markovsinequality_dict}$${% endraw %} This inequality can be verified by
noting that $\mathbb{P}\left(x \geq a\right)$ is the expectation
$\mathbb{E} {g(x)}$ with the function
{% raw %}$$g: \mathbb{R} \rightarrow \mathbb{R}: x' \mapsto \mathbb{I}_{\{x \geq a\}}(x').$${% endraw %}

As illustrated in the Figure below, for any positive $a>0$,
$$g(x') \leq x'/a \mbox{ for all } x' \in \mathbb{R}.$$ This obvious inequality 
implies Markov's inequality via the monotonicity of the Lebesgue integral (Folland 1999, 50).

<figure id="fig">
  <img src="../images/markovsinequality_tikz.png" alt="Illustration of Markov's inequality" width="80%">
</figure>


See also: expectation, probability, concentration inequality.

Folland, Gerald B. 1999. *Real Analysis: Modern Techniques and Their
Applications*. 2nd ed. New York, NY, USA: Wiley.

---

📚 This explanation is part of the [Aalto Dictionary of Machine Learning](https://AaltoDictionaryofML.github.io) — 
an open-access multi-lingual glossary developed at Aalto University to support 
accessible and precise communication in ML.
