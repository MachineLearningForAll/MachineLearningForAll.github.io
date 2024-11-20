---
layout: page
title: "Research"
permalink: /research/
---

## Computational and Statistical Aspects of Total Variation Minimization for Federated Learning


![Federated Learning during pandemics](images/Pandemics.jpg)

Many important application domains generate collections of local datasets that are 
related by an intrinsic network structure (**big data over networks**). A timely application 
domain that generates such big data over networks is the management of pandemics. 

Individuals generate local datasets via their smartphones and wearables that measure biophysical 
parameters. The statistical properties of local datasets are related via different network structures that reflect physical ("contact networks"), 
social or biological proximity. In general, local datasets are heterogeneous in the sense of having different statistical distributions. 
However, we can often approximate local datasets that form a tight-knit cluster by a common cluster-specific distribution. 
 

To capitalize on the information in local datasets and their network structure, we have recently proposed networked exponential 
families as a novel probabilistic model for big data over networks. Networked exponential families are appealing statistically and 
computationally. They allow us to adaptively pool local datasets with similar statistical properties as training sets to learn personalized 
predictions tailored to each local dataset. We can compute these personalized predictions using highly scalable distributed 
convex optimization methods. These methods are robust against various types of imperfections (statistically and computationally) 
and typically offer a high level of privacy protection. 

*Relevant Publications:*

- A. Jung, "On the Duality Between Network Flows and Network Lasso," in IEEE Signal Processing Letters, vol. 27, pp. 940-944, 2020, {{<a href="https://ieeexplore.ieee.org/document/9103236"  target="_blank">doi: 10.1109/LSP.2020.2998400</a>}}. 
- A. Jung, "Networked Exponential Families for Big Data Over Networks," in IEEE Access, vol. 8, pp. 202897-202909, 2020, {{<a href="https://ieeexplore.ieee.org/document/9239959"  target="_blank">doi: 10.1109/ACCESS.2020.3033817</a>}}.
- A. Jung, A. O. Hero, III, A. C. Mara, S. Jahromi, A. Heimowitz and Y. C. Eldar, "Semi-Supervised Learning in Network-Structured Data via Total Variation Minimization," in IEEE Transactions on Signal Processing, vol. 67, no. 24, pp. 6256-6269, Dec., 2019, {{<a href="https://ieeexplore.ieee.org/document/8902040"  target="_blank">doi: 10.1109/TSP.2019.2953593</a>}}.
- A. Jung and N. Tran, "Localized Linear Regression in Networked Data," in IEEE Signal Processing Letters, vol. 26, no. 7, pp. 1090-1094, July 2019, {{<a href="https://ieeexplore.ieee.org/document/8721536"  target="_blank">doi: 10.1109/LSP.2019.2918933</a>}}.


## Explainable AI (XAI) 

![Federated Learning during pandemics](images/ProbModelXML.png)
Current AI systems make heavy use of machine learning. 
A key challenge for the widespread use of machine learning methods is the explainability of their predictions. We have recently 
developed a novel approach to constructing personalized explanations for the predictions delivered by machine learning method. 
We measure the effect of an explanation by the reduction in the conditional entropy of the prediction given the summary that a 
particular user associates with data points. The user summary is used to characterise the background knowledge of the "explainee" 
in order to compute explanations that are tailored for her. To compute the explanations our method only requires some training samples that consists of data points and their corresponding 
predictions and user summaries. Thus, our method is model agnostic and can be used to compute explanations for different machine learning methods. 

*Relevant Publications:*

- L. Zhang, G. Karakasidis, A. Odnoblyudova, et al. Explainable empirical risk minimization. Neural Comput & Applic 36, 3983–3996 (2024). {{<a href="https://doi.org/10.1007/s00521-023-09269-3"  target="_blank">link</a>}}  
- A. Jung and P. H. J. Nardelli, "An Information-Theoretic Approach to Personalized Explainable Machine Learning," in IEEE Signal Processing Letters, vol. 27, pp. 825-829, 2020, {{<a href="https://ieeexplore.ieee.org/document/9089200"  target="_blank">doi: 10.1109/LSP.2020.2993176</a>}}.

