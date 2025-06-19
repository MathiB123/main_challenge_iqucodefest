from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from typing import Tuple
import numpy as np


class CroqueMarmotte:
    def __init__(self,
                 num_players: int,
                 num_dalles: int,
                 intrication_map: list[Tuple],
                 ) -> None:
        self.num_players = num_players
        self.num_dalles = num_dalles
        self._num_lapin = 2 * num_players
        self._num_qubits = self.num_dalles + self._num_lapin
        self._intrication_map = []

        self.tour_courant = 0
        self.partie_terminee = False

        for tup in intrication_map:
            if tup[1] and tup[0] in np.arange(0, self._num_lapin + 1):
                self._intrication_map.append(tup)

        # case de depart
        self._position_lapin = {f"{i}": 0 for i in range(self._num_lapin)}

    def play_game(self):
        while not self.partie_terminee:
            self.jouer_tour()

    def jouer_tour(self, action: str):
        return 0

    def _build_circuit(self, action: str) -> None:
        self._quantum_circuit

    def _update_vies_lapin(self) -> None:
        self._position_lapin = {}
