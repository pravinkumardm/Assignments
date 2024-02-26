import random
import numpy as np

class ERModel:
    def __init__(self, n, p) -> None:
        self.n = n
        self.p = p
        self.generate_graph()
        self.generate_edge_list()
        self.generate_adj_list()

    def generate_graph(self):
        self.adj_mat = np.zeros((self.n, self.n))
        for i in range(self.n):
            for j in range(i+1,self.n):
                self.adj_mat[i][j] = random.choices([0,1], [1-self.p, self.p])[0]
        # self.halfmat = np.copy(self.adj_mat)
        self.adj_mat = self.adj_mat + self.adj_mat.T
    
    def generate_edge_list(self):
        ones = np.where(self.adj_mat == 1)
        self.edge_list = [x for x in zip(ones[0], ones[1])]
    
    def generate_adj_list(self):
        self.adj_list = {}
        for i in range(self.n):
            val = np.where(self.adj_mat[i]==1)[0].tolist()
            self.adj_list[i] = val
    