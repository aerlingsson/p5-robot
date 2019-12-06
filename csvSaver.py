import csv
import os


class Saver:
    def __init__(self, file_name, test_nr, model_id, save_interval, max_epochs, mem_size, lr, eps_decay, eps_min,
                 max_tau):
        self.model_id = model_id
        self.save_interval = save_interval
        self.max_epochs = max_epochs
        self.mem_size = mem_size
        self.learning_rate = lr
        self.eps_decay = eps_decay
        self.eps_min = eps_min
        self.max_tau = max_tau
        self.filename = file_name + test_nr
        self.extension = '.csv'
        self.fieldnames_setup = ['Model_id', 'Save_interval', 'Max_epochs', 'Memory_size', 'Learning_rate',
                                 'Epsilon_decay', 'Epsilon_min', 'Max_tau']
        self.fieldnames_results = ['Epoch', 'Time_avg', 'Score_avg', 'Epsilon', 'Memory_size']
        self.results = []
        wpath = os.getcwd()
        self.path = wpath + "/" + file_name + "/"
        if not os.path.exists(self.path):
            os.mkdir(self.path)
        self.make_file()

    def make_file(self):
        with open(self.path + self.filename + self.extension, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames_setup)
            writer.writeheader()
            writer.writerow({'Model_id': self.model_id,
                             'Save_interval': self.save_interval,
                             'Max_epochs': self.max_epochs,
                             'Memory_size': self.mem_size,
                             'Learning_rate': self.learning_rate,
                             'Epsilon_decay': self.eps_decay,
                             'Epsilon_min': self.eps_min,
                             'Max_tau': self.max_tau})

    def write_to_file(self, epoch, time_avg, score_avg, agent_epsilon, agent_memory_size):
        with open(self.path + self.filename + self.extension, 'a', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self.fieldnames_results)
            if int(epoch) == 0:
                writer.writeheader()
            writer.writerow({'Epoch': epoch,
                             'Time_avg': time_avg,
                             'Score_avg': score_avg,
                             'Epsilon': agent_epsilon,
                             'Memory_size': agent_memory_size})
