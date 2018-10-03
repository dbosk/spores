Date: Fri, 22 Jun 2018 19:20:40 +0200
From: SRDS 2018 <srds2018@easychair.org>
X-Mailer: MIME::Lite 3.030 (F2.84; A2.14; B3.15; Q3.13)
Subject: SRDS 2018 notification for paper 90

Thank you for your submission 90 to SRDS 2018.  This year we received a large 
number of high-quality submissions. Unfortunately, we regret to inform you that 
your manuscript could not be accepted.  We have attached the reviews. We hope 
that they will assist you in revising the paper.

Please consider submitting to open calls of SRDS 2018:
Posters and Fast Abstracts: http://www.lasid.ufba.br/srds2018/view/postersabstracts.php
Workshops: http://www.lasid.ufba.br/srds2018/view/workshops.php

Best regards,
 
SRDS 2018 TPC-Co-chairs.


----------------------- REVIEW 1 ---------------------
PAPER: 90
TITLE: SPORES: Stateless Predictive Onion Routing for E-Squads
AUTHORS: Daniel Bosk, Yérom-David Bromberg, Sonja Buchegger, Adrien Luxey and François Taiani

Overall evaluation: -1 (weak reject)

----------- Overall evaluation -----------
The paper presents an interesting scheme for sharing files among groups of devices. The paper uses onion routing for privacy and predictions using HMMs to maximize availability.

----------- Strong points -----------
The paper is interesting, solves an interesting problem, and there’s novelty in the solution proposed.

----------- Weak points -----------
The paper in it’s current state suffers from too many presentation weaknesses: missing explanations, terms that are not defined, and phrases that are hard to understand. More details in the next section.

----------- Detailed review -----------
Sec. 2 supposedly presents the system model but it says little about it (e.g., no cryptographic, time or fault assumptions are made). Clouds appear suddlenly without explanation. The introduction suggests that there is no cloud, only mobile devices, then in sec. 2 the cloud appears without the paper saying anything about it. The mention to “friends" is equally strange. Even more because the friends are said to be able to "become the most powerful potential attackers”. The notion of "global network adversary” is not defined.

Sec. 3 presents the scheme. Onion routing is crucial but there is no explanation on how it works. Same thing for broadcast encryption. The relation between key regeneration and joining/leaving a group is not explained. The DeBE scheme is explained but in a confusion way. The ANOBE scheme is not explained (e.g., why is it anonymous?). POR appears a few times before it is actually explained. Probabilistic broadcast encryption is not defined (i.e., what does Sprinkler do?). There is no introduction to the notion of predicting the future user behaviour, only a detailed explanation using HMMs. The concept of failure threshold is also not properly defined. 

All these limitations make the paper hard to follow in its current form.


----------------------- REVIEW 2 ---------------------
PAPER: 90
TITLE: SPORES: Stateless Predictive Onion Routing for E-Squads
AUTHORS: Daniel Bosk, Yérom-David Bromberg, Sonja Buchegger, Adrien Luxey and François Taiani

Overall evaluation: 0 (borderline paper)

----------- Overall evaluation -----------
The paper is well-structured, presents a promising contribution, and a good review of the related works. However, the proposed approach is poorly presented, and the performance evaluation needs to be improved.

----------- Strong points -----------
* The paper is well-structured;
* It is a promising contribution;
* A good review of the related works.

----------- Weak points -----------
* The algorithms and performance evaluation are poorly presented: variables and operations aren’t properly presented; same notation with different meanings; different notations for the same meaning etc.

* I couldn’t relate the churn rate to the protocol performance

* The computing costs of the proposed approach weren’t evaluated.

----------- Detailed review -----------
1. SUMMARY OF THE PAPER
----------------------------------------
This paper proposes a strategy to overcome the low performance caused by high churn of nodes when an overlay peer-to-peer (p2p) network is used to support anonymous file-sharing between nodes (i.e., computing devices). Thus, the main idea is to modify a secure p2p routing mechanism to consider routes with a set of nodes on each hop. The set of nodes is selected based on its availability - i.e., the probability of it being online (available) during the data routing for the destination node. Such a device availability is predicted using a well-known stochastic model, named as Hidden Markov Model, which estimates the future device availability based on the current user’s location. The paper discusses a set of experiments that evaluates the performance of the proposed approach. In addition, different issues related to the security of the proposed solution are also discussed in the paper. 

2. REVIEW OF THE PAPER
----------------------------------------
The paper is well-structured and well-written (except sections III and IV). It addresses an important problem and presents an interesting approach. The paper also presents a good review of related works.

