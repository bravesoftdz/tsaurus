# Python OOP Primer

# main class
class Employee:
    #class variable
    raise_amount = 1.4
    num_of_emps = 0

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.pay = pay
        self.email = first + '.' + last + '@emaildomain.com'

        Employee.num_of_emps += 1

    @classmethod
    def from_string(cls, emp_string):
        first, last, pay = emp_string.split('-')
        return cls(first, last, pay)

    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True

    def fullname(self):
        return '{} {}'.format(self.first, self.last)

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)


# subclass
class Developer(Employee):
    def __init__(self, first, last, pay, prog):
        super().__init__(first, last, pay)
        self.prog = prog


# subclass
class Manager(Employee):
    def __init__(self, first, last, pay, employees=None):
        super().__init__(first,last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emps(self):
        if self.employees is not None:
            for emp in self.employees:
                print('--->', emp.fullname())





emp1 = Employee('Dina', 'Basumatary', 450)
print(emp1.__dict__)
print(Employee.num_of_emps)

emp2 = Employee('Foo', 'Bar', 333)
emp3 = Employee.from_string('Roman-Empire-452')

d1 = Developer('Dev1', 'Last', 2233, 'Python')
d2 = Developer('Dev2', 'Last', 2231, 'Java')

mgr1 = Manager('Marco', 'T', 2333)
mgr1.add_emp(d1)
mgr1.add_emp(d2)

mgr2 = Manager('Jarrod', 'Plant', 5555, [mgr1, d1, d2, emp1])

print(emp2.__dict__)
print(emp3.__dict__)
print(Employee.num_of_emps)
print(Employee.__dict__)

import datetime
my_date = datetime.date(2017, 12, 13)

print(Employee.is_workday(my_date))
