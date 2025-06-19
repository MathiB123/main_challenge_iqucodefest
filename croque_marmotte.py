from qiskit import QuantumCircuit, QuantumRegister


class CroqueMarmotte:
    def __init__(self,
                 num_players,
                 num_dalles,
                 intrication_map,
                 ):
        self._num_players = num_players
        self._num_dalles = num_dalles
        self._num_lapin = 2 * num_players
        self._num_qubits = self._num_dalles + self._num_lapin

        # case de depart
        self._position_lapin = {f"{i}": 0 for i in range(self._num_lapin)}

