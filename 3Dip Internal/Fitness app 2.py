import tkinter as tk
from tkinter import ttk
from tkinter import messagebox, filedialog

class LogFoodTab:
    # set up the LogFoodTab class
    def __init__(self, parent):
        # make a new frame for the log food section
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        # variable to track total calories
        self.total_calories = 0

        # create the widgets like labels, entry boxes, and buttons
        self.create_widgets()

    def create_widgets(self):
        # label and input box for the food name
        self.food_label = tk.Label(self.frame, text="Food:")
        self.food_label.grid(row=0, column=0, padx=10, pady=5)
        self.food_entry = tk.Entry(self.frame)
        self.food_entry.grid(row=0, column=1, padx=10, pady=5)

        # label and input box for the calories
        self.calories_label = tk.Label(self.frame, text="Calories:")
        self.calories_label.grid(row=1, column=0, padx=10, pady=5)
        self.calories_entry = tk.Entry(self.frame)
        self.calories_entry.grid(row=1, column=1, padx=10, pady=5)

        # button to add food and calories to the list
        self.add_button = tk.Button(self.frame, text="Add", command=self.add_food)
        self.add_button.grid(row=2, column=0, columnspan=2, pady=10)

        # listbox to show all foods and calories
        self.food_listbox = tk.Listbox(self.frame, width=50)
        self.food_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # label to show the total calories
        self.total_label = tk.Label(self.frame, text="Total Calories: 0")
        self.total_label.grid(row=4, column=0, columnspan=2, padx=10, pady=5)

        # button to save the food log to a file
        self.save_button = tk.Button(self.frame, text="Save Log to File", command=self.save_log_to_file)
        self.save_button.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

    def add_food(self):
        # get the food and calories from the entry boxes
        food = self.food_entry.get()
        calories = self.calories_entry.get()

        if food and calories:
            try:
                # convert calories to an integer and add to total
                calories = int(calories)
                self.total_calories += calories
                # add the food and its calories to the listbox
                self.food_listbox.insert(tk.END, f"{food}: {calories} calories")
                # update the total calories label
                self.total_label.config(text=f"Total Calories: {self.total_calories}")
                # clear the input boxes
                self.food_entry.delete(0, tk.END)
                self.calories_entry.delete(0, tk.END)
            except ValueError:
                # show error if the calories input isn't a valid number
                messagebox.showerror("Invalid input", "Please enter a valid number for calories")
        else:
            # warn the user if either input field is empty
            messagebox.showwarning("Input error", "Please fill out both fields")

    def save_log_to_file(self):
        # open a file dialog for saving the log
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])

        if not file_path:
            return  # exit if no file is selected

        try:
            # write the food log to the selected file
            with open(file_path, 'w') as file:
                file.write("Food Log:\n")
                for item in self.food_listbox.get(0, tk.END):
                    file.write(item + "\n")
                file.write(f"\nTotal Calories: {self.total_calories}")
            # show success message
            messagebox.showinfo("Success", "Food log saved successfully!")
        except Exception as e:
            # show an error message if saving fails
            messagebox.showerror("Error", f"An error occurred: {e}")

class MaintenanceTab:
    # set up the MaintenanceTab class
    def __init__(self, parent):
        # make a new frame for the maintenance tab
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        # create all the labels, input boxes, and buttons
        self.create_widgets()

    def create_widgets(self):
        # labels and input fields for the user's details like age, gender, etc.
        self.age_label = tk.Label(self.frame, text="Age:")
        self.age_label.grid(row=0, column=0, padx=10, pady=5)
        self.age_entry = tk.Entry(self.frame)
        self.age_entry.grid(row=0, column=1, padx=10, pady=5)

        self.gender_label = tk.Label(self.frame, text="Gender (M/F):")
        self.gender_label.grid(row=1, column=0, padx=10, pady=5)
        self.gender_entry = tk.Entry(self.frame)
        self.gender_entry.grid(row=1, column=1, padx=10, pady=5)

        self.weight_label = tk.Label(self.frame, text="Weight (kg):")
        self.weight_label.grid(row=2, column=0, padx=10, pady=5)
        self.weight_entry = tk.Entry(self.frame)
        self.weight_entry.grid(row=2, column=1, padx=10, pady=5)

        self.height_label = tk.Label(self.frame, text="Height (cm):")
        self.height_label.grid(row=3, column=0, padx=10, pady=5)
        self.height_entry = tk.Entry(self.frame)
        self.height_entry.grid(row=3, column=1, padx=10, pady=5)

        self.activity_label = tk.Label(self.frame, text="Activity Level (1-5):")
        self.activity_label.grid(row=4, column=0, padx=10, pady=5)
        self.activity_entry = tk.Entry(self.frame)
        self.activity_entry.grid(row=4, column=1, padx=10, pady=5)

        # button to calculate maintenance calories
        self.calc_button = tk.Button(self.frame, text="Calculate", command=self.calculate_maintenance_calories)
        self.calc_button.grid(row=5, column=0, columnspan=2, pady=10)

        # label to show the result of the calculation
        self.result_label = tk.Label(self.frame, text="")
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)

    def calculate_maintenance_calories(self):
        try:
            # get user inputs and calculate BMR based on the activity level
            age = int(self.age_entry.get())
            gender = self.gender_entry.get().upper()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            activity_level = int(self.activity_entry.get())

            if gender not in ['M', 'F']:
                raise ValueError("Invalid gender")  # error if gender is invalid

            if not 1 <= activity_level <= 5:
                raise ValueError("Invalid activity level")  # error if activity level is out of range

            # formula for calculating BMR based on gender
            if gender == 'M':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            # activity factor used to adjust BMR
            activity_factors = {
                1: 1.2,   # Sedentary (little or no exercise)
                2: 1.375, # Lightly active
                3: 1.55,  # Moderately active
                4: 1.725, # Very active
                5: 1.9    # Super active
            }

            # final calculation of maintenance calories
            maintenance_calories = bmr * activity_factors[activity_level]

            # update the result label with the calculated maintenance calories
            self.result_label.config(text=f"Maintenance Calories: {maintenance_calories:.2f}")
        except ValueError as e:
            messagebox.showerror("Invalid input", str(e))

