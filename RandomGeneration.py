from projectq.ops import  H, Measure
from projectq import MainEngine

def get_random_number(quantum_engine):
    qubit = quantum_engine.allocate_qubit()
    H | qubit
    Measure | qubit
    random_number = int(qubit)
    return random_number


print('Random number generated ', get_random_number(MainEngine()))