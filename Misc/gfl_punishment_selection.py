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

## Beginning of Random Number Generator

random_value = random.randint(1,6)

print("spinning wheel...")
time.sleep(2)
print("The Weekly Punishment in The GFL will be, ", punishments_d[random_value])