class FoodSuggesterTab:
    # set up the FoodSuggesterTab class
    def __init__(self, parent):
        # make a new frame for the food suggester section
        self.frame = tk.Frame(parent)
        self.frame.pack(fill="both", expand=True)

        # create the widgets for this tab
        self.create_widgets()

    def create_widgets(self):
        # label and dropdown menu to select a diet type
        self.diet_label = tk.Label(self.frame, text="Select Diet Type:")
        self.diet_label.grid(row=0, column=0, padx=10, pady=5)
        
        self.diet_options = ["Vegan", "Vegetarian", "Meat"]
        self.selected_diet = tk.StringVar()
        self.selected_diet.set(self.diet_options[0])  # default option is Vegan
        
        self.diet_menu = tk.OptionMenu(self.frame, self.selected_diet, *self.diet_options)
        self.diet_menu.grid(row=0, column=1, padx=10, pady=5)

        # button to get food suggestions based on the selected diet
        self.suggest_button = tk.Button(self.frame, text="Suggest Foods", command=self.suggest_foods)
        self.suggest_button.grid(row=1, column=0, columnspan=2, pady=10)

        # listbox to show the food suggestions
        self.suggestions_listbox = tk.Listbox(self.frame, width=50)
        self.suggestions_listbox.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

    def suggest_foods(self):
        # clear the listbox before adding new suggestions
        self.suggestions_listbox.delete(0, tk.END)
        
        # get the selected diet type
        diet_type = self.selected_diet.get()

        # define food suggestions for each diet type
        suggestions = []
        if diet_type == "Vegan":
            suggestions = ["Tofu", "Quinoa", "Chickpeas", "Lentils", "Almonds", "Soy Milk"]
        elif diet_type == "Vegetarian":
            suggestions = ["Eggs", "Greek Yogurt", "Cheese", "Paneer", "Vegetable Stir-fry"]
        elif diet_type == "Meat":
            suggestions = ["Chicken Breast", "Salmon", "Beef", "Pork Chops", "Turkey"]
        
        # add the suggestions to the listbox
        for food in suggestions:
            self.suggestions_listbox.insert(tk.END, food)

class MainApp:
    # main application class that holds all the tabs
    def __init__(self, root):
        self.root = root
        self.root.title("Calorie Tracker & Food Suggester")

        # method to create the tabs
        self.create_tabs()

    def create_tabs(self):
        # make a notebook to hold the different tabs
        tab_control = ttk.Notebook(self.root)
        
        # log food tab
        log_food_tab = LogFoodTab(tab_control)
        tab_control.add(log_food_tab.frame, text="Log Food")
        
        # maintenance calories tab
        maintenance_tab = MaintenanceTab(tab_control)
        tab_control.add(maintenance_tab.frame, text="Maintenance Calories")
        
        # food suggester tab
        food_suggester_tab = FoodSuggesterTab(tab_control)
        tab_control.add(food_suggester_tab.frame, text="Food Suggester")
        
        # pack the tabs into the window
        tab_control.pack(expand=1, fill="both")

if __name__ == "__main__":
    # create the main window and run the app
    root = tk.Tk()
    app = MainApp(root)
    root.mainloop()
