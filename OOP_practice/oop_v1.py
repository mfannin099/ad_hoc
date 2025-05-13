class Employee:
    employee_count = 0
    cost_of_living_adjustment = .03
    tenure = 0

    def __init__(self,name,age,title,salary):
        self.name = name
        self.age = age
        self.title = title
        self.salary = salary
        Employee.employee_count += 1

    @classmethod # Counts the number of employees 
    def get_employee_count(cls):
        return cls.employee_count
    
    def __str__(self):
        return f"Employee Description - Name: {self.name}, Age: {self.age}, Title: {self.title} , Salary: {self.salary}, Tenure: {Employee.tenure}"
    
    def get_raise(self,amount=None):
        if amount is None:
            self.salary += self.salary * Employee.cost_of_living_adjustment
        else:
            self.salary += amount

    def change_position(self,new_title):
        self.title = new_title
    
    def year_of_tenure(self):
        Employee.tenure = Employee.tenure + 1




## init employee
employee1 = Employee("bob", 22, "analyst",10000)
print(employee1)

employee1.get_raise()
employee1.year_of_tenure()
print(employee1)

employee1.get_raise()
employee1.year_of_tenure()
print(employee1)

## After Promotion/Raise
employee1.change_position("data scientist")
employee1.get_raise(1000)
print(employee1)





# print("Total employees:", Employee.get_employee_count())