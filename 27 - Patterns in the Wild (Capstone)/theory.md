# Capstone: Patterns in the Wild

## 🧒 The 5-Year-Old Explanation

You've learned 26 different tools. A hammer, a screwdriver, a saw...
But when you build a real house, you don't just use a hammer. You use all the tools together!

In the real world, Design Patterns don't live in isolation. They **combine** to form massive architectures.

---

## 🏗️ How Frameworks Combine Patterns

If you want to master Software Architecture, you must learn to see how these patterns intertwine. Let's look at a few examples:

### 1. Django (Python Web Framework)

Django is a massive combination of patterns working in harmony:

- **Template Method**: Django's Class-Based Views (`View`, `ListView`, `DetailView`) use the Template Method to define the skeleton of an HTTP request, letting you override `get()`, `post()`, or `get_context_data()`.
- **Observer (PubSub)**: Django Signals (`post_save`, `pre_delete`) allow completely decoupled components to react when database models change.
- **Active Record**: (A variation of Repository/Data Mapper). `User.objects.get(id=1)` binds the data and the database access into a single Model class.
- **Middleware / Chain of Responsibility**: Every HTTP Request passes through a chain of Middleware (Authentication, CSRF, Sessions) before hitting your view.

### 2. SQLAlchemy (Python ORM)

- **Unit of Work**: The `Session` object. It tracks all changes to your objects and commits them atomically.
- **Identity Map**: (Related to Flyweight/Singleton). If you query `User(id=1)` twice in the same session, SQLAlchemy returns the *exact same object in memory*.
- **Iterator**: `ResultProxy` batches database results instead of loading millions of rows into RAM.

### 3. FastAPI (Python API Framework)

- **Dependency Injection**: FastAPI's core routing engine is a massive DI Container. You declare `db: Session = Depends(get_db)`, and the framework builds and injects it for you.
- **Decorator**: You register routes using `@app.get("/")`, adding routing behavior to your raw functions.

---

## ⚠️ The Danger Zone: Patternitis

The biggest mistake junior and mid-level developers make is **Patternitis** (or "Golden Hammer Syndrome").

> "When you have a shiny new hammer, everything looks like a nail."

### How to avoid Patternitis:
1. **YAGNI (You Aren't Gonna Need It)**: Do not implement a pattern because you *might* need it next year. Implement it when the pain of *not* having it becomes unbearable today.
2. **KISS (Keep It Simple, Stupid)**: A simple function is almost always better than a 5-class Strategy pattern. Only upgrade to the Strategy pattern when the simple function becomes a 200-line `if/elif` nightmare.
3. **Listen to the Language**: Python is not Java. Python has first-class functions, decorators, and metaclasses. Often, a GoF pattern that takes 4 classes in Java takes 1 line of Python. Don't write Java in Python.

---

## 🎓 Conclusion

Design Patterns are not rules. They are a **Shared Vocabulary**.

When you say, "I implemented a *Factory* that returns a *Strategy*," another engineer immediately understands the entire architecture of your code without reading a single line.

Use them wisely, use them sparingly, and happy coding! 🚀
