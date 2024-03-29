Date: Tue, 2 Oct 2018 20:27:54 +0000
From: NDSS 2019 HotCRP <noreply@ndss19.hotcrp.com>
Subject: [NDSS 2019] Author response period starts now!

Dear Authors,

The Program Committee of the 2019 Network and Distributed System Security
(NDSS) Symposium has decided that your paper #454:

Title: SP²ORES: Stateless Predictive Probabilistic Onion Routing for
E-Squads
Site: https://ndss19.hotcrp.com/paper/454

should advance to Round 2 of the reviewing process. Before the second round
begins, we are giving authors of all such papers the opportunity to respond
to the first round of reviews. Authors should pay special attention to the
“Questions for Authors’ Response” section of reviews, where present. The
Program Chairs have asked the reviewers to use this section to indicate the
most critical issues that, if successfully clarified, can possibly lead to
changes in opinions.

You have until Thursday, October 4th, at 11:59pm EDT to respond to these
reviews. Responses are limited to 500 words.

Thank you for submitting to NDSS 2019!

Best regards,
Alina Oprea and Dongyan Xu
2019 Program Co-Chairs

--------------------------------
Review #454A
===========================================================================

Overall merit
-------------
4. Accept

Reviewer expertise
------------------
2. Some familiarity

Novelty
-------
3. New contribution

Paper summary
-------------
This paper presents SP$^2$ORES, a distributed system for file
transferring that avoids centralized trust.  SP$^2$ORES leverages (1)
the ubiquity of **e-squads**, a group of devices that share an owner,
and (2) **proxemics**, the manner in which devices within proximity of
one another can communicate.  To enable SP$^2$ORES, the authors make
several contributions, including (1) modifying the Sphinx onion
routing protocol to support groups, (2) the SP$^2$OR protocol that
uses random-peer sampling (RPS) and availability estimates to maximize
the availability of onion routes, (3) a protocol for an e-squad to
estimate its availability, and (4) the file transfer service itself.

Comments for author
-------------------
This is very impressive work that somehow fits a number of interesting
contributions into a single conference paper submission.

I like the system model of this paper: Alice and Bob want to transfer
a file, don't want to involve a centralized party, and don't care
about leaving that file available for sharing after it's been
transferred.  This is a useful and realistic scenario, and I like the
unique tact of using e-squads and predictive behavior to deliver
messages/files.

The paper is very well-written, but it's definitely not an easy read.
Given the complexities involved, the paper could benefit from a
clearer operational diagram; Figure 1 presents the overall
architecture, but attempts to incorporate all of the various protocols
and components of the system into a single diagram.  I'd prefer to see
a clearer and more high-level figure that shows a complete file
transfer between two devices.

On a somewhat related note, Section IV spends a considerable amount of
time on the formalities of SphinxES and its security properties.  I
think some of the material here is better suited for an appendix; the
paper could be made a bit more readable by describing in more detail
the overall operation and purpose of the protocol (and how it fits
into the larger SP$^2$ORES picture) and stating its security
properties (but saving the subtle implementation details for an
appendix).

To me, the more interesting portion of the paper is the e-squad
overlay and techniques for predicting a device's availability
(presented in Sections IV-B and IV-C, respectively).

The paper does seem to gloss over SP$^2$ORES' location privacy
implications.  Devices publicly advertise its probability of being
connected in the near future, based on their past behavior.  I would
have liked to see some analysis of how much information is leaked due
to the advertising of $P'd$ -- that is, what can be inferred about a
device (and/or the device's owner) based on these advertisements?  Can
this privacy risk be quantified?

The evaluation struck me as being somewhat optimistic, since human
movements are emulated in the evaluation via a Hidden Markov Model
(HMM) and HMMs also serve as the models as to how SP$^2$ORES forms
predictive behavior.  In other words, the evaluation uses a model
that's assumed by the implementation, and thus misses how actual human
behavior (which doesn't strictly conform to HMMs) affects performance.

Overall, however, I think this paper exceeds the bar.  Routing in a
fully-decentralized manner is difficult.  SP$^2$ORES does quite a bit
of work to achieve such decentralization.  Performing availability
prediction using e-squads is a neat idea, and incorporating this into
onion routing protocols isn't straightforward.  SP$^2$ORES doesn't
introduce any especially novel protocols, but it does a very good job
of both composing and extending several existing techniques to achieve
its goals.  This is good work, and I appreciate the paper's formal
treatment of the problem.


Nit: toppology -> topology (page 4)


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


Review #454B
===========================================================================

Overall merit
-------------
2. Weak reject

Reviewer expertise
------------------
2. Some familiarity

Novelty
-------
3. New contribution

Paper summary
-------------
This paper describes a distributed file system to connect sets of devices associated with different users. The bulk of the paper is spent describing the SP(2)ORES system, but it is difficult to map the authors design onto their target deployment scenario. There are also numerous places where the description of the system is unclear (e.g., stating that communication should not require a circuit, but then using onion routing which will require some state set up). I also wonder if the overheads in terms of data transmitted and power used by this system would be incompatible with the small personal devices people keep with them.

Comments for author
-------------------
Detailed comments:

* Intro: you should cite the Mark Weiser vision/statement you refer to in the first sentence.

* Section III: It is not clear how you use onion routing without circuits

* Section III: It doesn’t seem reasonable to have a hash table of nodes that are globally selected across vs. select among a users nodes, or nodes that are in close proximity. Especially thinking of low-powered devices that are kept with users and store such personal data.

* Section IV: This section contains a lot of detail that perhaps would be more suited to an appendix. In general, the system design contains a lot of details that get in the way of understanding how the system actually fits together and operates in practice. 

* Section IV-V: The system is comprised of many different named subsystems. It is difficult to recall the functions of all these subsystems. It would help to include a figure or table mapping each of these subsystems to the task they actually accomplish. It'd also be a good place to highlight which of these you implemented yourself or which were existing. 

* Section V C: It seems like the data needed to predict availability of the different devices could present a privacy risk to users of this system. How does the system protect this information once it is determined?

* Section VII I wonder how realistic the performance evaluation is. I would have liked some discussion of how the Docker instances can be limited to emulate lower powered devices. Also, how do you distribute the user's e-squads over the five machines in your evaluation. I feel like putting these all on the same machine will hide impacts of unreliable wireless channels on your results. 

* Section VII It would have been nice to see models of user mobility that are available in existing traces vs. a totally simulated mobility/usage pattern here. E.g., traces from CRAWDAD (https://crawdad.org/) may be a good starting point to create more realistic user models. 

* In light of my prior comment, it would be worth commenting on how generalizable your results are/how much they are tied to your particulate performance evaluation set up.




