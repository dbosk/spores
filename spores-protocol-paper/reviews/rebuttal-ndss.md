We would like to thank the reviewers for their constructive reviews. We structured our response by topic, referring to reviewers as RA and RB.

We agree with your joint suggestions for presentation (operational diagram, roles of protocols/subsystems; overview in text, details in appendix) and reference to Weiser; we will update the paper accordingly.

Regarding the concern about privacy threats from availability prediction data: @RB the data used for prediction is stored locally, only the predicted availability can be sampled. 
@RA leaks from prediction are analyzed in Section VI  (Device unlinkability), albeit for the worst case of extremely detailed availability data. In practice, leaks are constrained by separate address spaces (NFC for the out-of-band set-up step, and IP for availability sampling), public keys which can be replaced regularly, and availability prediction being coarse-grained and thus not unique. There are corner cases that allow for a link between IP addresses and devices and then potentially owners; for example when the adversary is behind the same NAT as the target, but even those are short-lived due to the coarse-grained prediction.

@RB on onion routing without circuits: this is likely a terminology issue. Onion routing is associated with circuits as Tor uses them, but it is not included in the definition in reference [21].  While Tor establishes circuits by maintaining a routing table at relays according to the onion layers, SphinxES (and Sphinx) defines a header format that encapsulates the routing information, hence the statelessness of SP²ORES.

@RB about global v. local sampling, we sample globally to achieve anonymity: if we only used our own devices, we would expose whom we are communicating with through our network metadata and Alice would reveal her devices to Bob.

Both reviewers expressed concerns regarding the realism of our evaluation. We have considered data collections such as Crawdad, but the data sets are not applicable as-is to our problem. Mobility is not a direct estimator of availability (e.g. mobile phones are available even during transitions), and it does not capture the interaction of a user with several of her devices, an emergent domain for which field data does not exist yet. We will keep an eye on data collections for any more directly applicable traces or empirical studies on availability of devices and their relation to data on mobility and other traces.

In the absence of data, HMM are commonly used for simulating user behavior. Should user behavior diverge markedly, however, the prediction module we use (based on plain Markov Chains) could be exchanged for one adapted to the scenario, for instance using privacy-preserving decentralized machine learning [Bellet, Guerraoui, et al, 2018].

@RB We agree that adapting our Docker setup to emulate more complex network properties and energy constraints could enrich our model. Our choice was to fold issues of network reliability and device resources together with device availability, considering that a poorly connected device is in effect only intermittently available. We believe that this provides an appropriate approximation for our experimental aims.


#Wannabe final version:

We would like to thank the reviewers for their constructive reviews. We structured our response by topic, referring to reviewers as RA and RB.

We agree with your joint suggestions for presentation (operational diagram, roles of protocols/subsystems; overview in text, details in appendix) and reference to Weiser; we will update the paper accordingly.

Regarding the concern about privacy threats from availability prediction data: @RB the data used for prediction is stored locally, only the predicted availability can be sampled. 
@RA leaks from prediction are analyzed in Section VI  (Device unlinkability), albeit for the worst case of extremely detailed availability data. In practice, leaks are constrained by separate address spaces (NFC for the out-of-band set-up step, and IP for availability sampling), public keys which can be replaced with configurable frequency, and availability prediction being coarse-grained and thus not unique. There are corner cases that allow for a link between IP addresses and devices and then potentially owners; for example when the adversary is behind the same NAT as the target, but even those are short-lived.

@RB on onion routing without circuits: this is likely a terminology issue. Onion routing is associated with circuits as Tor uses them, but it is not included in the definition in reference [21].  While Tor establishes circuits by maintaining a routing table at relays according to the onion layers, SphinxES defines a header format that encapsulates the routing information, hence the statelessness of SP²ORES.

@RB about global v. local sampling, we sample globally to achieve anonymity: if we only used our own devices, we would expose whom we are communicating with through our network metadata.

