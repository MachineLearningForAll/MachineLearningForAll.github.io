---
layout: post
title: "Aalto Dictionary of ML – Spectral Decomposition"
date: 2025-12-16
seo_title: "spectraldecomp"
seo_description: "spectraldecomp"
markdown: kramdown
---



Every normal matrix ${\bf A}\in \mathbb{C}^{d\times d}$ admits a
spectral decomposition of the form (Horn and Johnson 2013; Axler 2015)
$${\bf A}= \sum_{j=1}^{d} \lambda_{j} {\bf u}^{(j)} \big({\bf u}^{(j)})^{H} \nonumber \\ $$
with an orthonormal basis ${\bf u}^{(1)},\ldots,{\bf u}^{(d)}$.

![The spectral decomposition of a normal matrix ${\bf A}$ provides an
orthonormal basis ${\bf u}^{(1)}, {\bf u}^{(2)}$. Applying ${\bf A}$
amounts to a scaling of the basis vectors by the eigenvalues
$\lambda_{1},\lambda_{2}$.[]{#fig:eigenvectors-length_dict
label="fig:eigenvectors-length_dict"}](../images/spectraldecomp_tikz.png){#fig:eigenvectors-length_dict
width="80%"}

Each basis element ${\bf u}^{(j)}$ is an eigenvector of ${\bf A}$ with
corresponding eigenvalue $\lambda_{j}$, for $j=1,\ldots,d$.

Axler, Sheldon. 2015. *Linear Algebra Done Right*. 3rd ed. Cham,
Switzerland: Springer Nature.

Horn, R. A., and C. R. Johnson. 2013. *Matrix Analysis*. 2nd ed. New
York, NY, USA: Cambridge Univ. Press.

---

📚 This explanation is part of the [Aalto Dictionary of Machine Learning](https://AaltoDictionaryofML.github.io) — 
an open-access multi-lingual glossary developed at Aalto University to support 
accessible and precise communication in ML.
