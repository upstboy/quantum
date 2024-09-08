# This program is a test of the Grover's algorithm using Qiskit.
# Grover's algorithm is a quantum algorithm for searching an unsorted database.
# It is a search algorithm that uses the principles of quantum computing to search for a specific item in an unsorted database.
# It is a quantum analogue of classical binary search.
# Compared to classical search algorithms, Grover's algorithm has a quadratic speedup over classical algorithms.
# For example, a classical algorithm may take O(N) time to search an unsorted database of size N, 
# while a Grover-optimized quantum algorithm may take only O(sqrt(N)) time.

import qiskit
from qiskit_aer.primitives import SamplerV2

def oracle(circuit, n):
    # Oracle marks the solution state (in this case, state |111>)
    circuit.ccx(0, 1, 2)  # CCX (Toffoli) gate
    circuit.z(2)
    circuit.ccx(0, 1, 2)

def diffuser(circuit, n):
    # Diffuser for amplitude amplification
    circuit.h(range(n))
    circuit.x(range(n))
    circuit.ccx(0, 1, 2)
    circuit.x(range(n))
    circuit.h(range(n))

def grover(n, iterations):
    circuit = qiskit.QuantumCircuit(n)
    
    # Initialize in superposition
    circuit.h(range(n))
    
    # Apply Grover iteration
    for _ in range(iterations):
        oracle(circuit, n)
        diffuser(circuit, n)
    
    # Measure all qubits
    circuit.measure_all()
    
    return circuit

# Set up the problem
n = 3  # number of qubits
iterations = 1  # optimal number of iterations for 3 qubits

# Create the circuit
circuit = grover(n, iterations)

# Construct an ideal simulator with SamplerV2
sampler = SamplerV2()
job = sampler.run([circuit], shots=1000)

# Perform an ideal simulation
result_ideal = job.result()
counts_ideal = result_ideal[0].data.meas.get_counts()
print('Counts(ideal):', counts_ideal)

# Calculate the success probability
success_prob = counts_ideal.get('111', 0) / 1000
print(f'Success probability: {success_prob:.2f}')