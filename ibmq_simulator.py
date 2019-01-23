from qiskit.tools.visualization import plot_histogram
import Qconfig
import qiskit as qk
from qiskit.providers.ibmq import least_busy
qr = qk.QuantumRegister(4)  	# Allocate four quantum registers - 4 qubits
cr = qk.ClassicalRegister(4)  	# Allocate four classical registers - 4 bits
qc = qk.QuantumCircuit(qr, cr)  # Create a Quantum Circuit acting on qr and cr
# The values of qr will be stored in cr, this is
# the local memory. WE ARE NOT DEFINING THE AMOUNT
# OF REGISTERS.

# Now, we can make operations on those.
qc.h(qr[0])						# This operation will transfor the |0〉 into |+〉 and
# |1〉 into |-〉 so this allows entanglement using the
# control-not gate provided by the toolkit.
# It's recommendable that you use this operation at
# the beggining of the algorithm and at the end to
# translate the results.
# qc.h(qr[1])
qc.cx(qr[0], qr[2])   			# Control not-gate, this in a real QComputer will
# entangle both qubits.
# qc.cx(qr[1], qr[3])   			# In this case qubit_2 and qubit_3 will be in the
# same state as qubit_0 and qubit_1, respectevely.

# Create another circuit using the same
measure_Z = qk.QuantumCircuit(qr, cr)
# amount of qubits and bits.

# In this operation we are not entangleling the qubits, but operating the
# ones that weren't operated in the previous circuit.
measure_Z.h(qr[1])
measure_Z.cx(qr[1], qr[3])
# We measure the circuit
measure_Z.measure(qr, cr)

# We add the two circuits to obtain a test result on how many possible
# combinations we have and the probabilities of each combination to be
# exist. These results are mearly theorethical and in a real quantum
# computer, the results may vary.
test_Z = qc + measure_Z

# We run the circuit in the local simulator. For more information on
# the simulators, please visit the Github or read the documentation.
# For more, visit https://qiskit.com
qk.IBMQ.load_accounts(hub=None)

# To run the application in the real quantum computer provided by IBM Q.
# Note: remember to get the APItoken from the page and include it in the
# Qconfig.py and include it as an string.
backend = least_busy(qk.IBMQ.backends(
    filters=lambda x: not x.configuration().simulator))
qjob_2 = qk.compile(test_Z, backend, shots=1024)
print(qjob_2)
job_2 = backend.run(qjob_2)

print(job_2.status())

result_1 = job_2.result()

print(result_1.get_counts(test_Z))

plot_histogram(result_1.get_counts(test_Z)).savefig("test_Z.png")

# =====================================================================
# Another example where we use the same starting quantum circuit qc

measure_X = qk.QuantumCircuit(qr, cr)

# Here, we are applying the Hadermard Gate to all
measure_X.h(qr)
# measure_X.cx(qr[1],qr[3])
# the qubits but we wont entangle them.
measure_X.measure(qr, cr)   # By doing so, the amount of different possible
# combinations are reduced.
test_X = qc + measure_X

job_1 = qk.execute(test_X, backend, shots=1000)

result_1 = job_1.result()

print(result_1.get_counts(test_X))

plot_histogram(result_1.get_counts(test_X)).savefig("test_X.png")
