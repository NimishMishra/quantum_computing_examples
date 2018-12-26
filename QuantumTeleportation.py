from projectq.ops import All, CNOT, H, Measure, X, Z
from projectq import MainEngine


def create_bell_pair(quantum_engine):

    alice_qubit = quantum_engine.allocate_qubit()
    
    bob_qubit = quantum_engine.allocate_qubit()
    
    # The bell pair can be created by applying Hadamard on Alice's qubit and the CNOT
    H | alice_qubit

    CNOT | (alice_qubit, bob_qubit)

    # This shall create the Bell state we are looking for

    return alice_qubit, bob_qubit


def create_message(quantum_engine='', qubit_one='', qubit_to_send = ''):
    # Qubit one is Alice's half of the EPR she had created earlier with Bob
    
    # Alice does the following interactions

    CNOT | (qubit_to_send, qubit_one)
    H | qubit_to_send

    Measure | qubit_to_send
    Measure | qubit_one

    # This message is then sent to Bob
    classical_message = [int(qubit_to_send), int(qubit_one)]

    return classical_message



def message_reciever(quantum_engine, message, qubit_two):
    # message has two values:
    # message [0] stores the measurement of the superposition of the qubit_to_send
    # message [1] stores the measurement of the Alice's part of the EPR created earlier

    if message[0] == 1:
        Z | qubit_two
    if message[1] == 1:
        X | qubit_two

    Measure | qubit_two

    quantum_engine.flush()

    final_bit = int(qubit_two) # Same as message to send
    return final_bit




# Using the simulator as quantum engine
# Sending bit 0
engine=MainEngine()
to_send_qubit = engine.allocate_qubit()
sent_message = Measure | to_send_qubit
alice_qubit, bob_qubit = create_bell_pair(engine)
message = create_message(quantum_engine=engine, qubit_one=alice_qubit, qubit_to_send= to_send_qubit)
final = message_reciever(engine, message, bob_qubit)

print('Message sent is {}'.format('0'))
print('Message received is {}'.format(final))

# Now sending bit 1
to_send_qubit = engine.allocate_qubit()
X | to_send_qubit
alice_qubit, bob_qubit = create_bell_pair(engine)
message = create_message(quantum_engine=engine, qubit_one=alice_qubit, qubit_to_send= to_send_qubit)
final = message_reciever(engine, message, bob_qubit)

print('Message sent is {}'.format('1'))
print('Message received is {}'.format(final))