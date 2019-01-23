from qiskit.tools.visualization import plot_histogram
import Qconfig
import qiskit as qk
from qiskit.providers.ibmq import least_busy
qr = qk.QuantumRegister(4)  # Allocate two quantum registers - 4 qubits
cr = qk.ClassicalRegister(4)  # Allocate two classical registers - 4 bits
qc = qk.QuantumCircuit(qr, cr)  # Create a Quantum Circuit acting on qr and cr

# Now, we can make operations on those.
qc.h(qr[0])
qc.h(qr[1])
# control not-gate, this in a real QComputer will entangle both qubits.
qc.cx(qr[0], qr[2])
# control not-gate, this in a real QComputer will entangle both qubits.
qc.cx(qr[1], qr[3])

measure_Z = qk.QuantumCircuit(qr, cr)

measure_Z.h(qr[2])
measure_Z.h(qr[3])
# measure_Z.cx(qr[1],qr[3])
# measure_Z.cx(qr[2],qr[0])
measure_Z.measure(qr, cr)

measure_X = qk.QuantumCircuit(qr, cr)

measure_X.h(qr)
measure_X.measure(qr, cr)

test_Z = qc + measure_Z

test_X = qc + measure_X

backend = qk.BasicAer.get_backend('qasm_simulator')
job_1 = qk.execute(test_Z, backend, shots=1000)

result_1 = job_1.result()

print(result_1.get_counts(test_Z))

plot_histogram(result_1.get_counts(test_Z)).savefig("test_Z.png")

job_1 = qk.execute(test_X, backend, shots=1000)

result_1 = job_1.result()

print(result_1.get_counts(test_X))

plot_histogram(result_1.get_counts(test_X)).savefig("test_X.png")

qk.IBMQ.load_accounts(hub=None)

backend = least_busy(qk.IBMQ.backends(
    filters=lambda x: not x.configuration().simulator))

job_2 = qk.execute(test_Z, backend, shots=1000)

print(job_2.status)

result_2 = job_2.result()

print(result_2.get_counts(test_Z))

plot_histogram(result_2.get_counts(test_Z)).savefig("IBM_test_Z.png")

backend = least_busy(qk.IBMQ.backends(
    filters=lambda x: not x.configuration().simulator))

job_2 = qk.execute(test_X, backend, shots=1000)

result_2 = job_2.result()

print(result_2.get_counts(test_X))

plot_histogram(result_2.get_counts(test_X)).savefig("IBM_test_X.png")
