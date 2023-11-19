from qiskit import QuantumCircuit, Aer, execute
import numpy as np
import Crypto.Random.random
from qiskit.providers.aer import QasmSimulator

SIZE = 1024

# Encode each bit according to the chosen base
def encode(bits, bases):

    encoded_bits = []

    for i in range(SIZE):
        qc = QuantumCircuit(1,1)
        if bases[i] == 0:
            if bits[i] == 0:
                pass 
            else:
                qc.x(0)
        else:
            if bits[i] == 0:
                qc.h(0)
            else:
                qc.x(0)
                qc.h(0)

        encoded_bits.append(qc)

    return encoded_bits

# Measure al qubits with the beses given by Bob
def measure_bits(bits, bases):
    measured_bits = []
    backend = Aer.get_backend('aer_simulator')

    for i in range(SIZE):
        if bases[i] == 0: 
            bits[i].measure(0,0)
        if bases[i] == 1: 
            bits[i].h(0)
            bits[i].measure(0,0)
        
        result = backend.run(bits[i], shots=1, memory=True).result()
        measured_bit = int(result.get_memory()[0])
        measured_bits.append(measured_bit)
    
    return measured_bits


if __name__ == '__main__':

    # Alice generates random bits
    Alice_bits = [int(d) for d in bin(Crypto.Random.random.getrandbits(SIZE))[2:].rjust(SIZE, '0')] 

    # Alice generates random bits in order to choose bases
    Alice_bases = [int(d) for d in bin(Crypto.Random.random.getrandbits(SIZE))[2:].rjust(SIZE, '0')] 

    # Alice applies her bases
    qc_list = encode(Alice_bits, Alice_bases)

    # Bob generates random bits in order to choose bases
    Bob_bases = [int(d) for d in bin(Crypto.Random.random.getrandbits(SIZE))[2:].rjust(SIZE, '0')] 

    # Bob measures all the bits
    measured_bits = measure_bits(qc_list, Bob_bases)

    print(measured_bits)