import tkinter as tk
from tkinter import messagebox, filedialog
import json
import os
from PIL import Image, ImageTk

# path to store user data and food log
USER_DATA_FILE = "users.json"
FOOD_LOG_FILE = "food_log.json"

class Body:
    def __init__(self, root):
        # set up the main window with background and dimensions
        self.root = root
        self.root.geometry("600x400")
        self.root.configure(bg="#E6E6FA")

        # initially show the login page
        self.show_login_page()

    # function to display the login page
    def show_login_page(self):
        self.clear_window()  # clears the current frame
        self.login_frame = tk.Frame(self.root, bg="#E6E6FA")
        self.login_frame.pack(fill="both", expand=True)

        # login page widgets (labels, entry fields, and buttons)
        login_label = tk.Label(self.login_frame, text="Login", font=("Arial", 18), bg="#E6E6FA")
        login_label.pack(pady=20)

        username_label = tk.Label(self.login_frame, text="Username", bg="#E6E6FA")
        username_label.pack(pady=5)
        self.username_entry = tk.Entry(self.login_frame)  # input for username
        self.username_entry.pack(pady=5)

        password_label = tk.Label(self.login_frame, text="Password", bg="#E6E6FA")
        password_label.pack(pady=5)
        self.password_entry = tk.Entry(self.login_frame, show="*")  # password input field, hidden characters
        self.password_entry.pack(pady=5)

        # login and register buttons
        login_button = tk.Button(self.login_frame, text="Login", command=self.check_login, bg="#D8BFD8")
        login_button.pack(pady=20)

        register_button = tk.Button(self.login_frame, text="Register", command=self.show_register_page, bg="#D8BFD8")
        register_button.pack(pady=5)

    # function to clear the current window content
    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.pack_forget()  # remove all widgets in the current window

    # function to check if the login is valid
    def check_login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        # if no users are registered, show an error
        if not os.path.exists(USER_DATA_FILE):
            messagebox.showerror("login failed", "no users are registered yet. please register first!")
            return

        # read user data from the JSON file
        with open(USER_DATA_FILE, "r") as file:
            users = json.load(file)

        # check if the username and password match
        if username in users and users[username] == password:
            self.login_frame.pack_forget()  # hide the login page
            self.show_home_page()  # display the home page
        else:
            messagebox.showerror("login failed", "invalid username or password!")

    # function to display the registration page
    def show_register_page(self):
        self.clear_window()
        self.register_frame = tk.Frame(self.root, bg="#E6E6FA")
        self.register_frame.pack(fill="both", expand=True)

        # register page widgets (labels, entry fields, and buttons)
        register_label = tk.Label(self.register_frame, text="Register", font=("Arial", 18), bg="#E6E6FA")
        register_label.pack(pady=20)

        username_label = tk.Label(self.register_frame, text="choose a username", bg="#E6E6FA")
        username_label.pack(pady=5)
        self.new_username_entry = tk.Entry(self.register_frame)
        self.new_username_entry.pack(pady=5)

        password_label = tk.Label(self.register_frame, text="choose a password", bg="#E6E6FA")
        password_label.pack(pady=5)
        self.new_password_entry = tk.Entry(self.register_frame, show="*")
        self.new_password_entry.pack(pady=5)

        register_button = tk.Button(self.register_frame, text="create account", command=self.register_user, bg="#D8BFD8")
        register_button.pack(pady=20)

        back_to_login_button = tk.Button(self.register_frame, text="back to login", command=self.show_login_page_from_register, bg="#D8BFD8")
        back_to_login_button.pack(pady=5)

    # function to return to login page from registration
    def show_login_page_from_register(self):
        self.register_frame.pack_forget()
        self.show_login_page()

    # function to register a new user
    def register_user(self):
        new_username = self.new_username_entry.get()
        new_password = self.new_password_entry.get()

        # if either username or password is empty, show warning
        if not new_username or not new_password:
            messagebox.showwarning("registration failed", "both fields must be filled out!")
            return

        users = {}
        # if the users JSON file exists, load the users data
        if os.path.exists(USER_DATA_FILE):
            with open(USER_DATA_FILE, "r") as file:
                try:
                    users = json.load(file)
                except json.JSONDecodeError:
                    users = {}

        # check if the username already exists
        if new_username in users:
            messagebox.showerror("registration failed", "username already exists! please choose another one.")
            return

        # save the new username and password in the JSON file
        users[new_username] = new_password

        try:
            with open(USER_DATA_FILE, "w") as file:
                json.dump(users, file)
            messagebox.showinfo("registration successful", "account created successfully! you can now log in.")
            self.register_frame.pack_forget()
            self.show_login_page()
        except Exception as e:
            messagebox.showerror("error", f"an error occurred while saving the user: {e}")

    # function to display the home page after login
    def show_home_page(self):
        self.clear_window()
        self.home_frame = tk.Frame(self.root, bg="#E6E6FA")
        self.home_frame.pack(fill="both", expand=True)

        welcome_label = tk.Label(self.home_frame, text="welcome to calorie tracker", font=("Arial", 16), bg="#E6E6FA")
        welcome_label.pack(pady=20)

        log_food_button = tk.Button(self.home_frame, text="log food", command=self.show_log_food, width=20, height=2, bg="#D8BFD8")
        log_food_button.pack(pady=10)

        maintenance_button = tk.Button(self.home_frame, text="maintenance calories", command=self.show_maintenance, width=20, height=2, bg="#D8BFD8")
        maintenance_button.pack(pady=10)

        suggester_button = tk.Button(self.home_frame, text="meal suggester", command=self.show_meal_suggester, width=20, height=2, bg="#D8BFD8")
        suggester_button.pack(pady=10)

        logout_button = tk.Button(self.home_frame, text="logout", command=self.logout, width=20, height=2, bg="#D8BFD8")
        logout_button.pack(pady=20)

    # function to log out the user and return to login screen
    def logout(self):
        messagebox.showinfo("logged out", "you have been logged out successfully!")
        self.clear_window()
        self.show_login_page()

    # function to show the food logging tab
    def show_log_food(self):
        self.clear_window()
        self.log_food_tab = LogFoodTab(self.root, self.go_home)

    # function to show the maintenance calories tab
    def show_maintenance(self):
        self.clear_window()
        self.maintenance_tab = MaintenanceTab(self.root, self.go_home)

    # function to show the meal suggester tab
    def show_meal_suggester(self):
        self.clear_window()
        self.meal_suggester_tab = FoodSuggesterTab(self.root, self.go_home)

    # returns to the home screen
    def go_home(self):
        self.clear_window()
        self.show_home_page()


