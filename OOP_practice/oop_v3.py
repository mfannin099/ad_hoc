class Exercise:
    def __init__(self, name: str, muscle_group: str, sets: int, reps: str):
        self.name = name
        self.muscle_group = muscle_group
        self.sets = sets
        self.reps = reps

    def __str__(self):
        return f" ({self.muscle_group}) - {self.name} - {self.sets} sets of {self.reps} reps"
    

class Workout:
    def __init__(self, name: str):
        self.name = name
        self.exercises = []

    def add_exercise(self, exercise: Exercise):
        self.exercises.append(exercise)

    def __str__(self):
        workout_str = f"Workout: {self.name}\n"
        for ex in self.exercises:
            workout_str += str(ex) + "\n"
        return workout_str





e1 = Exercise('DB bench press', 'chest', 4, "8-10")
e2 = Exercise('Pec Flies', 'chest', 3, "10-15")
e3 = Exercise('DB Shoulder press', 'shoulders', 4, "6-8")
e4 = Exercise('tricep push down', 'triceps', 5, "8-15")
e5 = Exercise('DB Skullcrushers', 'triceps', 3, "12-15")

workout1 = Workout("Chest Day")

workout1.add_exercise(e1)
workout1.add_exercise(e2)
workout1.add_exercise(e3)
workout1.add_exercise(e4)
workout1.add_exercise(e5)
print(workout1)

