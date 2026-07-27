## 🐍 Object-Oriented Programming (OOP) with Python

Welcome to my personal learning journey repository! This space serves as my digital notebook, interactive playground, and comprehensive guide to mastering Object-Oriented Programming (OOP) in Python.
Inspired by professional interview-prep repositories and built using a structured learning path, this project documents my transition from procedural coding to building scalable, clean, and maintainable object-oriented software.

------------------------------
## 🗺️ My Learning Roadmap
This repository follows a strict, step-by-step curriculum designed to build deep foundational knowledge before moving into advanced Python internals.

[Level 1: Fundamentals] ──> [Level 2: The Four Pillars] ──> [Level 3: Python Magic & Internals]

## 🔹 Level 1: Core Foundations
Before diving into complex architectures, I mastered the fundamental building blocks of classes:

* Classes vs. Instances: Understanding the blueprint vs. the actual object.
* Attributes: Differentiating between Class Attributes (shared by all instances) and Instance Attributes (unique to each object).
* Methods: Implementing instance methods and understanding the explicit self argument.

## 🔹 Level 2: The 4 Pillars of OOP
The core of object-oriented design patterns:

   1. Encapsulation: Using public, protected (_), and private (__) attributes to hide internal data and restrict direct modification.
   2. Inheritance: Reusing code by creating child classes from parent classes, reducing redundancy.
   3. Polymorphism: Writing flexible code where different classes can implement the same method interface in unique ways.
   4. Abstraction: Using the abc module to define blueprint classes (Abstract Base Classes) that enforce specific method implementations in subclasses.

## 🔹 Level 3: Advanced Python & Under-The-Hood Internals
Moving past the basics to understand how Python handles objects dynamically:

* Multiple Inheritance & MRO: Mastering how Python resolves method calls in complex inheritance trees using Method Resolution Order (MRO) and super().
* Dunder (Magic) Methods: Overloading operators and customizing object behaviors using methods like __init__, __str__, __repr__, __len__, and __call__.
* Property Decorators: Transforming methods into attributes using @property, @getter, and @setter for clean data validation.

------------------------------
## 💻 Code Examples & Concept Explanations
Here is a look at how I structure my code and explanations inside this repository:
## 1. Data Encapsulation & Validation
Using getters and setters to protect internal state:

class BankAccount:
    def __init__(self, owner, balance):
        self.owner = owner
        self.__balance = balance  # Private attribute

    @property
    def balance(self):
        """Getter: Safely exposes the private balance."""
        return self.__balance

    @balance.setter
    def balance(self, amount):
        """Setter: Validates data before altering the balance."""
        if amount < 0:
            raise ValueError("Balance cannot be negative!")
        self.__balance = amount
# Working Exampleaccount = BankAccount("Alice", 1000)
account.balance = 1500  # Works perfectly# account.balance = -500 # Raises ValueError

## 2. Polymorphism in Action
Allowing different objects to respond to the same method call:

class SQLiteDatabase:
    def connect(self):
        return "Connected to SQLite local database."
class PostgreSQLDatabase:
    def connect(self):
        return "Connected to cloud PostgreSQL production database."
def initialize_system(db_object):
    """This function doesn't care what DB type it receives, as long as it has a .connect() method."""
    print(db_object.connect())
# Both work seamlessly despite being different classes
initialize_system(SQLiteDatabase())
initialize_system(PostgreSQLDatabase())

------------------------------
## 🛠️ Project Structure

📦 oop-with-python
 ┣ 📂 01_foundations/         # Classes, objects, self, __init__
 ┣ 📂 02_four_pillars/        # Encapsulation, Inheritance, Polymorphism, Abstraction
 ┣ 📂 03_advanced_oop/        # MRO, Multiple Inheritance, Abstract Base Classes
 ┣ 📂 04_magic_methods/       # Dunder methods (__str__, __repr__, etc.)
 ┣ 📂 05_real_world_exercises/# Practical mini-projects and interview prep
 ┗ 📜 README.md               # You are here!

------------------------------
## 🎯 Key Takeaways & Code Philosophy

* Composition over Inheritance: favor combining objects over deep, messy inheritance trees where possible.
* Don't Repeat Yourself (DRY): Use objects and base structures to maximize code reusability.
* Readability Counts: Document code with clear docstrings, clear class intentions, and robust type hinting.

