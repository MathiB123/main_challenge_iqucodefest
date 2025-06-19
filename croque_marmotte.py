from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from typing import Tuple
import numpy as np


class CroqueLaitue:
    def __init__(self,
                 num_players: int,
                 num_dalles: int,
                 ) -> None:
        self.num_players = num_players
        self.num_dalles = num_dalles
        self._num_marmotte = 2 * num_players
        self._num_qubits = self.num_dalles + self._num_marmotte
        self._marmottes = [{"num_marmottes": 2, "position": 0} for _ in range(num_players)]
        self.tour_courant = 0
        self.partie_terminee = False
        self.current_player = 0

        # case de depart

    def play_game(self):
        pass

    def jouer_round(self):
        joueur = 0
        while joueur < self.num_players - 1:
            self._current_player = joueur
            if self._marmottes[joueur]["num_marmottes"] == 0:
                joueur += 1
            if joueur > self.num_players - 1:
                self.partie_terminee = True
                print("Partie terminée, vous avez tous perdus!")

            self.faire_action()


    # Pour chaque joueur
    def faire_action(self):
        action = input(
            f"Quelle action veux-tu faire, joueur {self._current_player}? (Pour s'intriquer : 1, pour avancer : 2, pour tenter le terrier : 3)")
        if action == 1:
            marmotte = input("Avec quelle marmotte veux-tu t'intriquer?")
            self.intriquer(marmotte)
        elif action == 2:
            self.avancer
        elif action == 3:
            greedyness = input("De combien de case aimerais-tu avancer?")
            self.terrier(greedyness)
        else:
            print("Vous n'avez pas entrez une option possible, veuillez recommencer!")
            self.faire_action()

    def intriquer(self, entangled_player) -> QuantumCircuit:
        marmottes_reg = QuantumRegister(self.num_players)
        dalles_reg = QuantumRegister(self.num_dalles)
        qcircuit = QuantumCircuit(marmottes_reg, dalles_reg)

        # the current player stays at the same place
        info_current_player = self._marmottes[self.current_player]
        qcircuit.cx(dalles_reg[info_current_player["position"]], marmottes_reg[self.current_player])

        # entangling the two marmottes
        qcircuit.cx(marmottes_reg[self.current_player], marmottes_reg[entangled_player])
        print(qcircuit)
        return qcircuit

    def avancer(self):
        pass

    # Effet tunnel
    def terrier(self, greedyness):
        pass

    def _build_circuit(self) -> None:
        self._quantum_circuit

    def _update_marmotte(self) -> None:
        self._position_lapin = {}

    def _initialize_circuit(self) -> QuantumCircuit:
        marmottes_reg = QuantumRegister(self.num_players)
        dalles_reg = QuantumRegister(self.num_dalles)
        qcircuit = QuantumCircuit(marmottes_reg, dalles_reg)

        for i in range(len(dalles_reg)):
            angle = np.random.uniform(0, 2 * np.pi)
            qcircuit.ry(angle, dalles_reg[i])

        self._quantum_circuit = qcircuit

        return qcircuit
