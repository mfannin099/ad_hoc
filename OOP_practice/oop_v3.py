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
    
class WeeklyRoutine:
    def __init__(self):
        self.schedule = {}

    def add_workout(self, day: str, workout: Workout):
        self.schedule[day] = workout  

    def __str__(self):
        routine_str = "Weekly Workout Routine:\n"
        for day, workout in self.schedule.items():
            routine_str += f"\n{day}:\n{workout}"
        return routine_str





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


workout2 = Workout("Back Day")
e6 = Exercise("Deadlift", "Back", 4, "6-8")
e7 = Exercise("Lat Pull Down", "Back", 3, "8-14")
e8 = Exercise("Cable Pull", "Back", 4, "8-12")
e9 = Exercise("Bicep Curls", "Biceps", 5, "8-12")

for i in range(6,10):
    workout2.add_exercise(globals()[f"e{i}"])
print("-------------")
print(workout2)


workout3 = Workout("Leg Day")
e10 = Exercise("Squat", "Legs", 4, "6-8")
e11 = Exercise("Leg Extension", "Legs", 3, "8-14")
e12 = Exercise("Calf Raise", "Legs", 4, "8-12")
e13 = Exercise("DB Romanian Deadlift", "Legs", 3, "8-12")

for i in range(10,14):
    workout3.add_exercise(globals()[f"e{i}"])
print("-------------")
print(workout3)

## Create the Weekly Routine
week1 = WeeklyRoutine()
week1.add_workout("Monday", workout1)   # Chest Day
week1.add_workout("Wednesday", workout2)  # Back Day
week1.add_workout("Friday", workout3)   # Leg Day

print("-------------")
print("-------------")
print(week1)

