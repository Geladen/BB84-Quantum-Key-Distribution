import numpy as np
from qiskit import QuantumCircuit, Aer, transpile, assemble

def create_entangled_pairs(num_pairs):
    entangled_pairs = []
    for _ in range(num_pairs):
        circuit = QuantumCircuit(2, 2)  # Aggiungi 2 qubit e 2 bit classici
        circuit.h(0)
        circuit.cx(0, 1)
        entangled_pairs.append(circuit)
    return entangled_pairs

def measure_in_random_bases(circuit):
    basis1 = np.random.choice(['Z', 'X'])
    basis2 = np.random.choice(['Z', 'X'])

    circuit.barrier()  # Aggiungi una barriera per separare i passaggi dei qubit
    if basis1 == 'Z':
        circuit.measure(0, 0)
    elif basis1 == 'X':
        circuit.h(0)
        circuit.measure(0, 0)
    
    if basis2 == 'Z':
        circuit.measure(1, 1)
    elif basis2 == 'X':
        circuit.h(1)
        circuit.measure(1, 1)

    backend = Aer.get_backend('aer_simulator')
    compiled_circuit = transpile(circuit, backend)
    result = backend.run(compiled_circuit, shots=1).result()

    counts = result.get_counts()

    return counts, basis1==basis2

def main(num_pairs):
    entangled_pairs = create_entangled_pairs(num_pairs)
    key_bits = []

    for pair in entangled_pairs:
        counts, same_base = measure_in_random_bases(pair)
        if same_base:
            #print(counts)
            key_bits.append(0 if '00' in counts else 1)

    return key_bits

if __name__ == "__main__":
    num_pairs =1024  # Puoi scegliere quante coppie di particelle entangled verificare.
    key_bits = main(num_pairs)
    
    print("Chiave quantistica generata:")
    print(key_bits)
    print(len(key_bits))

