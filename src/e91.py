import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble

# Generation of a num_pairs entangled qubits in Bell states
def create_entangled_pairs(num_pairs):
    entangled_pairs = []
    for _ in range(num_pairs):
        circuit = QuantumCircuit(2, 2)  # generates 2 qubits and 2 classic bits
        circuit.h(0)
        circuit.cx(0, 1)
        entangled_pairs.append(circuit)
    return entangled_pairs

# Measurement of one pair of entangled qubits using randon bases
def measure_in_random_bases(pair):
    basisAlice = np.random.choice(['Z', 'X'])
    basisBob = np.random.choice(['Z', 'X'])

    pair.barrier()  
    if basisAlice == 'Z':
        pair.measure(0, 0)
    elif basisAlice == 'X':
        pair.h(0)
        pair.measure(0, 0)
    
    if basisBob == 'Z':
        pair.measure(1, 1)
    elif basisBob == 'X':
        pair.h(1)
        pair.measure(1, 1)

    backend = Aer.get_backend('aer_simulator')
    compiled_circuit = transpile(pair, backend)
    result = backend.run(compiled_circuit, shots=1).result()

    counts = result.get_counts()

    return counts, basisAlice == basisBob

def main(num_pairs):
    # Creation of the pairs
    entangled_pairs = create_entangled_pairs(num_pairs)
    key_bits = []

    # For every pair calls the measure function
    for pair in entangled_pairs:
        counts, same_base = measure_in_random_bases(pair)
        if same_base: # If the the bases are the same use the bit for the key
            key_bits.append(0 if '00' in counts else 1)

    return key_bits

if __name__ == "__main__":
    num_pairs = 1024 # Key length
    key_bits = main(num_pairs)
    
    print("\nFinal key: ", key_bits)
    print("Key lenght: ", len(key_bits))