Both reviewers expressed concerns regarding the realism of our evaluation. We have considered data collections such as Crawdad, but the data sets are not applicable as-is to our problem. Mobility is not a direct estimator of availability (e.g. mobile phones are available even during transitions), and it does not capture the interaction of a user with several of her devices, an emergent domain for which field data does not exist yet. We will keep an eye on data collections for any more directly applicable traces or empirical studies on availability of devices and their relation to data on mobility and other traces.

In the absence of data, HMM are commonly used for simulating user behavior. Should user behavior diverge markedly, however, the prediction module we use (based on plain Markov Chains) could be exchanged for one adapted to the scenario, for instance using privacy-preserving decentralized machine learning [Bellet, Guerraoui, et al, 2018].

@RB We agree that adapting our Docker setup to emulate more complex network properties and energy constraints could enrich our model. Our choice was to fold issues of network reliability and device resources together with device availability, considering that a poorly connected device is in effect only intermittently available. We believe that this provides an appropriate approximation for our experimental aims.




-------------

[If room: In addition, devices in proximity can more easily be controlled by the same entity, thus they can more easily collude to de-anonymize the connections.]

Both reviewers expressed concerns regarding the realism of our evaluation. Mobility/connectivity datasets are not applicable as-is to our study, because they do not capture the interaction of a user with many of her devices, an emergent domain for which field data does not exist yet.
There are not a direct mapping between mobility and availability.... Mobility is not a direct indicator about availability ... Mobility is not a direct estimator of availability 
 Still, we thank you for the Crawdad pointer. OR We keep an eye on Crawdad in the hope that some dataset would be directly applicable to our work.
 [If room: we would need to make our own empirical study/a contribution.]

@RA <insert separated address spaces, short-lived public keys, coarse-grained availability, point to device unlinkability, still corner cases left that can link IP to device/owner [We must state clearly that most of the time [we don't know if it's most of the time], we **cannot** link IP to owner]>. 

In the absence of data, HMM are commonly used for simulating user behavior. Should user behavior diverge markedly, however, the prediction module we use (based on plain Markov Chains) would be enriched, for instance using privacy-preserving decentralized machine learning [Bellet, Guerraoui, et al, 2018].

@RB on onion routing without circuits: this is likely a terminology issue. Onion routing is associated with circuits as Tor uses them, but it is not included in the definition in reference [CL]. Sphinx is a header format for mix networks, and SP2ORES is technically a source-bounded random walk that adapts sphinx headers for encapsulating routing information (onion routing) per packet (SP2ORES, not IP) and not per connection (circuit).
but it is not mandatory according to [CL]. While Tor pre-establishes circuits by maintaining a routing table at relays, Sphinxes defines a header format that contains all the routing information, hence the statelessness of SP²ORES.
[Encrypted Tor packets == *cells*]


We therefore simulated user behavior using Hidden Markov chains, because of [versatile/widely used/ simplicity and realism [Gambs, Killijian, Núñez del Prado Cortez, 2012]

#Answers to questions

We merged all these issues by exhibiting different levels of availability.

###- Q1,RA: Location privacy, how much info is leaked by the published prediction?

We have an implicit assumption that when Alice and Bob communicate
out-of-band they use local addresses which are unlinkable to the
addresses used on the global network (\ie where they advertise P'd).

I remember this as being emphasized in the paper, but now that I read
the system model it's very implicit. This should be fine: they use IP
for global communication and bluetooth or NFC for out-of-band. These are
different address spaces, hence according to our assumption.

We also (implicitly) assume that the network addresses are independent
of the owner's attributes --- this should be emphasized in the paper!

This is not the case for IP: GeoIP services work for this reason. \Eg if
Bob knows where Alice lives he can use GeoIP to look for IPs that are
likely Alice's. Also if Alice and Bob are on the same NATed LAN, they
will have the same global address. Then Bob can read out every entry in
the RPS that has the same IP as himself. If there are only two and he
knows that Alice is also using the service (likely if she's exchanging
out-of-band data with him), then he can be quite certain that that's
Alice. Then if the probability is quite unique he can use that as
Alice's identifier, \ie he can track her addresses later (and use GeoIP
to follow her location).

In that sense, it's better for Alice to use her 4G connection instead of
local WiFi. Since then Bob cannot know her address on the global network
--- only that she's online (this case is analysed in the security
discussion, see "Device unlinkability" there). Of course, then her
ISP/phone carrier can learn her online behaviour, but they do that
anyway. Maybe the device-to-device of 5G will break this property for
Alice.

