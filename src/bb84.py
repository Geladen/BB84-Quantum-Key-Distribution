from qiskit import QuantumCircuit, Aer
import numpy as np
import Crypto.Random.random

# Encode each bit according to the chosen base
def encode(qc, bit, base):

    if base == 'H':
        if bit == 1:
            qc.x(0)
    else:
        if bit == 1:
            qc.h(0)
            qc.x(0)
        else:
            qc.h(0)
    return qc

if __name__ == '__main__':

    # Alice generates random bits
    Alice_bits = Crypto.Random.random.getrandbits(1024)
    # Alice generates random bits in order to choose bases
    Alice_bases = Crypto.Random.random.getrandbits(1024)
    print(bin(Alice_bits))
    print(bin(Alice_bases))

    # Create a circuit
    qc = QuantumCircuit(1,1)
    qc.measure(0,0)

    # Simulate circuit
    aer_sim = Aer.get_backend('aer_simulator')
    job = aer_sim.run(qc)
    print(job.result().get_counts())
