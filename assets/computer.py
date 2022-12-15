import qiskit
import pygame
from . import globals


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

        if pygame.sprite.collide_mask(ball, self.paddle):
            ball.bounce()


class QuantumComputer(Computer):
    def __init__(self, quantum_paddles, quantum_bricks, circuit_grid):
        self.paddles = quantum_paddles.paddles
        self.bricks = quantum_bricks.bricks
        self.circuit_grid = circuit_grid

        self.score = 0
        self.measured_state = 0
        self.last_measurement_time = pygame.time.get_ticks() - \
            globals.MEASUREMENT_COOLDOWN_TIME
        self.last_brick_broken = pygame.time.get_ticks() - \
            globals.MEASUREMENT_COOLDOWN_TIME

    def update(self, ball):
        current_time = pygame.time.get_ticks()

        # when ball close to paddle or brick, measure
        if 40 < ball.rect.x / globals.WIDTH_UNIT < 54:
            if current_time - self.last_brick_broken > globals.MEASUREMENT_COOLDOWN_TIME:
                self.brick_after_measurement(current_time)
                self.last_brick_broken = pygame.time.get_ticks()
        else:
            self.brick_before_measurement(current_time)

        if 88 < ball.rect.x / globals.WIDTH_UNIT < 92:
            if current_time - self.last_measurement_time > globals.MEASUREMENT_COOLDOWN_TIME:
                self.paddle_after_measurement()
                self.last_measurement_time = pygame.time.get_ticks()
        else:
            self.paddle_before_measurement()

        if pygame.sprite.collide_mask(ball, self.paddles[self.measured_state]):
            ball.bounce()

        if pygame.sprite.collide_mask(ball, self.bricks[self.measured_state]) and self.bricks[self.measured_state].is_breakable(current_time):
            ball.bounce()
            self.bricks[self.measured_state].disintegrate()

    # simulates measuring a quantum state and collapsing superpositions
    def set_measured_state(self):
        simulator = qiskit.BasicAer.get_backend("qasm_simulator")
        circuit = self.circuit_grid.model.compute_circuit()
        circuit.measure_all()

        transpiled_circuit = qiskit.transpile(circuit, simulator)
        counts = simulator.run(
            transpiled_circuit, shots=1).result().get_counts()
        self.measured_state = int(list(counts.keys())[0], 2)

# I attempted to implement Grover's algorithm to make the quantum paddle placement more accurate
# The bricks would have been the only thing controlled by the player's circuit
# unfortunately I don't understand the gates used well enough to fully implement it
    def place_paddle(self, ball_y):
        qr = qiskit.QuantumRegister(3)
        cr = qiskit.ClassicalRegister(3)

        oracle = qiskit.QuantumCircuit(qr, cr)

        qr = qiskit.QuantumRegister(3)
        cr = qiskit.ClassicalRegister(3)

        amplifier = qiskit.QuantumCircuit(qr, cr)
        amplifier.barrier(qr)
        amplifier.h(qr)
        amplifier.x(qr)

        amplifier.h(qr[1])
        amplifier.ccx(qr[0], qr[1], qr[2])
        amplifier.h(qr[2])

        amplifier.barrier(qr)
        amplifier.x(qr)
        amplifier.h(qr)

    def get_statevectors(self):
        simulator = qiskit.BasicAer.get_backend(
            "statevector_simulator")  # simulated quantum computing
        circuit = self.circuit_grid.model.compute_circuit()
        transpiled_circuit = qiskit.transpile(circuit, simulator)
        statevector = simulator.run(transpiled_circuit, shots=100).result(
        ).get_statevector()  # lower accuracy (shots) higher speed

        return statevector

    def paddle_before_measurement(self):
        # changes opacity of paddle based on state vector probability
        # (fully opaque for 100% certainty to transparent for 0% certainty)
        for basis_state, amplitude in enumerate(self.get_statevectors()):
            self.paddles[basis_state].image.set_alpha(amplitude ** 2 * 255)

    def paddle_after_measurement(self):
        self.set_measured_state()

        # reset all paddles to transparent
        for paddle in self.paddles:
            paddle.image.set_alpha(0)

        # set most certain paddle to fully opaque
        self.paddles[self.measured_state].image.set_alpha(255)

    def brick_before_measurement(self, current_time):
        # changes opacity brick
        for basis_state, amplitude in enumerate(self.get_statevectors()):
            if self.bricks[self.measured_state].is_breakable(current_time):
                self.bricks[basis_state].image.set_alpha(amplitude ** 2 * 255)

    def brick_after_measurement(self, current_time):
        self.set_measured_state()

        # reset all bricks to transparent
        for brick in self.bricks:
            brick.image.set_alpha(0)

        if self.bricks[self.measured_state].is_breakable(current_time):
            self.bricks[self.measured_state].image.set_alpha(255)