###- Q2,RB: It's unclear how onion routing is used without circuits:

This is a problem with terminology. There's first that CL called it
onion routing. Sphinx is a mixnet header. SphinxES is too. Technically,
routing is something stateless: there are no circuits in IP. We route
packets through multiple layers, using multiple layers of encryption,
hence onion routing. The problem is that, right now, onion routing is
synonymous to Tor. Tor sets up a state at each
node, \ie the circuit setup. We contain all that data in the header of
each packet, this is inherited from mixes. This gives us larger overhead
than Tor, as Tor can send just data without headers after the circuit
setup.

So we're correct in calling it onion routing. On the other hand we're
closer to a mix-cascade in that sense, except we don't do batching,
which is characteristic for mixes. Strictly speaking, using that survey
I used to characterize our work (of which I'm not sure how much remains
in the paper), we're technically a "source-routed bounded random-walk",
or maybe "source-bounded random-walk" is better.

###- Q3,RB: How are the overheads in terms of data transmitted and power used by this system for the small personal devices people keep with them?

I don't think processing one packet is much more expensive than an HTTPS handshake. But it's of course better to know, or at least make the estimate more explicit.

###Q4,RB: Why have a global DHT with all devices instead of choosing locally?

We use  a global DHT to achieve anonymity: if we only used our own devices, we would expose whom we are communicating with through our network metadata. In addition, devices in proximity can more easily be controlled by the same entity, thus they can more easily collude to de-anonymize the connections.

###- Q5,RB: Isn't the data needed for the prediction privacy sensitive, wouldn't the system endager users' privacy?
The data doesn't leave the user's own devices. The only data that leaves is in "aggregate from" in terms of the prediction. This information can be very coarse-grained, which it is in our evaluation.

###- Q6, RA, RB:  Both reviewers expressed concerns regarding the realism of our evaluation.

(See text above)


----
v2:
We use a general model for our predictions: a Markov chain (not Hidden) where states are the bitarray denoting which devices are connected: our prediction of a future device's availability solely depends on which devices are online now, given the history of the user's behavior. Our argument is that prediction enables onion routing. If we had field data, we would choose another prediction model, e.g. Recurrent Neural Networks, that are good candidates for classifying patterns in time series.
For the evaluation, we introduced the user's location (leading to a HMM), which enabled to model fixed appliances tied to a location (i.e. more realistic connection traces than mere random).
Despite the location transition matrix being fixed for all users, devices' connectivity traces exhibit much diversity, because the number, type and connection probability of devices are all different for each user. 

