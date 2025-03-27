# Basic SQL Syntax

CRUD stands for **Create, Read, Update, Delete**—the four basic operations you perform on a database. Below are the typical SQL syntax examples and explanations for each operation.

---

## 1. CREATE

### A. Creating Tables (DDL – Data Definition Language)

You can define your database schema by creating tables:

```sql
CREATE TABLE employees (
    id INT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    department VARCHAR(50)
);
```

### B. Inserting Data (DML – Data Manipulation Language)

To add records to a table, use the `INSERT` statement:

```sql
INSERT INTO employees (id, name, age, department)
VALUES (1, 'Alice', 30, 'Sales');
```

You can also insert multiple rows at once:

```sql
INSERT INTO employees (id, name, age, department)
VALUES
    (2, 'Bob', 25, 'Marketing'),
    (3, 'Charlie', 28, 'HR');
```

---

## 2. READ (SELECT)

The `SELECT` statement is used to retrieve data from one or more tables.

### Basic SELECT Syntax

```sql
SELECT column1, column2, ...
FROM table_name;
```

Example – selecting all columns:

```sql
SELECT * FROM employees;
```

### Adding Conditions

Use the `WHERE` clause to filter results:

```sql
SELECT id, name, age
FROM employees
WHERE department = 'Sales';
```

### Sorting Results

Order results with `ORDER BY`:

```sql
SELECT id, name, age
FROM employees
WHERE department = 'Sales'
ORDER BY age DESC;
```

### Grouping Data

Aggregate rows using `GROUP BY` and functions like `SUM()`, `AVG()`, etc.:

```sql
SELECT department, COUNT(*) AS num_employees
FROM employees
GROUP BY department;
```

---

## 3. UPDATE

To modify existing records, use the `UPDATE` statement along with `WHERE` to target specific rows.

### Basic UPDATE Syntax

```sql
UPDATE employees
SET age = 31
WHERE id = 1;
```

### Updating Multiple Columns

```sql
UPDATE employees
SET age = 32, department = 'Business Development'
WHERE name = 'Alice';
```

---

## 4. DELETE

The `DELETE` statement removes records from a table. Use the `WHERE` clause to avoid deleting all rows.

### Basic DELETE Syntax

```sql
DELETE FROM employees
WHERE id = 1;
```

### Delete All Rows

To delete all records (be cautious!):

```sql
DELETE FROM employees;
```

---

## Summary

- **Create:**

  - **DDL:** `CREATE TABLE` to define a table.
  - **DML:** `INSERT INTO` to add data.

- **Read:**

  - Use `SELECT` with optional `WHERE`, `ORDER BY`, and `GROUP BY` clauses to retrieve data.

- **Update:**

  - Use `UPDATE` with `SET` to modify existing records, using `WHERE` to limit the update.

- **Delete:**
  - Use `DELETE` with `WHERE` to remove specific rows, or without `WHERE` to remove all rows.

Each of these operations forms the backbone of working with relational databases in SQL.

# GROUP BY Deep Dive

It is used to group rows that have the same values in one or more columns so that aggregate functions (like `SUM()`, `COUNT()`, `AVG()`, etc.) can be applied to each group.

---

## How GROUP BY Works

Imagine you have a table that records sales transactions. Each row in this table might represent an individual sale, and you want to know total sales for each salesperson. Instead of processing each row individually, you can group all rows for a given salesperson and then apply an aggregate function to compute a summary (such as the total amount of sales).

---

## The Basic Syntax

```sql
SELECT column1, column2, ..., aggregate_function(column)
FROM table_name
WHERE condition
GROUP BY column1, column2, ...;
```

- **`SELECT` Clause:**  
  Contains both the columns you want to group by and the aggregate functions you want to compute.
- **`FROM` Clause:**  
  Specifies the table.
- **`WHERE` Clause:**  
  Filters rows before grouping (optional).
- **`GROUP BY` Clause:**  
  Lists the columns by which the rows will be grouped.
- **`HAVING` Clause:**  
  (Optional) Filters groups after the aggregation is done.

---

## Visual Example

Let's use a visual example with a sample table called `sales`:

### Sample Table: `sales`

| id  | salesperson | region | amount |
| --- | ----------- | ------ | ------ |
| 1   | Alice       | North  | 150    |
| 2   | Alice       | North  | 200    |
| 3   | Bob         | South  | 300    |
| 4   | Charlie     | East   | 250    |
| 5   | Charlie     | East   | 100    |
| 6   | Diana       | West   | 350    |
| 7   | Diana       | West   | 400    |
| 8   | Ethan       | North  | 500    |
| 9   | Ethan       | North  | 600    |
| 10  | Ethan       | North  | 700    |

### What Do We Want to Find Out?

