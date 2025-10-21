## Script to select the punishment for the GFL

import random
import time

# Dictionary of Punishments and choices

punishments_d = {
    1: "Fruit Pledge",
    2: "William Dafoe Pose",
    3: "Hot Ones",
    4: "Weatherman",
    5: "Beer Pour",
    6: "Fast Banana"
}

william_dafoe_d = {
    1 : "Pose 1",
    2 : "Pose 2",
    3 : "Pose 3",
    4 : "Pose 4",
    5 : "Pose 5",
}

hot_ones_d = {
    1 : "Bell Pepper",
    2 : "Ghost Pepper Chip",
    3: "Jalapeño",
    4: "Another Hot Pepper"
}
weights = [30, 10, 30, 30]

## Beginning of Random Number Generator

random_value = random.randint(1,6)

print("spinning wheel...")
time.sleep(2)
print("The Weekly Punishment in The GFL will be, ", punishments_d[random_value])

if random_value == 2:
    second_spin_value = random.randint(1,5)
    print("spinning wheel for william dafoe pose...")
    time.sleep(2)
    print("The William Dafoe pose will be, ", william_dafoe_d[second_spin_value])
elif random_value == 3:
    second_spin_value = random.choices(list(hot_ones_d.keys()), weights=weights, k=1)[0]
    print("spinning wheel for Hot Ones...")
    time.sleep(2)
    print("The hot food will be, ", hot_ones_d[second_spin_value])
else:
    print("Better Luck next week")
