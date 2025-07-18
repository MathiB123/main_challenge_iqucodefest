from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister, transpile
from qiskit_aer import AerSimulator
import numpy as np
import sys
import time

from renderer import Renderer


class CroqueLaitue:
    """
    A quantum-enhanced game where players, represented as groundhogs (marmottes),
    move across a board made of tiles (dalles). Players take actions using quantum operations:
    entangling with others, moving forward, or attempting risky tunnel jumps.

    The game ends when a player reaches the last tile, or all players lose.

    Attributes:
        num_players (int): Number of players in the game.
        num_dalles (int): Number of tiles on the board.
        _marmottes (list of dict): Each player's state including groundhog count and position.
        tour_courant (int): Current turn number (starts at 1).
        partie_terminee (bool): Flag indicating if the game is finished.
        _current_player (int): Index of the player currently taking a turn.
        _registre_marmotte (QuantumRegister): Quantum register for the players.
        _registre_dalles (QuantumRegister): Quantum register representing the tiles.
        renderer (Renderer): Visual renderer to display the game state.
    """

    def __init__(
        self,
        num_players: int,
        num_dalles: int,
    ) -> None:
        """
        Initializes the game state with the given number of players and tiles.

        Args:
            num_players (int): Number of players in the game.
            num_dalles (int): Number of tiles on the board.
        """

        self.num_players = num_players
        self.num_dalles = num_dalles
        self._marmottes = [
            {"num_marmottes": 2, "position": 0} for _ in range(num_players)
        ]
        self.tour_courant = 1
        self.partie_terminee = False
        self._current_player = 0
        self._registre_marmotte = QuantumRegister(self.num_players)
        self._registre_dalles = QuantumRegister(self.num_dalles)
        self.renderer = Renderer(num_dalles)

        # case de depart

    def play_game(self) -> None:
        """
        Runs the main game loop until a player wins or all players are eliminated.
        Handles rendering, player actions, and updates to the game state.
        """
        self.renderer.add_text("Start!")

        for i in range(len(self._marmottes)):
            self.renderer.draw_groundhog(0, i)

        while not self.partie_terminee:
            self.move_results = []
            self.renderer.add_text(f"Round : {self.tour_courant}")
            self.renderer.render()

            self.jouer_round()
            time.sleep(0.3)  # Gives a bit of time to see what is going on
            self.renderer.clear_text()
            self._read_measure()

            for res in self.move_results:
                self.renderer.add_text(res)

            self.renderer.clear_map()
            for i, marmotte in enumerate(self._marmottes):
                self.renderer.draw_groundhog(marmotte["position"], i)
                if marmotte["position"] == self.num_dalles - 1:
                    self.partie_terminee = True
                    self.renderer.add_text(f"Game Over! Player {i} has won!")

            self.tour_courant += 1

        self.renderer.render()
        time.sleep(2)  # DO NOT REMOVE THE NOTEBOOK CAN'T DISPLAY VICTORY

    def jouer_round(self):
        """
        Executes a single round where each player chooses one of the possible actions:
        1. Entangle with another player (quantum friendship),
        2. Move forward one tile,
        3. Attempt to dig a tunnel forward a chosen distance.

        The player's action is translated into a quantum circuit which is then executed
        at the end of the round.
        """
        joueur = 0
        classical_reg = ClassicalRegister(self.num_players)
        qc_total = QuantumCircuit(
            self._registre_marmotte, self._registre_dalles, classical_reg
        )
        qc_intriq, qc_avancer, qc_terrier = (
            QuantumCircuit(self._registre_marmotte, self._registre_dalles),
            QuantumCircuit(self._registre_marmotte, self._registre_dalles),
            QuantumCircuit(self._registre_marmotte, self._registre_dalles),
        )

        while joueur <= self.num_players - 1:
            self._current_player = joueur
            while self._marmottes[joueur]["num_marmottes"] < 1:
                joueur += 1
                if joueur > self.num_players - 1:
                    self.partie_terminee = True
                    sys.exit("Game over, everyone lost!")
            action = None
            while action not in ["1", "2", "3", "q"]:
                self.renderer.clear_tempo_text()
                self.renderer.add_tempo_text(
                    f"Player {self._current_player}, what will you do ?\n1 : Make a friend;\n2 : Frolic in the garden;\n3 : Dig a tunnel;\nQ : Exit the game"
                )
                self.renderer.render()
                action = input()
                if action == "1":
                    self.renderer.clear_tempo_text()
                    self.renderer.add_tempo_text("Who's your new friend ?")
                    self.renderer.render()
                    inputed = input()
                    joueur_vlimeux = -1
                    try:
                        joueur_vlimeux = int(inputed)
                    except BaseException:
                        joueur_vlimeux = -1
                    if joueur_vlimeux < 0 :
                        self.renderer.add_tempo_text(
                            f"Player {self._current_player}, you need to input a valid number!!!\nPress ENTER to make a valide choice !"
                        )
                        self.renderer.render()
                        input()
                        action = None
                    elif self._current_player == joueur_vlimeux:
                        self.renderer.clear_tempo_text()
                        self.renderer.add_tempo_text(
                            f"Player {self._current_player}, you can't be friend with yourself !!!\nPress ENTER to make a valide choice !"
                        )
                        self.renderer.render()
                        input()
                        action = None
                    else:
                        qc = self.intriquer(joueur_vlimeux)
                        qc_intriq.compose(qc, inplace=True)
                        self.renderer.add_text(
                            f"Player {self._current_player} wants to be friend with player {joueur_vlimeux}"
                        )
                        self.renderer.render()
                elif action == "2":
                    qc = self.avancer()
                    qc_avancer.compose(qc, inplace=True)
                    self.renderer.add_text(
                        f"Player {self._current_player} will move one square over"
                    )
                    self.renderer.render()
                elif action == "3":
                    self.renderer.clear_tempo_text()
                    self.renderer.add_tempo_text(
                        "How far do you want to dig your tunnel ?"
                    )
                    self.renderer.render()
                    inputed = input()
                    greedyness = -1
                    try:
                        greedyness = int(inputed)
                    except BaseException:
                        greedyness = -1
                    if greedyness < 1:
                        self.renderer.clear_tempo_text()
                        self.renderer.add_tempo_text(
                            f"Player {self._current_player}, you need to go farther than 0 squares !!!\nPress ENTER to make a valide choice"
                        )
                        self.renderer.render()
                        input()
                        action = None
                    elif greedyness > self.num_dalles - 1:
                        self.renderer.clear_tempo_text()
                        self.renderer.add_tempo_text(
                            f"Player {self._current_player}, you need to go less than {self.num_dalles} squares !!!\nPress ENTER to make a valide choice"
                        )
                        self.renderer.render()
                        action = None
                        input()
                    else:
                        qc = self.terrier(greedyness)
                        qc_terrier.compose(qc, inplace=True)
                        self.renderer.add_text(
                            f"Player {self._current_player} will try to dig a tunnel"
                        )
                elif action == "q":
                    sys.exit("You successfully left the game.")
                else:
                    self.renderer.clear_tempo_text()
                    self.renderer.add_tempo_text(
                        f"Player {self._current_player} you didn't enter a valide option !!!\nPress ENTER to make a valide choice !"
                    )
                    self.renderer.render()
                    input()

            joueur += 1
        self.renderer.clear_tempo_text()
        self.renderer.render()

        qc_complet = self._initialize_circuit()
        qc_complet.compose(qc_avancer, inplace=True)
        qc_complet.compose(qc_terrier, inplace=True)
        qc_complet.compose(qc_intriq, inplace=True)
        qc_total.compose(qc_complet, inplace=True)
        qc_total.measure(range(self.num_players), range(self.num_players))
        self._quantum_circuit = qc_total

    def intriquer(self, entangled_player) -> QuantumCircuit:
        """
        Attempts to entangle the current player with another player.

        Args:
            entangled_player (int): The player to entangle with.

        Returns:
            QuantumCircuit: A circuit applying the entanglement operation.
        """
        qcircuit = QuantumCircuit(self._registre_marmotte, self._registre_dalles)

        # the current player stays at the same place
        info_current_player = self._marmottes[self._current_player]
        qcircuit.cx(
            self._registre_dalles[info_current_player["position"]],
            self._registre_marmotte[self._current_player],
        )

        # entangling the two groundhogs
        qcircuit.cx(
            self._registre_marmotte[self._current_player],
            self._registre_marmotte[entangled_player],
        )

        random_num = np.random.uniform(0, 1)
        if random_num < 0.25:
            self._marmottes[self._current_player]["position"] = self._marmottes[
                entangled_player
            ]["position"]
            self.move_results.append(
                f"Player {self._current_player} made friend with player {entangled_player}"
            )
        else:
            self.move_results.append(
                f"Player {self._current_player} didn't make friend with player {entangled_player}"
            )
        return qcircuit

    def avancer(self) -> QuantumCircuit:
        """
        Moves the current player forward by one tile.

        Returns:
            QuantumCircuit: A circuit that encodes the move operation.
        """
        qcircuit = QuantumCircuit(self._registre_marmotte, self._registre_dalles)

        info_current_player = self._marmottes[self._current_player]

        qcircuit.cx(
            self._registre_dalles[info_current_player["position"] + 1],
            self._registre_marmotte[self._current_player],
        )

        self._marmottes[self._current_player]["position"] += 1

        return qcircuit

    # Effet tunnel
    def terrier(self, greedyness) -> QuantumCircuit:
        """
        Attempts to tunnel forward a given number of tiles.

        Success probability decreases with distance.

        Args:
            greedyness (int): Number of tiles the player wants to jump.

        Returns:
            QuantumCircuit: A circuit encoding the tunneling operation.
        """
        qcircuit = QuantumCircuit(self._registre_marmotte, self._registre_dalles)

        probability = 1 / (greedyness**2)
        random_num = np.random.uniform(0, 1)

        if random_num < probability:
            self._marmottes[self._current_player]["position"] += greedyness
            self.move_results.append(
                f"Player {self._current_player}'s tunnel succeeded"
            )
        else:
            self.move_results.append(f"Player {self._current_player}'s tunnel failed")

        qcircuit.cx(
            self._registre_dalles[self._marmottes[self._current_player]["position"]],
            self._registre_marmotte[self._current_player],
        )

        return qcircuit

    def _initialize_circuit(self) -> QuantumCircuit:
        """
        Initializes the quantum circuit with randomized tile states.

        Returns:
            QuantumCircuit: The initialized quantum circuit.
        """
        marmottes_reg = QuantumRegister(self.num_players)
        dalles_reg = QuantumRegister(self.num_dalles)
        classical_reg = ClassicalRegister(self.num_players)
        qcircuit = QuantumCircuit(marmottes_reg, dalles_reg, classical_reg)

        for i in range(1, len(dalles_reg)):
            angle = np.random.uniform(0, np.pi / 4)
            qcircuit.ry(angle, dalles_reg[i])

        self._quantum_circuit = qcircuit

        return qcircuit

    def _read_measure(self) -> None:
        """
        Runs the quantum circuit on a simulator and reads the measurement results.
        Updates each player's state based on the measurement outcome.
        """
        simulator = AerSimulator()
        transpiled_circuit = transpile(self._quantum_circuit, backend=simulator)
        result = simulator.run(transpiled_circuit, shots=1).result()
        counts = result.get_counts(transpiled_circuit)
        result = list(counts.keys())[0][::-1]
        for i in range(len(result)):
            if result[i] == "1":
                self._marmottes[i]["num_marmottes"] -= 1
                self.move_results.append(
                    f"Oh no! Player {i}, one of your groundhog has been trapped :("
                )
                self._marmottes[i]["position"] = 0
