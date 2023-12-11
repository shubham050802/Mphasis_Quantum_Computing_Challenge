import dimod
from dimod import Binary, ConstrainedQuadraticModel, quicksum
from dwave.system import LeapHybridCQMSampler
import numpy as np
from code_1 import find_all_flight_paths_all_pairs
from dwave.system import DWaveSampler, EmbeddingComposite, FixedEmbeddingComposite
from minorminer.busclique import find_clique_embedding
import numpy as np
import dwave.cloud as dc

cqm = ConstrainedQuadraticModel()

def cqm_formulation(K, M):
    cqm = ConstrainedQuadraticModel()
    
    for i in range(K):
        for j in range(M):
            cqm.add_variable('BINARY', f'X_{i}_{j}')
    
    X = {(i, j): dimod.Binary(f'X_{i}_{j}')
         for i in range(K)
         for j in range(M)}
    
    for j in range(M):
        cqm.add_constraint((quicksum(X[i,j] for j in range(M)))==1)