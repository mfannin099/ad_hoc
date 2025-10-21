## Script to select the punishment for the GFL

import random
import time
import tkinter as tk

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
hot_ones_weights = [30, 10, 30, 30]

def spin_wheel():
    """Generates the random punishments and updates the GUI Label."""
    
    # Clear previous results
    main_result_label.config(text="spinning wheel...")
    secondary_result_label.config(text="")
    
    # Simulate a delay for dramatic effect (freezes GUI briefly)
    root.update() # Forces the GUI to update immediately before sleeping
    time.sleep(2)
    
    # Main spin logic
    random_value = random.randint(1, 6)
    
    if random_value == 2: # Second Spin for Dafoe
        main_result_label.config(text="The Weekly Punishment in The GFL will be: Pose!")
        
        secondary_result_label.config(text="spinning wheel for william dafoe pose...")
        root.update()
        time.sleep(2)
        
        second_spin_value = random.randint(1, 5)
        pose_result = william_dafoe_d[second_spin_value]
        secondary_result_label.config(text=f"The William Dafoe pose will be: {pose_result}")
        
    elif random_value == 3: # Second Spin for Hot Ones
        main_result_label.config(text="The Weekly Punishment in The GFL will be: Hot Ones!")

        secondary_result_label.config(text="spinning wheel for Hot Ones...")
        root.update()
        time.sleep(2)
        
        choices = list(hot_ones_d.keys())
        second_spin_value = random.choices(choices, weights=hot_ones_weights, k=1)[0]
        hot_sauce_result = hot_ones_d[second_spin_value]
        
        secondary_result_label.config(text=f"The hot food will be: {hot_sauce_result}")
        
    else:
        # Standard punishment or 'better luck next week'
        punishment_text = punishments_d[random_value]
        main_result_label.config(text=f"The Weekly Punishment in The GFL will be: {punishment_text}")
        secondary_result_label.config(text="Better Luck next week (no secondary spin)")

# 1. Create the main window
root = tk.Tk()
root.title("Generic Fantasy Football: Weekly Punishment Wheel Spin")
root.geometry("600x300")
root.configure(bg='#333333')

spin_button = tk.Button(
    root, 
    text="Spin the Wheel", 
    command=spin_wheel, # This links the button to the function above
    font=("Helvetica", 18),
    bg='#FF5733',
    fg='white',
    pady=10,
    padx=20
)
spin_button.pack(pady=30)

# Label to display the main result
main_result_label = tk.Label(
    root, 
    text="Click 'Spin the Wheel' to find your fate.", 
    font=("Helvetica", 14), 
    bg='#333333',
    fg='#4CAF50',
    wraplength=580 # Wraps text so it fits in the window
)
main_result_label.pack(pady=20)

# Label to display the secondary (spin-off) result
secondary_result_label = tk.Label(
    root, 
    text="", 
    font=("Helvetica", 12), 
    bg='#333333',
    fg='#FFC300',
    wraplength=580
)
secondary_result_label.pack(pady=10)

root.mainloop()