Our study did not consider connection unreliability or devices' scarce resources, because we collapsed these concepts with device availability: a user carrying their phone outside would have e.g. 65% of availability, because the phone's connection often drops and its resources are constrained. Using Docker to limit the resources of devices, or simulate an unreliable network with high latency would still benefit the soundness of our experiments, but certainly field data would be best.
Mobility/connectivity datasets are not applicable as-is for our study, because they do not capture the interaction of a user with many of their devices; we would need to engage in empirical experiments to get data on the emerging trend of e-squads.
Still, studies about user mobility prediction (like \url{https://crawdad.org/yonsei/lifemap/20120103/)} or connectivity over time are of interest to us, and we thank you for pointing us to Crawdad.

-----
v1:
We use a general model for our predictions: a Markov chain (not Hidden) where state are the bitarray stating which devices are connected:
our prediction of a future device's availability solely depends on which devices are online now, given the history of the user's behavior.
For the evaluation, we introduced a second stochastic process, the user's location, which enabled to model fixed appliances tied to a location.
Despite the location transition matrix being fixed for all users, devices' connectivity traces exhibit much diversity, because the number, type and connection probability of devices are all different for each user. 
We picked a Markov prediction model because it fits the simulated users behavior. If we had field  but we would strengthen our prediction with a more complex model if we had different (real world) traces of human behavior (e.g. Recurrent Neural Networks are good candidates for classifying patterns in time series).
Which leads to the question of ground data being absent from our experiments.
Mobility/connectivity datasets are not applicable as-is for our study, because they do not capture the interaction of a user with many of their devices; we would need to engage in empirical experiments to get data on the emerging trend of e-squads.
Still, studies about user mobility prediction (like \url{https://crawdad.org/yonsei/lifemap/20120103/)} or connectivity over time are of interest to us, and we thank you for pointing us to Crawdad.
Lastly, our study did not consider connection unreliability or devices' scarce resources, because we collapsed these concepts with the availability: 
a user carrying their phone outside would have e.g. 65% of availability, because the phone's connection is often dropping and its resources are constrained.
Using Docker to limit the resources of devices, or simulate an unreliable network with high latency would still benefit the soundness of our experiments.

#Adrien V1

Dear Reviewers,

Thank you for valuable comments! Notably, we understand that the relationship between SP²ORES' building blocks must be better explained (with a figure), that putting SphinxES details (Section IV) in an appendix would facilitate the presentation, and that we need to address the security risks of publicly advertising the devices' predicted availability.

We will develop on two other points: the statelessness of SP²ORES, and our evaluation testbed.

Reviewer B observed the following: "It is not clear how you use onion routing without circuits". 
In Tor, Alice creates onion routes by iteratively contacting her designated relays. The Onion Routers (OR) along the path must remember where to forward each received stream (i.e. they maintain a routing table).
Unlike it, SP²ORES builds routes by crafting a self-sufficient header beforehand, such that each OR will know where to forward each packet by simply decrypting the header.
// To enjoy sender-receiver anonymity in SP²ORES, both ends of the circuit must exchange their headers out-of-band.

You coined our evaluation optimistic, and doubted its realism. It is true that we only employ fabricated user traces (furthermore, using the same stochastic model as our prediction engine).
We aim to show that, assuming information on personal devices (such as timestamped connection/disconnection), it is possible to infer their future availability by modeling the user's behavior. 
Alas, real-world data that would fit our purpose is cruelly lacking (at least for academia). Adapting data such as wireless connectivity traces to fit our purpose (multi-device interaction over time) would by itself constitute a legitimate contribution: we firmly envisage to tackle it in the near future.

##Quotes from reviewers

###On the evaluation.
 
since human movements are emulated in the evaluation via a Hidden Markov Model
(HMM) and HMMs also serve as the models as to how SP$^2$ORES forms
predictive behavior.  In other words, the evaluation uses a model
that's assumed by the implementation, and thus misses how actual human
behavior (which doesn't strictly conform to HMMs) affects performance.
# @B Section VII I wonder how realistic the performance 
evaluation is. I would have liked some discussion of how the Docker instances 
can be limited to emulate lower powered devices. Also, how do you distribute 
the user's e-squads over the five machines in your evaluation. I feel like 
putting these all on the same machine will hide impacts of unreliable wireless 
channels on your results. 
# @B Section VII It would have been nice to see models of user 
mobility that are available in existing traces vs. a totally simulated 
mobility/usage pattern here. E.g., traces from CRAWDAD (\url{https://crawdad.org/)} 
may be a good starting point to create more realistic user models.
