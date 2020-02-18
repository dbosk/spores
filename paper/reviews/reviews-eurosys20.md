Date: Fri, 14 Feb 2020 18:24:22 +0000
From: EuroSys 2020 HotCRP <noreply@eurosys20.hotcrp.com>
To: Adrien Luxey <adrien.luxey@irisa.fr>, Sonja Buchegger <buc@kth.se>, David
 Bromberg <david.Bromberg@irisa.fr>, Daniel Bosk <dbosk@kth.se>, Francois
 Taiani <francois.taiani@irisa.fr>
CC: dmk@kth.se
Subject: [EuroSys 2020] Submission #343 "Spores: Stateless Predictive
 Onion..."

Dear authors,

Thank you for your submission to the 2020 European Systems Conference
(EuroSys 2020). We are sorry to inform you that your submission #343 was
not accepted and will not appear in the conference.

       Title: Spores: Stateless Predictive Onion Routing for E-Squads
     Authors: Daniel Bosk (KTH Royal Institute of Technology, Stockholm,
              Sweden)
              Yérom-David Bromberg (Univ Rennes, CNRS, Inria, IRISA,
              Rennes, France)
              Sonja Buchegger (KTH Royal Institute of Technology,
              Stockholm, Sweden)
              Adrien Luxey (Univ Rennes, CNRS, Inria, IRISA, France)
              François Taïani (Univ Rennes, CNRS, Inria, IRISA, France)
        Site: https://eurosys20.hotcrp.com/paper/343

We had the good fortune to receive many outstanding papers and could not
accept all of them. We hope that you'll find the feedback provided helpful
in deciding on next steps for your work.

We accepted 43 papers out of 234 submissions.

Please visit the submission site for reviews, comments, and related
information. Reviews and comments are also included below.

Contact the PC chairs at <pc-chairs@eurosys2020.org> with any questions or
concerns.

- EuroSys 2020 Submissions

Review #343A
===========================================================================

Overall merit
-------------
2. Weak reject

Reviewer expertise
------------------
3. Knowledgeable

Paper summary
-------------
Proposes an anonymous decentralized file transfer protocol, which is Tor-like except that it assumes
each participant has multiple devices, and uses gossipped information about which devices were
online recently to choose routes for forwarding (chunks of) files.  Unlike Tor, routes can comprise
multiple devices per "layer", so that if some devices in the layer happen to be offline, the
transfer can still succeed via another that is offline, whereas Tor would drop the message and
require a new route to be created.

Strengths
---------
It is an important problem to solve that (for example) journalists and their sources are not safe
from surveillance.  The paper contains some interesing ideas in this direction.

Weaknesses
----------
The motivation and solution do not seem to fit together.  The parties are assumed to physically meet
(or otherwise communicate securely) to exchange information in order to prepare for a file transfer
in future.  The route chosen is based on devices recently online (at the time of the route
preparation, *not* at the time of the actual transfer).  As far as one can tell from the
description, the evaluation does not take this into account, allowing the results to benefit from
locality (of availability information) that would likely not be valuable in practice if they file
transfer happens long after the route creation.  Security analysis is vague and unclear, evaluation
seems to be flawed and in general is not well presented.

Furthermore, the metadata exchanged when setting up the route (specifically the file descriptor)
contains information the depends on the file contents.  If this is available already and a secure
enough channel is available (e.g., physically exchanging files on storage devices), then why not
simply hand over the file then?  I don't think this is a fundamental limitation of the approach,
i.e., it could be modified such that the file contents do not need to be known in advance at route
creation time, but it is a weakness that they do as presented.

Comments for author
-------------------
"leveraging machine learning in order to predict peers’ availability".  I find it quite unclear from
the paper where this actually happens.  It seems that it is just from using V_RPS, which is
described only briefly and vaguely, but only talks about what devices were online recently, which
says nothing about "prediction".

At the end of the "Cryptographic Primitves" section, I think HE and HD are supposed to be ME and MD
respectively.

