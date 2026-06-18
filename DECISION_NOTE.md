## Architectural Decision Note

**Decision:** Opting for a Stateless API Architecture over a Database Backend.

In approaching the "DevHabit Tracker" challenge, the most critical decision was choosing not to implement a persistent database layer (like PostgreSQL or SQLite). Instead, the system operates as a stateless API. It receives the complete payload of user activity, calculates the metrics synchronously, pulls the LLM insight, and returns the aggregated data immediately.

**Trade-offs:**
The primary trade-off is the inability to track user behavior over long periods or across multiple sessions without the client retaining and sending the historical data. However, for a 24-hour MVP, this sacrifice was intentional to prioritize reviewer experience. By keeping the API stateless, the application avoids complex database migrations, schema setups, and container networking issues. A reviewer can reliably clone the repository and run `docker-compose up` without needing to configure external database keys or ensure a local database service connects properly to the web container. This guarantees the core requirements—combining rule-based logic with an LLM in a functional endpoint—are easily verifiable.
