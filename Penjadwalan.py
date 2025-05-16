import random

# Data
courses = ["A", "B", "C", "D"]
times = ["Senin", "Selasa"]
rooms = ["R1", "R2"]

# Mahasiswa dan mata kuliah yang diambil
students = {
    "M1": ["A", "C"],
    "M2": ["B", "D"]
}

# Param GA
POP_SIZE = 30
GENERATIONS = 100
MUTATION_RATE = 0.2

# Representasi kromosom: dict course -> (time, room)
def generate_chromosome():
    return {course: (random.choice(times), random.choice(rooms)) for course in courses}

# Fitness: penalti konflik mahasiswa dan ruangan
def calculate_fitness(chromosome):
    conflict = 0

    # Cek konflik mahasiswa
    for student, student_courses in students.items():
        scheduled = []
        for course in student_courses:
            scheduled.append(chromosome[course])
        # Jika ada dua mata kuliah mahasiswa yang waktunya sama, konflik
        if scheduled[0][0] == scheduled[1][0]:  # waktu sama
            conflict += 1

    # Cek konflik ruangan
    seen = {}
    for course, (time, room) in chromosome.items():
        key = (time, room)
        if key in seen:
            conflict += 1
        else:
            seen[key] = course

    return 1 / (1 + conflict)  # makin kecil konflik, makin besar fitness

# Seleksi (tournament)
def selection(population):
    k = 3
    selected = random.sample(population, k)
    return max(selected, key=lambda chromo: calculate_fitness(chromo))

# Crossover
def crossover(parent1, parent2):
    child = {}
    for course in courses:
        child[course] = parent1[course] if random.random() < 0.5 else parent2[course]
    return child

# Mutasi
def mutate(chromosome):
    if random.random() < MUTATION_RATE:
        course = random.choice(courses)
        chromosome[course] = (random.choice(times), random.choice(rooms))
    return chromosome

# Algoritma Genetika
def genetic_algorithm():
    population = [generate_chromosome() for _ in range(POP_SIZE)]
    best = max(population, key=lambda chromo: calculate_fitness(chromo))

    for _ in range(GENERATIONS):
        new_pop = []
        for _ in range(POP_SIZE):
            p1 = selection(population)
            p2 = selection(population)
            child = crossover(p1, p2)
            child = mutate(child)
            new_pop.append(child)

        population = new_pop
        current_best = max(population, key=lambda chromo: calculate_fitness(chromo))
        if calculate_fitness(current_best) > calculate_fitness(best):
            best = current_best

    return best, calculate_fitness(best)

# Jalankan
best_schedule, best_fitness = genetic_algorithm()

# Tampilkan hasil
print("\n Jadwal Terbaik:")
for course, (time, room) in best_schedule.items():
    print(f"  Mata Kuliah {course}: {time}, Ruang {room}")

print("\n Fitness:", round(best_fitness, 3))
