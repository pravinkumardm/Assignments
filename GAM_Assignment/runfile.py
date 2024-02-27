from ERModel import ERModel
import math
import numpy as np
from PageRank import PageRank


def iterate_ERgraphs(n, p, iterations):
    print(f'========================= m:{n}, p:{p}, iterations: {iterations}==========================')
    for _ in range(iterations):
        ergraph = ERModel(n,p)
        lcc, _ = ergraph.get_largest_component()
        print(f'np value = {n*p} | Largest Connected Component in the graph : {len(lcc)} | Number of Triangles in the graph: {ergraph.get_triangles()} ')
        if n*p < 1:
            print(f'\tTrue size of LCC: {len(lcc)} : From Formula(O(log(n))): {math.log(n)} Truesize > O(log(n)) : {len(lcc) > math.log(n)}')
        elif n*p == 1:
            print(f'\tTrue size of LCC: {len(lcc)} : From Formula(n^(2/3)): {n**(2/3)} Truesize == n^(2/3) : {len(lcc) == int(n**(2/3))}')
        else:
            print(f'\tTrue size of LCC: {len(lcc)} : From Formula(n): {n} Truesiz
                  e == n : {len(lcc) == int(n)}')
    print(f'===================================================')

iterate_ERgraphs(100, 0.04, 100)
iterate_ERgraphs(100, 0.5, 100)


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
pg.iterate_pagerank()

