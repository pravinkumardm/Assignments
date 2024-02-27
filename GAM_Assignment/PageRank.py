import numpy as np
import math

class PageRank:
    def __init__(self, adj_mat, iterations=10000, d=0.5, n_surfers=100) -> None:
        self.adj_mat = adj_mat
        self.iterations = iterations
        self.d = d
        self.n_surfers = n_surfers
        self.len_of_nodes = len(adj_mat)
        self.page_rank = np.ones(self.len_of_nodes) / self.len_of_nodes
        self.generate_adj_list()
        self.generate_edge_list()
        self.generate_parent_list()

    def generate_edge_list(self):
        ones = np.where(self.adj_mat == 1)
        self.edge_list = [x for x in zip(ones[0], ones[1])]

    def generate_adj_list(self):
        self.adj_list = {}
        for i in range(self.len_of_nodes):
            val = np.where(self.adj_mat[i]==1)[0].tolist()
            self.adj_list[i] = val

    def generate_parent_list(self):
        self.parent_list = {}
        for i in range(self.len_of_nodes):
            val = np.where(self.adj_mat.T[i]==1)[0].tolist()
            self.parent_list[i] = val
    
    def iterate_pagerank(self):
        for i in range(self.iterations):
            print(f"Iteration: {i}", end=" | ")
            if i == 0:
                surf = np.ones(self.len_of_nodes) * self.n_surfers
            new_rank = np.zeros(self.len_of_nodes)
            for j in range(self.len_of_nodes):
                children = self.adj_list[j]
                st = np.zeros(self.len_of_nodes)
                for each in children:
                    new_rank[each] += math.ceil(surf[j] / len(children))
            print(f'Updated Rank: {new_rank} | Old Rank: {surf} Matching updated and old: {all(new_rank == surf)}')
            
            if all(surf == new_rank):
                total = sum(surf)
                page_rank = [round((x*100)/total, 2) for x in surf]
                print(f'Final Page Ranks : {page_rank}')
                break
            surf = new_rank



if __name__ == "__main__":
    adjmat = np.array([
        [0,1,1,1,0,0,0,0,0,0],
        [0,0,1,0,0,0,0,0,1,0],
        [0,1,0,0,0,1,0,0,0,0],
        [1,0,0,0,0,0,0,0,0,1],
        [0,0,0,1,0,0,0,0,0,0],
        [0,0,0,0,0,0,1,0,0,0],
        [0,0,0,0,0,1,0,1,1,0],
        [0,0,0,0,0,1,0,0,0,0],
        [0,0,0,0,0,0,0,1,0,1],
        [0,0,0,0,1,0,0,0,1,0],
    ])
    pg = PageRank(adj_mat=adjmat)
    print(pg.adj_mat)
    print(pg.edge_list)
    print(pg.adj_list)
    print(pg.parent_list)
    pg.iterate_pagerank()