# Base class for all tab components (this class provides common functionality for all tabs)
class TabBase:
    def __init__(self, parent, go_home_callback, image_path):
        self.frame = tk.Frame(parent, bg="#E6E6FA")
        self.frame.pack(fill="both", expand=True)
        self.go_home_callback = go_home_callback
        self.image_path = image_path

        # load and display the image if available
        self.load_image(image_path)

        # add a home button to the top left
        self.create_home_button()

    # function to load the tab image
    def load_image(self, image_path):
        if os.path.exists(image_path):
            try:
                image = Image.open(image_path)
                resized_image = image.resize((300, 250))  # Resize to fit
                self.image = ImageTk.PhotoImage(resized_image)
                self.image_label = tk.Label(self.frame, image=self.image, bg="#E6E6FA")
                self.image_label.grid(row=1, column=2, rowspan=6, padx=10, pady=10)
            except Exception as e:
                messagebox.showerror("Image Error", f"Failed to load image: {e}")
        else:
            messagebox.showerror("File Error", f"Image file not found: {image_path}")

    # function to create a home button
    def create_home_button(self):
        home_button = tk.Button(self.frame, text="home", command=self.go_home_callback, bg="#D8BFD8", fg="black")
        home_button.grid(row=0, column=0, padx=10, pady=10, sticky="w")