Suppose you want to know:

- The **total sales amount** for each salesperson.
- The **number of sales** each salesperson made.

---

## Writing the Query

We can use aggregate functions and group by the `salesperson` column:

```sql
SELECT
    salesperson,
    COUNT(*) AS num_sales,
    SUM(amount) AS total_sales
FROM sales
GROUP BY salesperson;
```

When you use a `GROUP BY` clause, here's what happens logically:

1. **FROM/WHERE:**  
   The database first selects rows from the table (and applies any filtering in the `WHERE` clause).

2. **GROUP BY:**  
   The rows are then grouped based on the columns specified in the `GROUP BY` clause. Essentially, all rows with the same values in those columns are put together into a single group.

3. **SELECT & Aggregation:**  
   Next, the `SELECT` clause is applied to each group. Aggregate functions (like `SUM()`, `COUNT()`, etc.) compute values for each group, and any columns that aren’t aggregated must be part of the `GROUP BY`.

4. **HAVING/ORDER BY (if present):**  
   Finally, the query can filter groups (using `HAVING`) or order the results.

So yes, you can think of it as: the engine groups the data first, then the `SELECT` (and any aggregate functions) are applied to each of these groups to produce the final result.

### How It Works Step-by-Step

1. **Row Grouping:**  
   The `GROUP BY salesperson` tells the database to collect all rows with the same `salesperson` value together.

   - **Group for Alice:**  
     Rows with id 1 and 2 are grouped.
   - **Group for Bob:**  
     Only the row with id 3 is in Bob’s group.
   - **Group for Charlie:**  
     Rows with id 4 and 5 are grouped.
   - **Group for Diana:**  
     Rows with id 6 and 7 are grouped.
   - **Group for Ethan:**  
     Rows with id 8, 9, and 10 are grouped.

2. **Applying Aggregates:**
   - `COUNT(*)` counts the number of rows (sales) in each group.
   - `SUM(amount)` calculates the total sales amount for each group.
3. **Result:**  
   The query returns one row per salesperson with the number of sales and the total sales amount.

---

### Expected Output

Based on our sample data:

| salesperson | num_sales | total_sales |
| ----------- | --------- | ----------- |
| Alice       | 2         | 350         |
| Bob         | 1         | 300         |
| Charlie     | 2         | 350         |
| Diana       | 2         | 750         |
| Ethan       | 3         | 1800        |

---

## Advanced: Using the HAVING Clause

You can filter groups after they are aggregated using the `HAVING` clause. For example, if you only want salespeople with total sales greater than 500, you could write:

```sql
SELECT
    salesperson,
    COUNT(*) AS num_sales,
    SUM(amount) AS total_sales
FROM sales
GROUP BY salesperson
HAVING SUM(amount) > 500;
```

This would return only the groups (salespeople) whose total sales exceed 500.

---

## Implementing GROUP BY with SQLAlchemy Core

Here's how you can translate the above SQL into SQLAlchemy Core:

```python
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, select, func

# Create an engine and metadata object
engine = create_engine("sqlite:///sales.db", echo=True)
meta = MetaData()

# Define the sales table
sales = Table(
    "sales",
    meta,
    Column("id", Integer, primary_key=True),
    Column("salesperson", String, nullable=False),
    Column("region", String, nullable=False),
    Column("amount", Float, nullable=False)
)

# Create the table (if it doesn't exist)
meta.create_all(engine)

# Build the query
stmt = select(
    sales.c.salesperson,
    func.count().label("num_sales"),
    func.sum(sales.c.amount).label("total_sales")
).group_by(sales.c.salesperson)

# Execute the query and print the result
with engine.connect() as conn:
    result = conn.execute(stmt)
    for row in result:
        print(f"Salesperson: {row.salesperson}, Number of Sales: {row.num_sales}, Total Sales: {row.total_sales}")
```

### Explanation of the SQLAlchemy Query

- **`select(...)`**:  
  We specify the columns we want in our output.
- **`func.count().label("num_sales")`**:  
  Uses the aggregate `COUNT` function and labels the output column as `num_sales`.
- **`func.sum(sales.c.amount).label("total_sales")`**:  
  Uses the `SUM` function to add up the `amount` for each group.
- **`.group_by(sales.c.salesperson)`**:  
  Groups the rows by the `salesperson` column.

---

## Recap

- **`GROUP BY`** is used to aggregate rows that share common values.
- **Aggregate functions** like `COUNT()` and `SUM()` operate on each group.
- The **HAVING clause** can filter groups after aggregation.
- The example provided shows how to calculate the number of sales and the total sales amount per salesperson, both in raw SQL and in SQLAlchemy Core.

This detailed example should give you a clear understanding of the `GROUP BY` clause and how to use it effectively.
