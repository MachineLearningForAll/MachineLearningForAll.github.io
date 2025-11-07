---
layout: post
title: "Aalto Dictionary of ML – Markov's inequality"
date: 2025-11-07
seo_title: "Generalization – How Machine Learning Models Handle Unseen Data"
seo_description: "Explore the concept of generalization in machine learning: how models trained on a dataset perform on new, unseen data."
markdown: kramdown
---



Consider a real-valued non-negative random variable (RV) $x$ for which
the expectation $\expect\{ x\}$ exists. Markov's inequality provides an
upper bound on the probability $\prob{x\geq a}$ that $x$ exceeds a given
positive threshold $a>0$. In particular,
{% raw %}$$\prob{x \geq a} \leq \frac{\expect \{ x\}}{a} \qquad \mbox{ holds for any } a > 0.
 \label{eq:markovsinequality_dict}$${% endraw %} This inequality can be verified by
noting that $\prob{x \geq a}$ is the expectation $\expect{g(x)}$ with
the function
{% raw %}$$g: \mathbb{R} \rightarrow \mathbb{R}: x' \mapsto \indicatorfunc{\{x \geq a\}}(x').$${% endraw %}
As illustrated in Figure
[1](#fig:markovsinequality_dict){reference-type="ref"
reference="fig:markovsinequality_dict"}, for any positive $a>0$,
$$g(x') \leq x'/a \mbox{ for all } x' \in \mathbb{R}.$$ This implies
[\[eq:markovsinequality_dict\]](#eq:markovsinequality_dict){reference-type="eqref"
reference="eq:markovsinequality_dict"} via the monoticity of the
Lebesgue integral (Folland 1999, 50).

<figure id="fig">
  <img src="../images/markovsinequality_tikz.png" alt="The expectation $\expect\{x\}$ and the probability $\prob{x \geq a}$
of a non-negative random variable (RV) with probability distribution
$\probdist^{(x)}$ can be obtained via Lebesgue integral of $f(x') = x'$
and {% raw %}$g(x') = \indicatorfunc{\{x \geq a\}}(x')${% endraw %},
respectively." width="80%">
  <figcaption>
    The expectation $\expect\{x\}$ and the probability $\prob{x \geq a}$
of a non-negative random variable (RV) with probability distribution
$\probdist^{(x)}$ can be obtained via Lebesgue integral of $f(x') = x'$
and {% raw %}$g(x') = \indicatorfunc{\{x \geq a\}}(x')${% endraw %},
respectively.
  </figcaption>
</figure>

\
See also: expectation, probability, concentration inequality.

Folland, Gerald B. 1999. *Real Analysis: Modern Techniques and Their
Applications*. 2nd ed. New York, NY, USA: Wiley.

---

📚 This explanation is part of the [Aalto Dictionary of Machine Learning](https://AaltoDictionaryofML.github.io) — 
an open-access multi-lingual glossary developed at Aalto University to support 
accessible and precise communication in ML.