# LogFoodTab inherits from TabBase and adds specific functionality for logging food
class LogFoodTab(TabBase):
    def __init__(self, parent, go_home_callback):
        # use super() to call the __init__ method of the parent class (TabBase)
        super().__init__(parent, go_home_callback, "images/log_food_image.png")
        self.food_log = self.load_food_log()  # load the food log from the file
        self.total_calories = sum(item['calories'] for item in self.food_log)  # calculate the total calories
        self.create_widgets()  # create widgets for food input and display

    # function to create input widgets for the log food tab
    def create_widgets(self):
        self.food_label = tk.Label(self.frame, text="food:", bg="#E6E6FA")
        self.food_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.food_entry = tk.Entry(self.frame)
        self.food_entry.grid(row=1, column=1, padx=10, pady=5)

        self.calories_label = tk.Label(self.frame, text="calories:", bg="#E6E6FA")
        self.calories_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.calories_entry = tk.Entry(self.frame)
        self.calories_entry.grid(row=2, column=1, padx=10, pady=5)

        # button to add food to the log
        self.add_button = tk.Button(self.frame, text="add", command=self.add_food, bg="#D8BFD8", fg="black")
        self.add_button.grid(row=3, column=0, columnspan=2, pady=10)

        # listbox to display the food and calorie entries
        self.food_listbox = tk.Listbox(self.frame, width=50, bg="#FFFFFF")
        self.food_listbox.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # display the total calories
        self.total_label = tk.Label(self.frame, text=f"total calories: {self.total_calories}", bg="#E6E6FA")
        self.total_label.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        # button to save the food log
        self.save_button = tk.Button(self.frame, text="save log to file", command=self.save_log_to_file, bg="#D8BFD8", fg="black")
        self.save_button.grid(row=6, column=0, padx=10, pady=5)

        # button to clear the food log
        self.clear_button = tk.Button(self.frame, text="clear log", command=self.clear_food_log, bg="#D8BFD8", fg="black")
        self.clear_button.grid(row=6, column=1, padx=10, pady=5)

    # function to add food and calories to the list
    def add_food(self):
        food = self.food_entry.get()
        calories = self.calories_entry.get()
        if food and calories:
            try:
                calories = int(calories)
                self.total_calories += calories  # update total calories
                self.food_log.append({'food': food, 'calories': calories})  # add to food log list
                self.update_listbox()  # refresh the listbox with new data
                self.total_label.config(text=f"total calories: {self.total_calories}")  # update total label
                self.food_entry.delete(0, tk.END)  # clear entry after adding
                self.calories_entry.delete(0, tk.END)
                self.save_food_log()  # save the log after every addition
            except ValueError:
                messagebox.showerror("invalid input", "please enter a valid number for calories")
        else:
            messagebox.showwarning("input error", "please fill out both fields")

    # function to update the food listbox
    def update_listbox(self):
        self.food_listbox.delete(0, tk.END)
        for item in self.food_log:
            self.food_listbox.insert(tk.END, f"{item['food']}: {item['calories']} calories")

    # function to save the food log to a JSON file
    def save_food_log(self):
        with open(FOOD_LOG_FILE, "w") as file:
            json.dump(self.food_log, file)

    # function to load the food log from a JSON file
    def load_food_log(self):
        if os.path.exists(FOOD_LOG_FILE):
            with open(FOOD_LOG_FILE, "r") as file:
                return json.load(file)
        return []  # if the file does not exist, return an empty list

    # function to save the log to a file chosen by the user
    def save_log_to_file(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not file_path:
            return
        try:
            with open(file_path, 'w') as file:
                file.write("food log:\n")
                for item in self.food_log:
                    file.write(f"{item['food']}: {item['calories']} calories\n")
                file.write(f"\ntotal calories: {self.total_calories}")
            messagebox.showinfo("success", "food log saved successfully!")
        except Exception as e:
            messagebox.showerror("error", f"an error occurred: {e}")

    # function to clear the food log
    def clear_food_log(self):
        self.food_log.clear()  # empty the list
        self.total_calories = 0  # reset the total calories
        self.update_listbox()  # refresh the listbox
        self.total_label.config(text="total calories: 0")  # update total calories label
        if os.path.exists(FOOD_LOG_FILE):
            os.remove(FOOD_LOG_FILE)  # delete the log file if it exists


# MaintenanceTab inherits from TabBase and adds specific functionality for calculating maintenance calories
class MaintenanceTab(TabBase):
    def __init__(self, parent, go_home_callback):
        super().__init__(parent, go_home_callback, "images/maintenance_image.png")
        self.create_widgets()

    # function to create input widgets for the maintenance tab
    def create_widgets(self):
        self.age_label = tk.Label(self.frame, text="age:", bg="#E6E6FA")
        self.age_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")
        self.age_entry = tk.Entry(self.frame)
        self.age_entry.grid(row=1, column=1, padx=10, pady=5)

        self.gender_label = tk.Label(self.frame, text="gender (M/F):", bg="#E6E6FA")
        self.gender_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")
        self.gender_entry = tk.Entry(self.frame)
        self.gender_entry.grid(row=2, column=1, padx=10, pady=5)

        self.weight_label = tk.Label(self.frame, text="weight (kg):", bg="#E6E6FA")
        self.weight_label.grid(row=3, column=0, padx=10, pady=5, sticky="w")
        self.weight_entry = tk.Entry(self.frame)
        self.weight_entry.grid(row=3, column=1, padx=10, pady=5)

        self.height_label = tk.Label(self.frame, text="height (cm):", bg="#E6E6FA")
        self.height_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")
        self.height_entry = tk.Entry(self.frame)
        self.height_entry.grid(row=4, column=1, padx=10, pady=5)

        self.activity_label = tk.Label(self.frame, text="activity level (1-5):", bg="#E6E6FA")
        self.activity_label.grid(row=5, column=0, padx=10, pady=5, sticky="w")
        self.activity_entry = tk.Entry(self.frame)
        self.activity_entry.grid(row=5, column=1, padx=10, pady=5)

        self.calc_button = tk.Button(self.frame, text="calculate", command=self.calculate_maintenance_calories, bg="#D8BFD8", fg="black")
        self.calc_button.grid(row=6, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self.frame, text="", bg="#E6E6FA")
        self.result_label.grid(row=7, column=0, columnspan=2, pady=10)

    # function to calculate maintenance calories based on user input
    def calculate_maintenance_calories(self):
        try:
            age = int(self.age_entry.get())
            gender = self.gender_entry.get().upper()
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get())
            activity_level = int(self.activity_entry.get())

            if gender not in ['M', 'F']:
                raise ValueError("invalid gender")
            if not 1 <= activity_level <= 5:
                raise ValueError("invalid activity level")

            # calculate the basal metabolic rate (BMR) based on gender
            if gender == 'M':
                bmr = 10 * weight + 6.25 * height - 5 * age + 5
            else:
                bmr = 10 * weight + 6.25 * height - 5 * age - 161

            # activity level factors for calculating maintenance calories
            activity_factors = {
                1: 1.2,  # sedentary
                2: 1.375,  # lightly active
                3: 1.55,  # moderately active
                4: 1.725,  # very active
                5: 1.9  # super active
            }

            # calculate maintenance calories by multiplying BMR with activity factor
            maintenance_calories = bmr * activity_factors[activity_level]
            self.result_label.config(text=f"maintenance calories: {maintenance_calories:.2f}")
        except ValueError as e:
            messagebox.showerror("invalid input", str(e))


