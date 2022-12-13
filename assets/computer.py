import qiskit


class Computer:
    def __init__(self):
        pass

    def update(self):
        pass


class ClassicalComputer(Computer):
    def __init__(self, paddle):
        self.paddle = paddle
        self.score = 0
        self.speed = 3

    # moves classical paddle up/down towards ball
    def update(self, ball):
        if self.paddle.rect.centery - ball.rect.centery > 0:
            self.paddle.rect.y -= self.speed
        else:
            self.paddle.rect.y += self.speed


class QuantumComputer(Computer):
    def __init__(self, quantum_paddles, circuit_grid):
        self.paddles = quantum_paddles.paddles
        self.score = 0
        self.circuit_grid = circuit_grid

    def update(self, ball):
        simulator = qiskit.BasicAer.get_backend("statevector_simulator")
        circuit = self.circuit_grid.model.compute_circuit()
        transpiled_circuit = qiskit.transpile(circuit, simulator)
        statevector = simulator.run(transpiled_circuit, shots=100).result(
        ).get_statevector()  # lower accuracy (shots) higher speed

        # changes opacity of paddle based on state vector probability
        # (fully opaque for 100% certainty to transparent for 0% certainty)
        for basis_state, amplitude in enumerate(statevector):
            self.paddles[basis_state].image.set_alpha(amplitude ** 2 * 255)