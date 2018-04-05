#!/usr/bin/env python3

import numpy as np
import random
import pomegranate as pg

STATE_NAME_PREFIX = "s"
OBSERVATION_NAME_PREFIX = "d"

DEFAULT_STATES_NAME = ["Home", "Outside", "Work"]


class Model:

    def __init__(self):
        self.n_states = 0
        self.n_obs = 0

        self.states = None
        self.observations = None
        self.A = None
        self.B = None
        self.defined = False

    def set(self, A, B, states=None, observations=None):
        self.A = np.array(A, dtype=np.float64)
        self.B = np.array(B, dtype=np.float64)
        self.n_states = self.A.shape[0]
        self.n_obs = self.B.shape[1]
        self.init = np.ones(self.n_states, dtype=np.float64)
        self.init = self.init / self.n_states

        if states is None or len(states) != self.n_states:
            self.states = [STATE_NAME_PREFIX +
                           str(i) for i in range(1, self.n_states+1)]
        else:
            self.states = states

        if observations is None or len(observations) != self.n_obs:
            self.observations = [OBSERVATION_NAME_PREFIX +
                                 str(i) for i in range(1, self.n_obs+1)]
        else:
            self.observations = observations

        self.defined = True

    def sample(self, length=20):
        if not self.defined:
            print("Model is not defined.")
            return None, None

        initial_state = True
        state = 0
        sample_states = np.empty(length, dtype=np.int)
        sample_obs = np.zeros((length, self.n_obs), dtype=np.bool)

        for t in range(length):
            if initial_state:
                # Random initial state
                state = random.randint(0, self.n_states-1)
                initial_state = False
            else:
                state = np.random.choice(
                    range(self.n_states), p=self.A[state, :])
            sample_states[t] = state

            # Each device has an independant probability of being online
            for obs in range(self.n_obs):
                p_obs_in_state = self.B[state, obs]
                sample_obs[t, obs] = \
                    np.random.choice([False, True],
                                     p=[1 - p_obs_in_state, p_obs_in_state])

        return sample_states, sample_obs

    def predict(self, up_to, obs):
        """Return a <t x s> matrix of the probability
        P[obs is online in t turns | current state is s]
        for all states s and t in [1, up_to].

        up_to -- turns to predict (int >= 1)
        obs -- currently studied observation (int >= 0 & < self.n_obs)
        """
        P = np.zeros((up_to, self.n_states), dtype=np.float64)

        for t in range(1, up_to+1):
            for current_state in range(self.n_states):
                p = 0
                if t == 1:
                    # P[obs_(t+1)|S_t=current_state] =
                    # sum_(s in states)
                    # P[S_(t+1)=s|S_t=current_state] * P[obs_(t+1)|S_(t+1)=s]
                    for s in range(self.n_states):
                        p += self.A[current_state, s] * self.B[s, obs]
                        # if obs == 1 and current_state == 2:
                        #     print(
                        #         "P[S_(t+1)={state}|S_t=Work] * \
                        #          P[{obs}_(t+1)|S_(t+1)={state}] \
                        #          = {x}*{y} = {p}".format(
                        #             state=self.states[s],
                        #             obs=self.observations[obs],
                        #             x=self.A[current_state, s],
                        #             y=self.B[s, obs],
                        #             p=self.A[current_state, s] \
                        #               * self.B[s, obs]))
                else:
                    # P[obs_(t+i)|S_t=current_state] =
                    # sum_(s in states)
                    # P[S_(t+1)=s|S_t=current_state] * P[obs_(t+i)|S_(t+1)=s]
                    for s in range(self.n_states):
                        p += self.A[current_state, s] * P[t-2, s]

                P[t-1, current_state] = p
        return P

    def fit(self, sequence):
        if not self.defined:
            print("Model is not defined.")
            return

        sequence_observations = np.unique(sequence)
        if len(sequence_observations) > self.n_obs:
            print(
                "Too many observations in sequence for the model. \
                Make a model with {} observations.".format(sequence_observations))
            return

        for obs in sequence_observations:
            if obs not in self.observations:
                print("'{}' is not a known observation.".format(obs))
                return

            non_obs = "non_"+obs

            # We bake a sequence with obs and non_obs only
            obs_sequence = [obs if o == obs else non_obs for o in sequence]

            obs_uniform_proba = pg.DiscreteDistribution({
                obs: 0.5, non_obs: 0.5
            })

            states = []
            for state_name in self.states:
                states.append(pg.State(obs_uniform_proba, name=state_name))

            # And define a Pomegranates HMM with states obs and state non_obs
            # Using the previously computed parameters
            m = pg.HiddenMarkovModel()
            m.add_states(states)
            for id_s, s in zip(states):
                m.add_transition(m.start, s, self.init[id_s])
                for id_s2, s2 in zip(states):
                    m.add_transition(s, s2, self.A[id_s, id_s2])
            m.bake()

            # Let Pomegranate do the Baum-Welsh fitting
            m.fit([obs_sequence])

            # Incorporate the Pomegranate parameters back into our model
            A = m.dense_transition_matrix()
            # Transition matrix
            self.A = A[:self.n_states, :self.n_states]
            # Initial probability
            self.init = A[self.n_states, :self.n_states]
            # Emission probabilities for each state
            obs_id = self.observations.index(obs)
            for s_id in range(self.n_states):
                self.B[s_id, obs_id] = \
                    m.states[s_id].distribution.parameters[0][obs]
        return


def get_default_model(observations):
    m = Model()
    n_states = len(DEFAULT_STATES_NAME)
    n_obs = len(observations)
    m.set(
        [[1/n_states]*n_states]*n_states,
        [[1/n_obs]*n_obs]*n_states,
        DEFAULT_STATES_NAME,
        observations)
    return m
