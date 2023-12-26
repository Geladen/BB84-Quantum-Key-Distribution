from qiskit import QuantumCircuit, Aer, execute
import random

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

        qc.barrier()
        encoded_bits.append(qc)

    return encoded_bits

# Measure all qubits with the bases given by Bob
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
    #Alice_bits = [int(d) for d in bin(Crypto.Random.random.getrandbits(100))[2:].rjust(SIZE, '0')] 
    Alice_bits = [int(d) for d in bin(random.getrandbits(SIZE))[2:].rjust(SIZE, '0')]

    # Alice generates random bits in order to choose bases
    Alice_bases = [int(d) for d in bin(random.getrandbits(SIZE))[2:].rjust(SIZE, '0')] 

    # Alice applies her bases
    qc_list = encode(Alice_bits, Alice_bases)

    # Bob generates random bits in order to choose bases
    Bob_bases = [int(d) for d in bin(random.getrandbits(SIZE))[2:].rjust(SIZE, '0')] 

    # Bob measures all the bits
    measured_bits = measure_bits(qc_list, Bob_bases)

    # Bob communicates his bases
    print("Bob bases:", Bob_bases)

    # Alice checks which bases are the same as bob's bases
    common_bases=[]
    for i in range(len(Bob_bases)):
        if Bob_bases[i] == Alice_bases[i]:
            common_bases.append(i)

    # Alice communicates right bases
    print("Common bases (indexes)",common_bases)

    # Alice updates her key
    Alice_temp_key = []
    for i in common_bases:
        Alice_temp_key.append(Alice_bits[i])

    # Bob updates his key
    Bob_temp_key = []
    for i in common_bases:
        Bob_temp_key.append(measured_bits[i])

    check_size = len(common_bases) * 0.1

    # Alice and Bob choose the bits to use to verify the correctness of the algorithm 
    security_bits = security_bits = random.sample(range(0, len(common_bases)), int(check_size))  

    print("Security bits: ")
    for i in security_bits:
        if Bob_temp_key[i] != Alice_temp_key[i]:
            print("\nSomeone manipulated the key exchange")
            exit()
        print(Alice_temp_key[i], end = "")

    # Alice discards the bits used for the correctness check
    Alice_key = []
    for i in range(len(Alice_temp_key)):
        if i not in security_bits:
            Alice_key.append(Alice_temp_key[i])

    # Bob discards the bits used for the correctness check
    Bob_key = []
    for i in range(len(Bob_temp_key)):
        if i not in security_bits:
            Bob_key.append(Bob_temp_key[i])

    print("\nFinal key: ", Bob_key)
    print("Key lenght: ", len(Bob_key))