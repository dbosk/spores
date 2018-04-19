#!/usr/bin/env python3

import numpy as np
import random
import pomegranate as pg
import string

STATE_NAME_PREFIX = "s"
OBSERVATION_NAME_PREFIX = "d"

DEFAULT_STATES_NAME = ["Home", "Outside", "Work"]
DEFAULT_STATES_NUMBER = len(DEFAULT_STATES_NAME)
DEFAULT_TRANSITION_MATRIX = \
    [[0.6, 0.4, 0.],
     [0.2, 0.6, 0.2],
     [0.,  0.4, 0.6]]

DEVICES_NUMBER_MIN = 3
DEVICES_NUMBER_MAX = 10

RANDOM_NAME_SIZE = 16


class Model:
    def __init__(self):
        self.n_states = 0
        self.n_obs = 0

        self.states = None
        self.observations = None
        self.A = None
        self.B = None
        self.defined = False

    def __str__(self):
        ret = str(self.__class__) + ': {\n'
        for k, v in self.__dict__.items():
            ret += "{}: {}\n".format(k, v)
        ret += "}"
        return ret

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

    def sample(self, length=20, previous_state=None):
        if not self.defined:
            print("Model is not defined.")
            return None, None
        if previous_state is not None and \
                (previous_state < 0 or previous_state >= self.n_states):
            raise ValueError(
                "Out of bounds initial state s0: \
                 should be in [[0, {}]]".format(self.n_states-1))

        initial_state = True
        state = 0
        sample_states = np.empty(length, dtype=np.int)
        sample_obs = np.zeros((length, self.n_obs), dtype=np.bool)

        for t in range(length):
            if initial_state:
                if previous_state is None:
                    # Random initial state
                    state = random.randint(0, self.n_states-1)
                else:
                    state = np.random.choice(
                        range(self.n_states), p=self.A[previous_state, :])
                initial_state = False
            else:
                state = np.random.choice(
                    range(self.n_states), p=self.A[state, :])
            sample_states[t] = state

            # Each device has an independant probability of being online
            for obs in range(self.n_obs):
                p_obs_in_state = self.B[state, obs]
                sample_obs[t, obs] = np.random.choice([False, True],
                                                      p=[1 - p_obs_in_state, p_obs_in_state])

        return sample_states, sample_obs

    def predict(self, up_to, obs, s_t=None):
        """Return a <t x s> matrix of the probability
        P[obs is online in t turns | current state is s]
        for all states s and t in [1, up_to].

        up_to -- turns to predict (int >= 1)
        obs -- currently studied observation (int >= 0 & < self.n_obs)
        s_t -- current state. Return a <t> matrix of proba for given state if not None
        """
        if s_t is not None and (s_t < 0 or s_t >= self.n_states):
            raise ValueError(
                'Out of bound s_t should be in range [[0, {}]]'.format(
                    self.n_states - 1))

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
                else:
                    # P[obs_(t+i)|S_t=current_state] =
                    # sum_(s in states)
                    # P[S_(t+1)=s|S_t=current_state] * P[obs_(t+i)|S_(t+1)=s]
                    for s in range(self.n_states):
                        p += self.A[current_state, s] * P[t-2, s]

                P[t-1, current_state] = p

        if s_t is None:
            return P
        else:
            return P[:, s_t]

    def fit(self, sequence):
        if not self.defined:
            raise EnvironmentError(
                'The model is not defined. Call set(...) method first.')

        if self.n_obs != sequence.shape[1]:
            raise ValueError("Wrong number of observations in sequence.\
                The model has {}, while the sequence has {}.".format(
                self.n_obs, sequence.shape[1]))

        for obs_id, obs_sequence in enumerate(sequence.T):
            obs = self.observations[obs_id]
            non_obs = "non_"+obs
            print("Observation "+obs)

            # We bake a sequence with obs and non_obs names
            obs_sequence = [obs if o else non_obs for o in obs_sequence]
            print("Sequence:")
            print(obs_sequence)

            print("A:")
            print(self.A)

            states = []
            print("B:")
            for s_id, state_name in enumerate(self.states):
                obs_uniform_proba = pg.DiscreteDistribution({
                    obs: self.B[s_id, obs_id],
                    non_obs: 1 - self.B[s_id, obs_id]
                })
                print(self.B[s_id, obs_id])
                states.append(pg.State(obs_uniform_proba, name=state_name))

            # And define a Pomegranates HMM with states obs and state non_obs
            # Using the previously computed parameters
            m = pg.HiddenMarkovModel()
            m.add_states(states)
            for s_id, s in enumerate(states):
                m.add_transition(m.start, s, self.init[s_id])
                for s_id2, s2 in enumerate(states):
                    m.add_transition(s, s2, self.A[s_id, s_id2])
            m.bake()

            # Let Pomegranate do the Baum-Welsh fitting
            print("fitting...")
            m.fit([obs_sequence])

            # Incorporate the Pomegranate parameters back into our model
            A = m.dense_transition_matrix()

            print("A:")
            print(A)
            # Transition matrix
            self.A = A[:self.n_states, :self.n_states]
            # Initial probability
            self.init = A[self.n_states, :self.n_states]
            # Emission probabilities for each state
            print("B:")
            for s_id in range(self.n_states):
                self.B[s_id, obs_id] = m.states[s_id].distribution.parameters[0][obs]
                print(self.B[s_id, obs_id])
            print()
        return


