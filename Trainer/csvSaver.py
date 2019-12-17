import csv
import os
from hyperparams import HyperParameters


class Saver:
    def __init__(self, file_name: str, test_nr: int, model_id: str, save_interval: int, max_epochs: int, params: HyperParameters):
        self.params = params
        self.filename = file_name + str(test_nr)
        self.extension = '.csv'
        self.results = []
        wpath = os.getcwd()
        self.path = wpath + "/" + file_name + "/"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.make_file(model_id, save_interval, max_epochs)

    def make_file(self, model_id, save_interval, max_epochs):
        setup_dict = {'Model_id': model_id,
                             'Save_interval': save_interval,
                             'Max_epochs': max_epochs,
                             'Memory_size': self.params.mem_size,
                             'Learning_rate': self.params.lr,
                             'Epsilon_decay': self.params.eps_decay,
                             'Epsilon_min': self.params.eps_min,
                             'Max_tau': self.params.max_tau,
                             'Priority_factor': self.params.priority_percentage,
                             'Batch_size': self.params.batch_size,
                      }

        with open(self.path + self.filename + self.extension, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=setup_dict)
            writer.writeheader()
            writer.writerow(setup_dict)

    def write_to_file(self, epoch, time_avg, score_avg, agent_epsilon, agent_memory_size):
        results_dict = {'Epoch': epoch,
                             'Time_avg': time_avg,
                             'Score_avg': score_avg,
                             'Epsilon': agent_epsilon,
                             'Memory_size': agent_memory_size}

        with open(self.path + self.filename + self.extension, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=results_dict)
            if int(epoch) == 0:
                writer.writeheader()
            writer.writerow(results_dict)
