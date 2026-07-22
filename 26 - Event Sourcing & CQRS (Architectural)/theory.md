# Pattern 26: Event Sourcing & CQRS (Architectural)

## 🧒 The 5-Year-Old Explanation

**Normal Database (CRUD):** Imagine a bank account. You deposit $100. The bank crosses out your old balance of $0 and writes `$100`. You deposit $50. They cross out $100 and write `$150`. If you ask, "How did I get $150?", the bank says, "I don't know, that's just the number on the paper."

**Event Sourcing:** The bank doesn't write down your balance. Instead, they write down a *list of things that happened*: 
1. Opened account
2. Deposited $100
3. Deposited $50

To find your balance, they just read the list from top to bottom and add it up. If you ask, "How did I get $150?", they can prove exactly how!

**CQRS:** When you ask "What's my balance?" it takes a long time to add up that whole list. So, CQRS splits the bank in half. One half ONLY writes down the events (Event Sourcing). The other half adds up the events in the background and keeps a separate, super-fast chalkboard with just the final number `$150` for you to read.

---

## 📦 Prerequisites

**You should be comfortable with:**
- Command Pattern (Ch 14).
- Observer Pattern / PubSub (Ch 18).
- Database scaling concepts (Read Replicas).

---

## 🔍 How to Spot This Pattern

**Think of Event Sourcing/CQRS when you see:**
- You absolutely cannot lose historical data. You need a perfect audit trail of every change ever made (Finance, Healthcare).
- You want to be able to "time travel" your application to see its exact state 3 weeks ago.
- Your application has a massive imbalance between Reads (99%) and Writes (1%).

**Anti-signals:**
- You are building a simple CRUD app. Event Sourcing will increase your complexity by 10x. Do not use it unless you truly have business requirements for it.

---

## 🧩 The Core Idea

### CQRS (Command Query Responsibility Segregation)
> Segregate operations that read data (Queries) from operations that update data (Commands) by using separate interfaces, and often entirely separate databases.

### Event Sourcing
> Capture all changes to an application state as a sequence of events. Do not store the current state; instead, reconstruct it by replaying the events.

### Architecture Diagram

```mermaid
flowchart TB
    C[Client UI]
    
    subgraph "Write Side (Command)"
        Cmd[Command API]
        ES[(Event Store / Kafka)]
        Cmd -->|Save Event| ES
    end
    
    subgraph "Read Side (Query)"
        Qry[Query API]
        RDB[(Read DB / Redis)]
        Qry -->|Fetch DTO| RDB
    end
    
    ES -.->|Async Publish Event| RDB
    
    C -->|Send Command (POST)| Cmd
    C -->|Ask Query (GET)| Qry
```

---

## 🔧 Pattern Anatomy

### Participants

| Participant | Role |
|-------------|------|
| `Command` | An intent to change state (e.g., `DepositMoneyCommand(amount=50)`). It is validated before becoming an event. |
| `Event` | A fact that has already happened (e.g., `MoneyDepositedEvent(amount=50)`). Events are immutable. They cannot be changed or deleted. |
| `Event Store` | An append-only database (like Kafka or EventStoreDB) that holds the single source of truth: the stream of events. |
| `Projection` | A background worker that listens to new events in the Event Store, calculates the new state, and saves the final result to a Read Database. |
| `Read DB` | A highly optimized database (like Redis or ElasticSearch) that only answers queries. It is completely decoupled from the Event Store. |

---

## 🔄 Without Pattern → With Pattern

### Level 1: Standard CRUD (Loss of History)
```python
# BAD (for audit systems): The previous state is gone forever!
def change_address(user_id, new_address):
    user = db.query(User).get(user_id)
    user.address = new_address
    db.commit() # The old address is permanently deleted!
```

### Level 3: Event Sourcing + CQRS
```python
# GOOD: We append a fact to history. We do not UPDATE rows.
def change_address(user_id, new_address):
    # 1. Create the Event
    event = UserMovedEvent(user_id=user_id, new_address=new_address, timestamp=now())
    
    # 2. Append to Event Store (WRITE)
    event_store.append(event)
    
    # 3. A background process hears the event and updates the Read DB (CQRS)
    # read_db.update_user_address(user_id, new_address)
```

---

## ⏱️ Trade-offs

| Aspect | Assessment |
|--------|-----------|
| **Complexity** | **Extreme**. You have to deal with eventual consistency, message brokers, event versions, and complex infrastructure. |
| **Auditability** | Flawless. You have a cryptographic record of every action. |
| **Scalability** | Massive. You can scale the Read DB (Queries) completely independently from the Event Store (Commands). |
| **Performance Issue** | If a user has 10,000 events, reconstructing their state takes a long time. (Mitigated using 'Snapshots' every 100 events). |

---

## 🌍 Real-World Framework Sightings

### Git
- Git is exactly Event Sourcing! The "events" are your commits. To get the current state of your codebase (the projection), Git replays all the commits from the beginning of time.

### Apache Kafka / RabbitMQ
- These messaging systems form the backbone of modern CQRS/Event Sourced microservices.

---

## ✅ Examples in This Chapter

| # | Example | Framework | Key Concept |
|---|---------|-----------|-------------|
| 1 | Event Sourced Bank Account | Pure Python | Separating Commands and Queries, appending events to a stream, and projecting the current balance. |
