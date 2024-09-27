import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

# main class for the calorie tracker
class CalorieTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Calorie Tracker")  # setting the window title

        # creating the notebook to hold tabs
        self.notebook = ttk.Notebook(root)
        self.notebook.pack(pady=10, expand=True)

        # creating frames for each tab
        self.log_frame = tk.Frame(self.notebook, width=400, height=400)
        self.maintenance_frame = tk.Frame(self.notebook, width=400, height=400)

        # adding the frames to the notebook and making them expandable
        self.log_frame.pack(fill="both", expand=True)
        self.maintenance_frame.pack(fill="both", expand=True)

        # adding tabs to the notebook for logging food and calculating maintenance calories
        self.notebook.add(self.log_frame, text="Log Food")
        self.notebook.add(self.maintenance_frame, text="Maintenance Calories")

        # setting up each tab
        self.create_log_tab()
        self.create_maintenance_tab()

    # this method sets up the log food tab
    def create_log_tab(self):
        # creating food input and label
        self.food_label = tk.Label(self.log_frame, text="Food:")
        self.food_label.grid(row=0, column=0, padx=10, pady=5)
        self.food_entry = tk.Entry(self.log_frame)
        self.food_entry.grid(row=0, column=1, padx=10, pady=5)

        # creating calories input and label
        self.calories_label = tk.Label(self.log_frame, text="Calories:")
        self.calories_label.grid(row=1, column=0, padx=10, pady=5)
        self.calories_entry = tk.Entry(self.log_frame)
        self.calories_entry.grid(row=1, column=1, padx=10, pady=5)

        # add button for food and calories
        self.add_button = tk.Button(self.log_frame, text="Add", command=self.add_food)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # listbox to display the logged food items
        self.food_listbox = tk.Listbox(self.log_frame, width=50)
        self.food_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # this method sets up the maintenance calories tab
    def create_maintenance_tab(self):
        # creating inputs for age, gender, weight, height, and activity level
        self.age_label = tk.Label(self.maintenance_frame, text="Age:")
        self.age_label.grid(row=0, column=0, padx=10, pady=5)
        self.age_entry = tk.Entry(self.maintenance_frame)
        self.age_entry.grid(row=0, column=1, padx=10, pady=5)

        self.gender_label = tk.Label(self.maintenance_frame, text="Gender (M/F):")
        self.gender_label.grid(row=1, column=0, padx=10, pady=5)
        self.gender_entry = tk.Entry(self.maintenance_frame)
        self.gender_entry.grid(row=1, column=1, padx=10, pady=5)

        self.weight_label = tk.Label(self.maintenance_frame, text="Weight (kg):")
        self.weight_label.grid(row=2, column=0, padx=10, pady=5)
        self.weight_entry = tk.Entry(self.maintenance_frame)
        self.weight_entry.grid(row=2, column=1, padx=10, pady=5)

        self.height_label = tk.Label(self.maintenance_frame, text="Height (cm):")
        self.height_label.grid(row=3, column=0, padx=10, pady=5)
        self.height_entry = tk.Entry(self.maintenance_frame)
        self.height_entry.grid(row=3, column=1, padx=10, pady=5)

        self.activity_label = tk.Label(self.maintenance_frame, text="Activity Level (1-5):")
        self.activity_label.grid(row=4, column=0, padx=10, pady=5)
        self.activity_entry = tk.Entry(self.maintenance_frame)
        self.activity_entry.grid(row=4, column=1, padx=10, pady=5)

        # button to calculate the maintenance calories
        self.calc_button = tk.Button(self.maintenance_frame, text="Calculate", command=self.calculate_maintenance_calories)
        self.calc_button.grid(row=5, column=0, columnspan=2, pady=10)

        # label to display the result
        self.result_label = tk.Label(self.maintenance_frame, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)

    # function to add food to the listbox
    def add_food(self):
        food = self.food_entry.get()  # getting the food input
        calories = self.calories_entry.get()  # getting the calorie input

        if food and calories:  # checking if both fields are filled
            try:
                calories = int(calories)  # converting calories to integer
                self.food_listbox.insert(tk.END, f"{food}: {calories} calories")  # adding to the listbox
                self.food_entry.delete(0, tk.END)  # clearing the food input field
                self.calories_entry.delete(0, tk.END)  # clearing the calories input field
            except ValueError:
                # show an error if the calories are not a valid number
                messagebox.showerror("Invalid input", "Please enter a valid number for calories")
        else:
            # show a warning if fields are empty
            messagebox.showwarning("Input error", "Please fill out both fields")

    # function to calculate maintenance calories based on user input
    def calculate_maintenance_calories(self):
        try:
            # gathering all the input values
            age = int(self.age_entry.get())
            gender = self.gender_entry.get().upper()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            activity_level = int(self.activity_entry.get())

            # ensuring the gender input is valid
            if gender not in ['M', 'F']:
                raise ValueError("Invalid gender")

            # ensuring the activity level is within the valid range
            if not 1 <= activity_level <= 5:
                raise ValueError("Invalid activity level")

            # calculating the bmr based on gender
            if gender == 'M':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            # using activity level to calculate total maintenance calories
            activity_factors = {
                1: 1.2,   # sedentary
                2: 1.375, # lightly active
                3: 1.55,  # moderately active
                4: 1.725, # very active
                5: 1.9    # super active
            }

            # calculating maintenance calories
            maintenance_calories = bmr * activity_factors[activity_level]

            # displaying the result
            self.result_label.config(text=f"Maintenance Calories: {maintenance_calories:.2f}")
        except ValueError as e:
            # show an error if there is an issue with the input
            messagebox.showerror("Invalid input", str(e))

if __name__ == "__main__":
    root = tk.Tk()  # creating the main tkinter window
    app = CalorieTracker(root)  # initializing the CalorieTracker class
    root.mainloop()  # starting the main loop to keep the window running