In my option, the presentation of the proposed approach and its performance evaluation must be improved. 

The algorithms presented are poorly described, for example: functions in Figures 3-5 are unclear because they are presented without describing some of their variables and some declared operations; the letter “S” is used to represent two clearly distinct things (one-time signature scheme and user’s locations); The function “ExtendRoute”, which is used to create routes based on the proposed approach, has an ambiguous interface – sometimes it's defined with two parameters and sometimes it's used with three parameters. 

The performance evaluation is also hard to follow, for instance: it uses a notation different from which was defined during the presentation of the proposed approach; the description of the Figure 7 is quite confusing (variables and notations used in text is different than those used in the Figure). 

The paper puts high churn as the problem for the poor performance of p2p based approaches. However, the effects of the node’s churn in the proposed approach weren’t clearly discussed. In addition, the performance of the proposed approach wasn’t compared to others p2p-based approaches. The computing costs of the proposed approach also weren’t properly analyzed – it is an important issue if the solution must be able to run at distinct kinds of devices, such as smartphones, tablets etc. 

3. OTHER ISSUES
-------------------------------------
* Review all text because there are a lot of typos, for example: “$V_{RPS}$containing”, “$l_{view}$other”, “H_Alice” and “H_Bob”, “$V_{RPS}$with”, “$V_{RPS}$is”etc.

* Page 3: The IND-CCA PKE scheme is pointed in the text without explanation or citation of references.

* Page 8: “for i \in {a, b}” what do “a”, “b” mean?

* Figure 5 (line 10): should it use “< theta” instead of “> theta”?

* Figure 7: what do “p”, “w”, “h”, “l” mean?


----------------------- REVIEW 3 ---------------------
PAPER: 90
TITLE: SPORES: Stateless Predictive Onion Routing for E-Squads
AUTHORS: Daniel Bosk, Yérom-David Bromberg, Sonja Buchegger, Adrien Luxey and François Taiani

Overall evaluation: 1 (weak accept)

----------- Overall evaluation -----------
This paper proposes a privacy-preserving file sharing service based on stateless predictive Onion Routing for e-squads (the multiple computing devices that form a personal squad of an entity/user). The proposed solution is fully decentralized and does not rely on any external storage service. The motivation is the need for sharing files among users and at the same time preserve end-to-end privacy. The paper motivates the work, presents the system model, discusses the design of the solution, and presents a performance evaluation and a discussion of the main security aspects.

The proposed solution seems to be sound and indeed fulfill the requirements established by the authors. The paper is very well written and, although understanding multiple concepts and techniques is required, the paper does a good job explaining the solution. The main limitation of the paper is the performance evaluation: although experiments were conducted and results are discussed, it is not clear how the solution will behave in terms of performance overhead compared with other approaches. Authors claim that the performance is acceptable, but one main question what a transfer time of 56s +- 36s for a chunck of a file to reach the destination really means…

----------- Strong points -----------
- Problem addressed is relevant and the proposed solution is sound, integrating multiple approaches to address the different issues involved.

- The paper is well written and easy to understand.

- The performance of the solution is evaluated and the main security aspects (and limitations) are adequately discussed.

----------- Weak points -----------
- Evaluation is limited, not clearly showing the performance final performance of the proposed approach.

- Some security aspects remain unclear and the authors simply remove them from the scope of the paper (e.g. how much the system is vulnerable to DoS attacks that can learn more about the system).

----------- Detailed review -----------
This paper proposes a privacy-preserving file sharing service based on stateless predictive Onion Routing for e-squads (the multiple computing devices that form a personal squad of an entity/user). The proposed solution is fully decentralized and does not rely on any external storage service. The motivation is the need for sharing files among users and at the same time preserve end-to-end privacy. The paper motivates the work, presents the system model, discusses the design of the solution, and presents a performance evaluation and a discussion of the main security aspects.

The proposed solution seems to be sound and indeed fulfill the requirements established by the authors. The paper is very well written and, although understanding multiple concepts and techniques is required, the paper does a good job explaining the solution. The main limitation of the paper is the performance evaluation: although experiments were conducted and results are discussed, it is not clear how the solution will behave in terms of performance overhead compared with other approaches. Authors claim that the performance is acceptable, but one main question what a transfer time of 56s +- 36s for a chunck of a file to reach the destination really means…

In terms of improving the paper, I would recommend designing a different experiment to adequately assess performance. Also, even if some security aspects are left for future work, please provide some reasoning about the main issues.


