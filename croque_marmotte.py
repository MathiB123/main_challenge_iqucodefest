from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from typing import Tuple
import numpy as np


class CroqueLaitue:
    def __init__(self,
                 num_players: int,
                 num_dalles: int,
                 intrication_map: list[Tuple],
                 ) -> None:
        self.num_players = num_players
        self.num_dalles = num_dalles
        self._num_marmotte = 2 * num_players
        self._num_qubits = self.num_dalles + self._num_lapin
        self._intrication_map = []

        self.tour_courant = 0
        self.partie_terminee = False

        for tup in intrication_map:
            if tup[1] and tup[0] in np.arange(0, self._num_lapin + 1):
                self._intrication_map.append(tup)

        # case de depart
        self._position_marmotte = {f"{i}": 0 for i in range(self._num_lapin)}

    def play_game(self):
        pass

    def jouer_round(self):
        pass

    #Pour chaque joueur
    def faire_action():
        pass

    def intriquer(lapin):
        pass

    def avancer():
        pass

    #Effet tunnel
    def terrier(greedyness):
        pass

    def _build_circuit(self, action: str) -> None:
        self._quantum_circuit

    def _update_marmotte(self) -> None:
        self._position_lapin = {}
