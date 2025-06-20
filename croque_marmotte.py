from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np


class CroqueLaitue:
    def __init__(self,
                 num_players: int,
                 num_dalles: int,
                 ) -> None:
        self.num_players = num_players
        self.num_dalles = num_dalles
        self._marmottes = [{"num_marmottes": 2, "position": 0} for _ in range(num_players)]
        self.tour_courant = 0
        self.partie_terminee = False
        self._current_player = 0

        # case de depart

    def play_game(self):
        print("Début de la partie! \n")

        while not self.partie_terminee:
            print("Tour : 1 \n")

            self.jouer_round()
            self._read_measure()
            for i, marmotte in enumerate(self._marmottes):
                if marmotte["position"] == self.num_dalles:
                    self.partie_terminee = True
                    print("Partie terminée! Le joueur {i} a gagné!")
                    self.tour_courant += 1

    def jouer_round(self):
        joueur = 0
        classical_reg = ClassicalRegister(self.num_players)
        quantum_reg = QuantumRegister(self.num_players + self.num_dalles)
        qc_total = QuantumCircuit(quantum_reg, classical_reg)
        qc_intriq, qc_avancer, qc_terrier = QuantumCircuit(self.num_players), QuantumCircuit(
            self.num_players + self.num_dalles), QuantumCircuit(self.num_players + self.num_dalles)
        while joueur < self.num_players - 1:
            self._current_player = joueur
            while self._marmottes[joueur]["num_marmottes"] < 1:
                joueur += 1
            if joueur > self.num_players - 1:
                self.partie_terminee = True
                print("Partie terminée, vous avez tous perdus!")
                exit()
            else:
                action = input(
                    f"Quelle action veux-tu faire, joueur {self._current_player}? (Pour s'intriquer : 1, pour avancer : 2, pour tenter le terrier : 3)")
                if action == 1:
                    joueur = input("Avec quel joueur veux-tu t'intriquer?")
                    qc = self.intriquer(int(joueur))
                    qc_intriq.append(qc)
                elif action == 2:
                    qc = self.avancer
                    qc_avancer.append(qc)
                elif action == 3:
                    greedyness = input("De combien de case aimerais-tu avancer?")
                    qc = self.terrier(int(greedyness))
                    qc_terrier.append(qc)
                else:
                    print("Vous n'avez pas entré une option possible!")
                joueur += 1

        qc_complet = self._initialize_circuit()
        qc_complet.append(qc_avancer)
        qc_complet.append(qc_terrier)
        qc_complet.append(qc_intriq, range(self.num_players))
        qc_total.append(qc_complet)
        qc_total.measure(range(self.num_players), range(self.num_players))
        qc_total.draw("mpl")
        self._quantum_circuit = qc_total

    def intriquer(self, entangled_player) -> QuantumCircuit:
        marmottes_reg = QuantumRegister(self.num_players)
        dalles_reg = QuantumRegister(self.num_dalles)
        qcircuit = QuantumCircuit(marmottes_reg, dalles_reg)

        # the current player stays at the same place
        info_current_player = self._marmottes[self._current_player]
        qcircuit.cx(dalles_reg[info_current_player["position"]] - 1, marmottes_reg[self._current_player])

        # entangling the two marmottes
        qcircuit.cx(marmottes_reg[self._current_player], marmottes_reg[entangled_player])
        self._marmottes[self._current_player]["position"] = self._marmottes[entangled_player]["position"]
        print(qcircuit)
        return qcircuit

    def avancer(self):
        marmottes_reg = QuantumRegister(self.num_players)
        dalles_reg = QuantumRegister(self.num_dalles)
        qcircuit = QuantumCircuit(marmottes_reg, dalles_reg)

        info_current_player = self._marmottes[self._current_player]
        qcircuit.cx(dalles_reg[info_current_player["position"] + 1], marmottes_reg[self._current_player])

        self._marmottes[self._current_player]["positions"] += 1

        return qcircuit

    # Effet tunnel
    def terrier(self, greedyness) -> QuantumCircuit:
        marmottes_reg = QuantumRegister(self.num_players)
        dalles_reg = QuantumRegister(self.num_dalles)
        qcircuit = QuantumCircuit(marmottes_reg, dalles_reg)

        probability = 1 / (greedyness ^ 2)
        random_num = np.random.uniform(0, 1)

        if random_num < probability:
            self._marmottes[self._current_player]["position"] += greedyness

        qcircuit.cx(dalles_reg[self._marmottes[self._current_player]["position"]] - 1,
                    marmottes_reg[self._current_player])

        return qcircuit

    def _initialize_circuit(self) -> QuantumCircuit:
        marmottes_reg = QuantumRegister(self.num_players)
        dalles_reg = QuantumRegister(self.num_dalles)
        classical_reg = ClassicalRegister(self.num_players)
        qcircuit = QuantumCircuit(marmottes_reg, dalles_reg, classical_reg)

        for i in range(len(dalles_reg)):
            angle = np.random.uniform(0, 2 * np.pi)
            qcircuit.ry(angle, dalles_reg[i])

        self._quantum_circuit = qcircuit

        return qcircuit

    def _read_measure(self):
        simulator = AerSimulator()
        transpiled_circuit = transpile(self._quantum_circuit, backend=simulator)
        result = simulator.run(transpiled_circuit, shots=1).result()
        counts = result.get_counts(transpiled_circuit)
        result = list(counts.keys())[0][::-1]
        for i in range(len(result)):
            if result[i] == "1":
                self._marmottes[i]["num_marmottes"] -= 1
                print("Oh no! One of your marmotte has been swallowed :(")
                self._marmottes[i]["position"] = 0

        return None
