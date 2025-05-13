from datetime import datetime

class Employee:
    cost_of_living_adjustment = 0.03  # Still OK as class variable

    def __init__(self, name, age, title, salary, start_year):
        self.name = name
        self.age = age
        self.title = title
        self.title_l = [self.title]

        self.salary = salary
        self.salary_l = [self.salary]

        self.start_year = start_year
        self.tenure = 0
        self.tenure_l = [self.tenure]

    def __str__(self):
        return f"Employee Description - Name: {self.name}, Age: {self.age}, Title: {self.title}, Salary: {self.salary}, Start Year: {self.start_year}, Tenure: {self.tenure}"

    def get_raise(self, amount=None):
        if amount is None:
            self.salary += self.salary * Employee.cost_of_living_adjustment
        else:
            self.salary += amount
        self.salary_l.append(round(self.salary,2))

    def change_position(self, new_title):
        self.title = new_title
        self.title_l.append(new_title)

    def year_of_tenure(self):
        self.tenure += 1
        self.tenure_l.append(self.tenure)


class Career():
    def __init__(self,employee):
        self.employee = employee
        self.promotions = employee.title_l
        self.salary_history = employee.salary_l
        self.tenure_history = employee.tenure_l

    def review_progress(self):
        print(f"Career Path for {self.employee.name}")
        print(f"Start Title: {self.promotions[0]}")
        print(f"Current Title: {self.promotions[-1]}")
        print(f"Title Progression: {self.promotions}")
        print(f"Years of Tenure: {self.tenure_history}")
        print(f"Salary History: {self.salary_history}")



def simulate_year(employee, raise_amount=None):
    employee.get_raise(raise_amount)
    employee.year_of_tenure()



## init employee
employee1 = Employee("bob", 22, "analyst",100000, 2017)
career1 = Career(employee1)
print(employee1)

simulate_year(employee1)
simulate_year(employee1)

## After Promotion/Raise
employee1.change_position("senior analyst")
simulate_year(employee1, 10000)

simulate_year(employee1)
simulate_year(employee1)
simulate_year(employee1)
simulate_year(employee1)

## After Promotion/Raise
employee1.change_position("data scientist")
simulate_year(employee1, 25000)

simulate_year(employee1)
simulate_year(employee1, 15000)
employee1.change_position("senior data scientist")





career1.review_progress()