# FoodSuggesterTab inherits from TabBase and adds specific functionality for suggesting food based on diet type
class FoodSuggesterTab(TabBase):
    def __init__(self, parent, go_home_callback):
        super().__init__(parent, go_home_callback, "images/suggester_image.png")
        self.create_widgets()

    # function to create input widgets for food suggester tab
    def create_widgets(self):
        self.diet_label = tk.Label(self.frame, text="select diet type:", bg="#E6E6FA")
        self.diet_label.grid(row=1, column=0, padx=10, pady=5, sticky="w")

        # dropdown menu to select the diet type
        self.diet_options = ["Vegan", "Vegetarian", "Meat"]
        self.selected_diet = tk.StringVar()
        self.selected_diet.set(self.diet_options[0])  # default to vegan

        self.diet_menu = tk.OptionMenu(self.frame, self.selected_diet, *self.diet_options)
        self.diet_menu.grid(row=1, column=1, padx=10, pady=5)

        # button to suggest meals based on diet type
        self.suggest_button = tk.Button(self.frame, text="suggest meals", command=self.suggest_meal, bg="#D8BFD8", fg="black")
        self.suggest_button.grid(row=2, column=0, columnspan=2, pady=10)

        # listbox to display meal suggestions
        self.suggestion_listbox = tk.Listbox(self.frame, width=50, height=10, bg="#FFFFFF")
        self.suggestion_listbox.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # function to suggest meals based on selected diet
    def suggest_meal(self):
        diet = self.selected_diet.get()

        # list of meals based on diet type
        vegan_meals = ["vegan buddha bowl", "quinoa salad", "tofu stir-fry"]
        vegetarian_meals = ["vegetarian pizza", "pasta primavera", "eggplant parmesan"]
        meat_meals = ["grilled chicken salad", "steak and vegetables", "beef stir-fry"]

        # determine which meals to suggest based on diet
        if diet == "Vegan":
            meals_to_display = vegan_meals
        elif diet == "Vegetarian":
            meals_to_display = vegan_meals + vegetarian_meals
        else:
            meals_to_display = vegan_meals + vegetarian_meals + meat_meals

        # clear the listbox and display the suggested meals
        self.suggestion_listbox.delete(0, tk.END)
        for meal in meals_to_display:
            self.suggestion_listbox.insert(tk.END, meal)


# main application driver
if __name__ == "__main__":
    root = tk.Tk()
    app = Body(root)  # instantiate the Body class
    root.mainloop()  # start the tkinter main loop