Algorithm 4, line 3 (similarly at line 8).  WHy not use more succinct notation: S \ d_A?

Algorithm 4, line 7 (similar at line 12).  Make clear that these "sends" refer to exchanging
information, perhaps physically, in contrast to the "send" used in Algorithm 3.

Algorithm 4, lines 18.  Presumably this could happen much later than the route creation?  Otherwise,
why not just hand over the file via the channel used to exhcange data for route creation?

I find the Security Analysis section unsatisfying.  The threats under analysis are not crisply
described, making it more difficult to understand what is being analyzed and why.  Various notation
is used without explanation (e.g., P^{SP}[ k adv. \in L]), and various leaps are made without
sufficient explanation and justification.  The penultimate paragraph of the section is difficult to
follow, and the last one even more so.  What does it mean for Tor to "implement" PORS?  On what
specific analyses are the stated conclusions based?

The experimental setup is largely presented without explanation or justification of the various
choices made.

The number of users in the experiments is orders of magnitude smaller than envisaged in the rest of
the paper, which calls into question how reperesentative the results are of the reality that the
authors imagine.  Why not also present some simulation results for larger numbers for at least some
of the experiments?

Under "An example", "nothing sums to one" is confusing and seems out of place.

The notion of predictability takes a log of a probability, which is undefined if the probability is
zero.  It is not clear why the log is taken here.  This notion should be better defined, motivated
and explained.  Also, the note in the caption of Fig. 4 "Higher is better, as this is a log score."
should be improved: "log score" is vague and it does not follow just from the fact that this is a
"log score" that higher is better.

"The bottom of the figure reads the amount of seized messages once routes are compromised, showing
how Spores circumvents traffic analysis attacks" is unclear.

"Remember that, when θ = 1, the PickLayer function is satisfied as long as the layer’s probability
of being offline (Poff L ) is lower than 1, that is, when there is one device per layer."  This is
not quite right. It should be *at least* one device per layer.

"It is interesting to note that, as θ shrinks exponentially, the number of relays per layer seems to
grow linearly: it is 2.5 for θ = 0.1, 4, when θ = 0.01, 6 when θ = 0.001, and 8 when θ = 0.0001."
Where do these "numbers of relays per layer" come from?  They are not evident in Fig. 6, which is
the only data mentioned in this section.


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


Review #343B
===========================================================================

Overall merit
-------------
4. Accept

Reviewer expertise
------------------
3. Knowledgeable

