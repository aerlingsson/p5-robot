class HyperParameters:
    def __init__(self, mem_size: int, lr: float, eps_decay: float, eps_min: float, max_tau: int, gamma: float,
                 priority_percentage: float, batch_size: int):
        super().__init__()
        self.mem_size = mem_size
        self.lr = lr
        self.eps_decay = eps_decay
        self.eps_min = eps_min
        self.max_tau = max_tau
        self.gamma = gamma
        self.priority_percentage = priority_percentage
        self.batch_size = batch_size

    def __str__(self):
        return str(vars(self))