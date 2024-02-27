from ERModel import ERModel
import math
import numpy as np
from PageRank import PageRank


def iterate_ERgraphs(n, p, iterations):
    print(f'========================= n:{n}, p:{p}, iterations: {iterations}==========================')
    model_lc = []
    for _ in range(iterations):
        ergraph = ERModel(n,p)
        lcc, _ = ergraph.get_largest_component()
        model_lc.append(len(lcc))
        # print(f'np value = {n*p} | Largest Connected Component in the graph : {len(lcc)} | Number of Triangles in the graph: {ergraph.get_triangles()} ')
    if n*p < 1:
        print(f'\tTrue size of LCC (Mean for {iterations} iterations): {sum(model_lc) / len(model_lc)} : From Formula(O(log(n))): {math.log(n)} Truesize > O(log(n)) : {sum(model_lc) / len(model_lc) > math.log(n)}')
    elif n*p == 1:
        print(f'\tTrue size of LCC (Mean for {iterations} iterations): {sum(model_lc) / len(model_lc)} : From Formula(n^(2/3)): {n**(2/3)} Truesize == n^(2/3) : {sum(model_lc) / len(model_lc) == int(n**(2/3))}')
    else:
        print(f'\tTrue size of LCC (Mean for {iterations} iterations): {sum(model_lc) / len(model_lc)} : From Formula(n): {n} Truesize == n : {sum(model_lc) / len(model_lc) == int(n)}')
    # print(f'\tMean for 100 iterations: {sum(model_lc) / len(model_lc)}')


iterate_ERgraphs(100, 0.04, 100)
iterate_ERgraphs(100, 0.5, 100)



print(f'===================================================')
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

