# COSC 581 HW 7
**Name:** Sarah Huang

**Assignment Title**: HW 7

**Assignment Description**: 
1) Create an RSA encryption algorithm that uses 2048-bit primes p and q such that: p = 2q + 1.

2a) Bron-Kerbosch: Given a graph in modified DIMACS format. Use the Bron-Kerbosch algorithm to return the maximum clique.

2b) Cast the maximum clique problem as an ILP problem. Solve using Gurobi.


**Files**: 
- rsa.py - The final code that implements RSA encryption algorithm.
- (OPTIONAL) lib_generate_2048_primes.py - Script to generate a random p and q value given the bit size (ex. 2048) and follows p = 2q + 1.
- bron_kerb.py - The final code that implements Bron-Kerbosch algorithm to return maximum clique
- ilp.py - The final code to cast the maximum clique problem as an ILP roblem
- (OPTIONAL) generate_1000_graph.py - Script to generate 1000 vertice graphs using networkx

**Use**:
- To run rsa.py program in the terminal, type "python  ./rsa.py p  q  message_string".
- To run bron_kerb.py program in the terminal, type "python ./bron_kerb.py graph.txt".
- To run ilp.py program in the terminal, type "python ./ilp.py graph.txt".

**Runtimes**:
- Average Runtime of 2a: 0.45 seconds
    - Graph #1: 0.4353
    - Graph #2: 0.4558
    - Graph #3: 0.4559
    - Graph #4: 0.4226
    - Graph #5: 0.4764

- Average Runtime of 2b: 4.79 seconds
    - Graph #1: 4.7703
    - Graph #2: 4.9236
    - Graph #3: 4.7539
    - Graph #4: 4.6997
    - Graph #5: 4.7948


**Sources I Looked At**:
- RSA
    - https://rosettacode.org/wiki/Miller%E2%80%93Rabin_primality_test 
    - https://brilliant.org/wiki/extended-euclidean-algorithm/#extended-euclidean-algorithm
    - https://www.dcode.fr/rsa-cipher
    - https://asecuritysite.com/encryption/nprimes 

- Bron-Kerbosch & ILP
    - https://en.wikipedia.org/wiki/Bron%E2%80%93Kerbosch_algorithm 
    - https://stackoverflow.com/questions/49730947/writing-graph-object-to-dimacs-file-format
    - https://users.aalto.fi/~tjunttil/bliss/fileformat.html
    - https://support.gurobi.com/hc/en-us/articles/17278438215313-Tutorial-Getting-Started-with-the-Gurobi-Python-API