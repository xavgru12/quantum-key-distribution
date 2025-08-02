from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
import numpy as np

# Parameters
num_bits = 20

# peer_a generates random bits and bases
peer_a_bits   = np.random.randint(2, size=num_bits)
peer_a_bases  = np.random.randint(2, size=num_bits)  # 0: Z-basis, 1: X-basis

# peer_b chooses random bases
peer_b_bases  = np.random.randint(2, size=num_bits)

# Results storage
peer_b_results = []

simulator = AerSimulator()

for i in range(num_bits):
    # build a fresh 1-qubit, 1-bit circuit each round
    qc = QuantumCircuit(1, 1)

    # peer_a’s preparation
    if peer_a_bits[i] == 1:
        qc.x(0)
    if peer_a_bases[i] == 1:
        qc.h(0)

    # peer_b’s basis change
    if peer_b_bases[i] == 1:
        qc.h(0)

    # execute Simulation of qubit and measurement
    qc.measure(0, 0)
    qc_t = transpile(qc, simulator)
    job  = simulator.run(qc_t, shots=1, memory=True)
    result = job.result()
    measured_bit = int(result.get_memory()[0])

    peer_b_results.append(measured_bit)

# Key sifting (keep only those where bases matched)
raw_key_peer_a = []
raw_key_peer_b = []

for i in range(num_bits):
    if peer_a_bases[i] == peer_b_bases[i]:
        raw_key_peer_a.append(peer_a_bits[i])
        raw_key_peer_b.append(peer_b_results[i])

print("peer_a's raw key:", raw_key_peer_a)
print("peer_b's raw key:", raw_key_peer_b)

