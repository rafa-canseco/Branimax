import random

def generate_timer(min: int, max: int) -> int:
    num_sal = random.random()
    numero_aleatorio = int(num_sal * (max - min + 1)) + min
    return numero_aleatorio