def get_default_model(observations):
    # [[0.5, 0.5, 0.],
    #  [0.3, 0.4, 0.3],
    #  [0.,  0.5, 0.5]]

    # [[1/n_states]*n_states]*n_states

    m = Model()
    n_obs = len(observations)
    m.set(
        DEFAULT_TRANSITION_MATRIX,
        [[1/n_obs]*n_obs]*DEFAULT_STATES_NUMBER,
        DEFAULT_STATES_NAME,
        observations)
    return m


def get_default(observations):
    return get_default_model(observations)


def get_random():
    devices_type = ['mobile', 'portable', 'fixed', 'server']
    devices_type_weights = [0.3, 0.3, 0.3, 0.1]
    # devices_type_cnt = np.zeros(len(devices_type), dtype=np.uint)
    n_devices = random.randint(DEVICES_NUMBER_MIN, DEVICES_NUMBER_MAX)

    n_states = DEFAULT_STATES_NUMBER
    A = DEFAULT_TRANSITION_MATRIX
    states_name = DEFAULT_STATES_NAME

    B = np.empty((n_states, n_devices), dtype=np.float64)
    devices_name = [None] * n_devices
    picked_devices_type = [None] * n_devices

    for obs_id in range(n_devices):
        device_type_id = 0
        # Always put a mobile device first
        if obs_id != 0:
            # device_type_id = random.randint(0, len(devices_type) - 1)
            device_type_id = np.random.choice(
                range(len(devices_type)), p=devices_type_weights)
        device_type = devices_type[device_type_id]
        picked_devices_type[obs_id] = devices_type[device_type_id]

        # Bake probabilities of connection depending on device type
        if device_type == 'mobile':
            # Mobile is highly available with varying probability
            p = 0.7 + 0.3 * np.random.sample(n_states)
        elif device_type == 'portable':
            # Portable is more or less available with varying probability
            p = 0.2 + 0.6 * np.random.sample(n_states)
        elif device_type == 'fixed':
            # Fixed is only available in one place ...
            p = np.zeros(n_states, dtype=np.float64)
            # ... with 0.4 to 1 probability
            p[random.choice([0, 2])] = 0.4 + 0.6 * np.random.sample()
        elif device_type == 'server':
            # Server has high availability regardless of the user's location
            p = [0.9 + 0.1 * np.random.sample()] * n_states

        B[:, obs_id] = p

        # Give the device a name
        devices_name[obs_id] = ''.join(
            [random.choice(string.ascii_lowercase+string.digits)
             for _ in range(RANDOM_NAME_SIZE)]) + '_' + device_type
        # devices_name.append(
        #     device_type + str(devices_type_cnt[device_type_id]))
        # devices_type_cnt[device_type_id] += 1

    # Create model with
    m = Model()
    m.devices_type = picked_devices_type
    m.set(A, B, states_name, devices_name)

    return m
