from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np
import sys
import time


class CroqueLaitue:
    def __init__(self,
                 num_players: int,
                 num_dalles: int,
                 ) -> None:
        self.num_players = num_players
        self.num_dalles = num_dalles
        self._marmottes = [{"num_marmottes": 2, "position": 0} for _ in range(num_players)]
        self.tour_courant = 1
        self.partie_terminee = False
        self._current_player = 0
        self._registre_marmotte = QuantumRegister(self.num_players)
        self._registre_dalles = QuantumRegister(self.num_dalles)

    def play_game(self):
        print("Début de la partie! \n")

        while not self.partie_terminee:
            print(f"Tour : {self.tour_courant}")

            time.sleep(0.5)
            self.jouer_round()
            self._read_measure()

            for i, marmotte in enumerate(self._marmottes):
                if marmotte["position"] == self.num_dalles-1:
                    self.partie_terminee = True
                    print(f"Partie terminée! Le joueur {i} a gagné!")
            self.tour_courant += 1

    def jouer_round(self):
        joueur = 0
        classical_reg = ClassicalRegister(self.num_players)
        qc_total = QuantumCircuit(self._registre_marmotte, self._registre_dalles, classical_reg)
        qc_intriq, qc_avancer, qc_terrier = QuantumCircuit(self._registre_marmotte, self._registre_dalles), QuantumCircuit(self._registre_marmotte, self._registre_dalles), QuantumCircuit(self._registre_marmotte, self._registre_dalles)
        
        for joueur in range(self.num_players):
        # while joueur <= self.num_players - 1:
            self._current_player = joueur
            while self._marmottes[joueur]["num_marmottes"] < 1:
                joueur += 1
                if joueur > self.num_players - 1:
                    self.partie_terminee = True
                    sys.exit("Partie terminée, vous avez tous perdus!")
            action = None
            while action not in ["1", "2", "3", "q"]:
                time.sleep(0.5)
                action = input(
                    f"Quelle action veux-tu faire, joueur {self._current_player}? (Pour s'intriquer : 1, pour avancer : 2, pour tenter le terrier : 3, pour decalisser : q)")
                if action == "1":
                    joueur_vlimeux = int(input("Avec quel joueur veux-tu t'intriquer?"))
                    if self._current_player == joueur_vlimeux:
                        print(f"Joueur {self._current_player}, on ne peut pas s'intriquer avec soi-même!")
                        action = None
                    else:
                        qc = self.intriquer(joueur_vlimeux)
                        qc_intriq.compose(qc, inplace=True)
                        print(f"Joueur {self._current_player} s'intrique avec joueur {joueur_vlimeux}")
                elif action == "2":
                    qc = self.avancer()
                    qc_avancer.compose(qc, inplace=True)
                    print(f"Joueur {self._current_player} avance d'une case")
                elif action == "3":
                    greedyness = int(input("De combien de case aimerais-tu avancer?"))
                    qc = self.terrier(greedyness)
                    qc_terrier.compose(qc, inplace=True)
                elif action == "q":
                    sys.exit("Vous avez quitté avec succès.")
                else:
                    print(f"Vous n'avez pas entré une option possible joueur {self._current_player}!")

            # joueur += 1

        qc_complet = self._initialize_circuit()
        qc_complet.compose(qc_avancer, inplace=True)
        qc_complet.compose(qc_terrier, inplace=True)
        qc_complet.compose(qc_intriq, inplace=True)
        qc_total.compose(qc_complet, inplace=True)
        qc_total.measure(range(self.num_players), range(self.num_players))
        self._quantum_circuit = qc_total

    def intriquer(self, entangled_player) -> QuantumCircuit:
        qcircuit = QuantumCircuit(self._registre_marmotte, self._registre_dalles)

        # the current player stays at the same place
        info_current_player = self._marmottes[self._current_player]
        qcircuit.cx(self._registre_dalles[info_current_player["position"]], self._registre_marmotte[self._current_player])

        # entangling the two marmottes
        qcircuit.cx(self._registre_marmotte[self._current_player], self._registre_marmotte[entangled_player])
        self._marmottes[self._current_player]["position"] = self._marmottes[entangled_player]["position"]

        return qcircuit

    def avancer(self) -> QuantumCircuit:
        qcircuit = QuantumCircuit(self._registre_marmotte,self._registre_dalles)

        info_current_player = self._marmottes[self._current_player]

        qcircuit.cx(self._registre_dalles[info_current_player["position"] + 1], self._registre_marmotte[self._current_player])

        self._marmottes[self._current_player]["position"] += 1

        return qcircuit

    # Effet tunnel
    def terrier(self, greedyness) -> QuantumCircuit:
        qcircuit = QuantumCircuit(self._registre_marmotte, self._registre_dalles)

        probability = 1 / (greedyness ** 2)
        random_num = np.random.uniform(0, 1)

        if random_num < probability:
            self._marmottes[self._current_player]["position"] += greedyness
            print(f"Terrier succeeded for player {self._current_player}")
        else:
            print(f"Terrier failed for player {self._current_player}")

        qcircuit.cx(self._registre_dalles[self._marmottes[self._current_player]["position"]],
                    self._registre_marmotte[self._current_player])

        return qcircuit

    def _initialize_circuit(self) -> QuantumCircuit:
        marmottes_reg = QuantumRegister(self.num_players)
        dalles_reg = QuantumRegister(self.num_dalles)
        classical_reg = ClassicalRegister(self.num_players)
        qcircuit = QuantumCircuit(marmottes_reg, dalles_reg, classical_reg)

        for i in range(len(dalles_reg)):
            angle = np.random.uniform(0, np.pi/4)
            qcircuit.ry(angle, dalles_reg[i])

        self._quantum_circuit = qcircuit

        return qcircuit

    def _read_measure(self) -> None:
        simulator = AerSimulator()
        transpiled_circuit = transpile(self._quantum_circuit, backend=simulator)
        result = simulator.run(transpiled_circuit, shots=1).result()
        counts = result.get_counts(transpiled_circuit)
        result = list(counts.keys())[0][::-1]
        for i in range(len(result)):
            if result[i] == "1":
                self._marmottes[i]["num_marmottes"] -= 1
                print(f"Oh no! Player {i}, one of your marmotte has been swallowed :(")
                self._marmottes[i]["position"] = 0
        print(self._marmottes,"\n")
