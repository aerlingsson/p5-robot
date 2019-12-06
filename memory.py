from heapq import heappush, heappop, heapify
from itertools import count
import numpy as np

class Memory:
    def __init__(self):
        self.memory = []
        heapify(self.memory)
        self.tiebreaker = count()

    def append(self, transition, tderr=100):
        heappush(self.memory, (-tderr, next(self.tiebreaker), transition))

    def append_batch(self, batch, errors):
        states, actions, rewards, next_states, dones = batch
        transitions = zip(states, actions, rewards, next_states, dones)

        for transition, error in zip(transitions, errors):
            self.append(transition, error)

    def get_distributed_batch(self, batch_size, priority_dist):
        batch = []
        random_size = int(batch_size * priority_dist)
        priority_size = int(batch_size * (1 - priority_dist))
        total_size = random_size + priority_size
        while total_size is not batch_size:
            if total_size < batch_size:
                random_size += 1
            elif total_size > batch_size:
                random_size -= 1
            total_size = random_size + priority_size
        batch.extend(self.priority_sample(priority_size))
        batch.extend(self.random_sample(random_size))

        states, actions, rewards, next_states, dones = zip(*batch)
        return states, actions, rewards, next_states, dones


    def priority_sample(self, batch_size):
        batch = []
        for _ in range(batch_size):
            batch.append(heappop(self.memory))
        batch = [e for (_, _, e) in batch]
        return batch

    def random_sample(self, batch_size):
        batch = []
        for _ in range(batch_size):
            rand_val = np.random.randint(low=0, high=len(self.memory))
            batch.append(self.memory.pop(rand_val))
        batch = [e for (_, _, e) in batch]
        return batch

    def size(self):
        return len(self.memory)
