# Pattern 25: Dependency Injection (Architectural)

## 🧒 The 5-Year-Old Explanation

Imagine you are a race car driver. You know how to steer, brake, and accelerate. 
But you don't build the engine yourself before you drive. You don't build the tires yourself.

The mechanic team builds the engine, puts on the tires, and then **gives (injects)** the finished car to you.

In code, **Dependency Injection (DI)** means an object should not create its own tools (dependencies). It should be *given* those tools from the outside.

---

## 📦 Prerequisites

**You should be comfortable with:**
- Object instantiation vs Interface implementation.
- The `SOLID` principles, specifically **Dependency Inversion Principle (DIP)**.
- Type hinting (`Protocol` / `ABC`).

---

## 🔍 How to Spot This Pattern

**Think of Dependency Injection when you see:**
- You are hardcoding `Database()` or `EmailClient()` directly inside your class's `__init__` method.
- You want to write unit tests, but your class is connecting to a real production database because you can't easily swap out the connection.
- You see massive configuration blocks scattered across multiple files.

**Anti-signals:**
- The dependency is a built-in Python primitive (like `dict` or `list`), or a simple dataclass that has no side effects (like `User(name="Bob")`). You don't need to inject DTOs or Value Objects.

---

## 🧩 The Core Idea

### Intent
> Separate the creation of a client's dependencies from its own behavior. This allows the program design to be loosely coupled and to follow the Dependency Inversion and Single Responsibility principles.

### The Dependency Inversion Principle (DIP)

1. High-level modules should not import anything from low-level modules. Both should depend on abstractions (e.g., interfaces).
2. Abstractions should not depend on details. Details (concrete implementations) should depend on abstractions.

### Types of Injection

1. **Constructor Injection** (Most Common & Recommended): Dependencies are passed into the `__init__` method.
2. **Method Injection**: Dependencies are passed into a specific method when called (e.g., `def calculate(self, tax_strategy):`).
3. **Property/Setter Injection**: Dependencies are set via a property (e.g., `obj.logger = MyLogger()`). (Less common, prone to errors if the object is used before the setter is called).

---

## 🔄 Without Pattern → With Pattern

### Level 1: Hardcoded Dependencies (Tight Coupling)
```python
# BAD: The OrderService creates its own dependencies. 
# It is permanently glued to Stripe and Postgres. You cannot unit test this.
class OrderService:
    def __init__(self):
        self.payment = StripeAPI()
        self.db = PostgresDB()
        
    def checkout(self, amount):
        self.payment.charge(amount)
        self.db.save("order")
```

### Level 3: Constructor Injection (Loose Coupling)
```python
# GOOD: OrderService doesn't care HOW things are built. It just uses them.
class OrderService:
    def __init__(self, payment: PaymentProtocol, db: DBProtocol):
        self.payment = payment
        self.db = db
        
# The "Mechanic" (or DI Container) wires everything together outside:
test_payment = MockPayment()
test_db = InMemoryDB()
service = OrderService(test_payment, test_db) # Fully testable!
```

---

## 🏗️ DI Containers (Inversion of Control)

In large applications, passing 20 dependencies down a chain of 10 objects becomes a nightmare (this is called **Dependency Hell**). 

A **DI Container** (or IoC Container) solves this. You tell the container:
- "Whenever someone asks for a `PaymentProtocol`, give them a `StripeAPI`."
- "Whenever someone asks for a `DBProtocol`, give them a `PostgresDB`."

Then, you just ask the container for an `OrderService`, and it magically builds the `StripeAPI`, builds the `PostgresDB`, passes them into the `OrderService`, and hands you the finished object!

---

## ⏱️ Trade-offs

| Aspect | Assessment |
|--------|-----------|
| **Complexity** | Low for manual injection. High if building/using complex IoC containers. |
| **SOLID** | **DIP** (High level modules depend on abstractions), **SRP** (Object creation is separated from business logic). |
| **Testability** | **Extremely High**. This is the primary mechanism that enables modern unit testing (Mocking). |

---

## 🌍 Real-World Framework Sightings

### FastAPI
- FastAPI has a built-in Dependency Injection system! Whenever you write `def get_user(db: Session = Depends(get_db)):`, you are using FastAPI's DI container. It handles creating the database session and passing it to your function.

### Pytest
- Pytest `fixtures` are a form of Dependency Injection. You define a fixture, and then you just put its name in your test function signature, and Pytest injects it for you!

---

## ✅ Examples in This Chapter

| # | Example | Framework | Key Concept |
|---|---------|-----------|-------------|
| 1 | Manual Dependency Injection | Pure Python | Demonstrating Constructor Injection and writing testable code. |
| 2 | Mini DI Container | Pure Python | Building a simple IoC Container to automate object wiring. |