Paper summary
-------------
This paper proposes Probabilistic Onion Routing where onion routes may include several candidate relays at each hop, such that a message can go through the route as long as one candidate is online per hop.  The paper presents the design, implementation, security analysis and evaluation of Spores, an anonymous P2P file transfer protocol by leveraging the multiple devices owned and used regularly by users to serve as potential relay points in the network.  The system predicts device availability (through observation of a user's device usage patterns) and uses this to choose candidate relay nodes between a file sender and a file receiver.  Empirical evaluation
shows that the use of this "multipath" routing approach is effective in increasing the reliability of routes despite churn in the network and hinders traffic correlation attacks more effectively than Tor.

Strengths
---------
well written, interesting point in the design space of anonymity networks

Weaknesses
----------
some areas unclear; see below.

Comments for author
-------------------
This is a well-written paper that studies an interesting point in the design space of anonymity networks.  The idea of using probabilistic onion routing (essentially multi-path onion routing) is new and interesting.  

The evaluation shows significant improvement over Tor, without usage of cover traffic.  While the security model does not assume a Global Passive Adversary as is done by many state-of-the-art privacy systems these days, the authors make a good case that in the particular usage scenario envisioned (multiple ASs -- mobile carriers, household connections etc.) this adversary mdel is less likely.

Some comments for improvement:

The threat model greatly depends on secure peer sampling (citation [25]) to make the assumption that the global overlay cannot be tampered with and it is possible to get a uniform sample of online peers in the system.  This is a big assumption and I would have liked to have seen more about the threat model and security guarantees that secure peer sampling provides, given 
that the security of the proposed system relies on being able to avoid having adversarial relay candidates at each level of the path route.  Is it possible to eclipse a device's view of the gossip messages so that the device chooses a higher proportion of adversarial nodes on each relay hop, thus increasing the chances the adversary can view a particular user's file exchanges? 

I'm a little fuzzy on how exactly the route between the sender and the receiver is established.   How do you choose  a path through relay nodes that ensures that the last relay node can reach the receiver?  In particular, how does the system work if edge devices are behind NAT or firewalls?  In Tor, the resource being requested (e.g., a web site) is typically on a publically available address.   More details on how the path to the destination is found would be helpful.

Other comments:
p. 3 first column, first line  "when they are grabbed" --- what do you mean by "grabbed"??  Please change the term.

p. 6 "..but small enough that the view's stale descriptors get evicted in a reasonable amount of time" -- please clarify.

p. 7 how long are messages forward around e-squad members until the receiver is back online?  Since the e-squad belongs to the user, is this really necessary?  In some sense, it is enough for the message to reach one of the user's devices in the e-squad?   It would
be interesting to consider what the security implications are if the requirement is for the message to reach only one of the e-squad members.

Again, it is not clear how a route to at least one e-squad member, and ultimately to the recipient device is determined.  The gossiping mechanism appears to allow device nodes to learn about device nodes in the global array.  How is a path to the recipient device determined?
This is the main point that is unclear and should be addressed.

p. 12 citation [33] has no publication venue.


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


Review #343C
===========================================================================

Overall merit
-------------
3. Weak accept

Reviewer expertise
------------------
1. No familiarity

Paper summary
-------------
This paper proposes a probabilistic version of onion routing, with multiple possible relays per onion layer, with the aim of making it possible for intermittently connected devices such as smartphones to participate in the network, while limiting the risk of route failure due to disconnected devices. The devices self-learning their availability profile, which they gossip to others nodes on the network. On top of this network a file transfer protocol is proposed and implemented. File transfers are initiated and routes are created out of band. While the bulk of the paper focuses on the formal aspects of the protocol, the protocol has also been implemented and tested running in AWS VMs, with the focus on availability and resistance to collusion attacks. While the network protocol is targeted at personal devices, all evaluation is done one well-connected cloud VM instances, and the paper does not deal with practical aspects such as NAT traversal.

Strengths
---------
Well motivated and timely, good explanation of TOR and onion routing, and of the proposed POR protocol and its security properties.

Weaknesses
----------
Though the paper aims at building "e-squads", collections of personal devices and enable anonymous communication among them, the implementation is written in Go, which is rarely used on mobile devices, and only tested on well-connected Cloud VMs. The file transfer initiation protocol requires that parties meet or connect out of band, which seems like a major weakness that the paper does not acknowledge or plan to address as future work. The paper does not mention issues with NAT traversal that all P2P systems have traditionally had to address to gain wide-spread acceptance.

Comments for author
-------------------
I found this paper interesting and liked the Probabilistic Routing idea. It is well written and appears optically close to camera ready quality, with easy to read figures and pseudo-code listings to guide the reader along. As outlined above, my concerns are to the practicality of the approach.

First, unless I misunderstood the idea, it seems impractical that Bob and Alice (e.g., a whistleblower in the US and a journalist in the UK) would be able to securely establish routes out of band, or rather, if they were already connected by (as the paper suggests is a possibility) by NFC or a LAN, why would they not just exchange the secret files at that point? Or, is it the case that they would arrange the route ahead of time (weeks or months in advance) and perform the transfer at at later point in time? Would the route not have become stale at that point? I also think a P2P protocol that aims to run on user's devices needs to address the issue of NATs and how to provide connectivity across them, at least by acknowledging the problem or using some hand-wavy arguments about the inevitability of IPv6 adoption or promises of Future Work.

Next, the file transfer protocol, which divides the file into chunks similar to Bittorrent, allows chunks to be "cached" on peers in the network, but is that not a an avenue for a DoS attack that anybody could launch against the network, by filling all nodes with garbage data, to force them to evict the bona fide file chunks to not run out of space?

Finally, by being Peer2Peer, the authors hope that their system will eventually have more hosts that Tor. However, unlike Bittorrent's system of tit-for-tat file chunk exchanges, there seems to be little incentive to keep nodes running when the system is not actively being used, especially on mobile devices where users will want to conserve battery and save on network traffic.


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


Review #343D
===========================================================================

Overall merit
-------------
2. Weak reject

Reviewer expertise
------------------
2. Some familiarity

Paper summary
-------------
This paper proposes an anonymous file-transfer service that can be used by journalists and whistle-blowers to safely/anonymously share information. The service uses sets of end-user devices (e-squads) to form an onion-rotuing network.

Strengths
---------
-interesting and timely topic

Weaknesses
----------
-importance of the contributions is unclear
-design decisions are not fully justified

Comments for author
-------------------
The claim that previous peer-to-peer systems do not work due to lack of availability/churn of the participating nodes, is not completely accurate. While churn may be a problem in some networks, several peer-to-peer systems have been successfully deployed at large scale, including file sharing systems.

The contributions of the paper are not completely clear. The gossip-based protocols seem to be mostly re-used from previous work, and similarly for the onion the routing protocol. There is a contribution on creating a model of availability of devices, but the need to predict availability of an end-user's set of devices is not completely clear to me. It seems that many devices are now on 24x7 and many of these devices are quite powerful, for example many pocket-sized devices include 10s of GB of memory and 64-bit high-performance processors. 
 
The need for an out-of-band exchange of metadata using some other channel (the paper suggests Near Field Communication, LAN, Bluetooth, carrier pidgeon, etc.) poses some difficulties, since it constitutes a complex step that is necessary and requires a fully secure exchange between the participants.

Reliance on a random peer sampling service is also problematic. The paper states that this protocol relies on a reputation system to mitigate Byzantine attacks on the system, but it is not clear that such a mitigation is effective.


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


Review #343E
===========================================================================

Overall merit
-------------
2. Weak reject

Reviewer expertise
------------------
2. Some familiarity

Paper summary
-------------
The paper presents a system for federated anonymous / onion routing using a collection of personal/mobile devices owned by a user. 

The underlying technique for data transport is probabilistic onion routing (POR), a variant of onion routing where there are multiple candidates that a message can use at each hop and these candidates are selected amongst in a random manner. Unlike in traditional onion routing where the connection setup requires the negotiation of keys with one node per intermediate hop, POR requires the negotiation of sets of keys with each of multiple candidate nodes that will be used at each intermediate hop. Notably, PORs are one-way, so the connection setup requires separate forward and backward routes to be negotiated.

Strengths
---------
The key insight is to achieve the benefits of peer-to-peer anonymous file exchange without the attendant disruptions to connectivity resulting from _churn_ in nodes in the network, by using machine learning to predict availability of peers.

Weaknesses
----------
There are quite a few typos.

Comments for author
-------------------
- The paper is well structured (though there are quite a few typos, some of which I have highlighted below). The first two sections have good tutorial value and convey the idea of POR and SPORES in a reasonably compact presentation.

- The mathematical problem formulation in Section 2.1 could have been more rigorous but it at least does not feel superfluous.

- In Section 2: It seems odd to publish information about device times of predicted availability side by side with network address and public key. Doesn’t this publicly reveal information about the user’s behavior?

- In Section 2.4: Why is Alice beloved?

- How do you quantify “decent security properties”? The subsequent security analysis in Section 4 does begin to quantify the effect on the chosen threat model, but it would be useful to make a forward reference to that probabilistic evaluation here.

- For the product in Equation 4, do you want parentheses around the expression to the right of the product?

- For Figure 4, It’s not very meaningful to look at the absolute file transfer times. While I understand that you could not do a like-for-like comparison against Tor, you could have used the same infrastructure to evaluate implementations of the two techniques (like you do in Figure 6) and normalized the resulting times.

- In Figure 4, it wouldn’t hurt to also have the x-axis labeled in the upper figure, as you are not pressed for space and that would make the figure a bit less confusing.


Typos in Introduction:
> a intra-

...

> a onion


* * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * * *


Review #343F
===========================================================================

Overall merit
-------------
2. Weak reject

Reviewer expertise
------------------
2. Some familiarity

Paper summary
-------------
The paper presents an improvement over onion routing to achieve anonymous communication, called Spores. The idea is to leverage multiple personal devices (referred to as e-squad), and multiple relays at each layer of the onion to improve the reliability of routing as well as providing better privacy. Spores establish the routes out of band, then follows a bit-torrent like mechanism for file exchange.

Strengths
---------
Interesting idea leveraging multiple personal devices to improve reliability and privacy for onion routing. 

Spores incorporates multipath routing, and there is a good amount of security analysis of the benefit of multipath routing.

Weaknesses
----------
The scheme builds on implicit assumptions about mobile device availability and usage patterns that may not be realistic (e.g., power availability, incentive issues).

The scheme requires an out-of-band mechanism to establish the end-to-end routes.

The predictive model about user behavior model is speculative and not validated with real measurements. 

There is not much experimental evaluation of the proposed scheme, especially regarding efficiency consideration.

Comments for author
-------------------
In some sense, there are two core ideas in the paper: using multiple person devices, using multipath routing. Both have been considered in other problem domains, but might indeed present new opportunities for anonymous communication, and together they might indeed improve the reliability and privacy. However, the viability of the scheme rests on some implicit assumptions that certainly weren’t validated in the paper. 

I’m not entirely sure about the scenario you are suggesting. What does an e-quad overlay entail? Figure 3 seems to suggest Alice sends a private file to Bob completely via other devices these two own. Or do they involve other user devices along the way (i.e., through a part of the Internet, involving some relays over wired connections?

You assume routes are set up via some out-of-band mechanism. That may or may not be feasible, and may not be reasonable depending on what you have in mind. You suggested NFC as one possibility, but if two devices can communicate via NFC, why don’t they communicate directly via this private link?

Using multiple personal devices may have benefits, but here the discussion glosses over many practical issues. Indeed, most of us have multiple personal devices now, mostly like a subset of desktop, laptop, tablet, phone, plus other wearables (assuming smart home appliances and the like are not included in this discussion). First, it’s not clear how many you need (is 2 enough? or at least 4 devices?). Second, other than the desktop, the other common types of devices tend to be wirelessly connected and often battery powered. Having these devices act as relays will consume power locally. If someone else’s device is concerned, there could be an incentive issue (as seen in other collaborative mobile scenarios).

You propose some user behavior model to determine how to use the personal devices, but the modeling discussion needs better justification, and there is no validation in the paper of your proposed HMMs. First, whether some device is online depends on, the availability of the wireless networks, the user behavior across devices, and the battery states. The last one in particular is less deterministic or predictable. Do you have evidence a Markov model captures the device availability accurately? Second, it sounds like you assume the unavailable episodes are independent across devices, but that’s not always true. If I take a flight with my laptop, phone, and tablet, there will be times all three devices are offline. Related, for the multipath routing part to improve the privacy, you also appear to assume the relays at each layer are not correlated, but it’s not clear whether your algorithm guarantees this. 

The evaluation setup emulates individual devices with containers. How do you capture connectivity and battery status that are hallmark issues for resource-constrained personal devices?

In any case, there is not much experimental evaluation in the paper. For example, I’d have expected some evaluation of efficiency (how many extra relays you use, power consumption) vs privacy guarantee, and some performance vs the number of devices needed/used per device owner.

Comment @A1 by Reviewer C
---------------------------------------------------------------------------
Before the PC meeting, the reviewers had reached consensus not to accept this paper for publication. The paper was presented and discussed at the PC meeting, but the pre-existing consensus was not challenged and did not change.

