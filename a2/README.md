# Assignment 2 - Conceptual Data Modelling Assignment

## Grade Received

## Errors
The only issue I know of is that my program fails to combine the attributes of weak relation into an entity set, and instead fails to account for the attributes whatsoever.

## Test Cases
The test cases used for grading are available in `tests.py`.

Test cases 15 and 17 failed, all others passed.

## Given Assignment Description

### Assignment Goals

In this assignment you will:

  * demonstrate knowledge of conceptual data modeling and the SQL DDL

    + convert entity-relationship diagrams into a logical model
    + implement a model in a relational database with SQL

### Task

You should write a computer program in the programming language of your choice that will take as input an entity-relationship diagram (ERD) and prints out to the standard output stream a series of SQL DDL queries (i.e., CREATE TABLE statements) that populates an empty MySQL database with a set of tables that match the ERD.

You have been provided with an ERD class that can be directly instantiated, even for complex examples like the one shown below. You are also provided with a Database class that has methods for comparing two databases for equality and for printing out CREATE TABLE statements. There is only one function missing, the one that you should implement, which converts an arbitrary ERD instance into a corresponding Database instance.

You will need to handle all concepts introduced in the lessons (e.g., weak entity sets, subclass hierarchies, many-many relationships), but you should assume that every one-many and many-one relationship requires referential integrity. You should not modify any identifiers. For simplicity, we have made every attribute of data type INT and avoided use of specifiers like "AUTOINCREMENT" and NOT NULL.

You _do not need to write any scripts_ for this assignment. We have instead wrapped all the code in a unit testing framework and we will directly probe the objects that you create by creating mock objects as solutions and using the provided equality comparator to determine whether you have the same solution. Where order is not important as per the SQL standard, we use set-based comparisons; where it is important, we check order. You can verify this by inspecting the comparators.

### Submission

If coding in Python, you should only submit one .py file, uncompressed, which implements the convert_to_table() function with the exact signature provided. If coding in C++, you should submit up to two files (one .cpp implementation file and one corresponding .hpp header file) that together implement the convert_to_table() function.

### Evaluation

We will swap out the test file with a new set of unit tests and assign a grade of pass (1) or fail (0) for each assertion that you pass. If your code takes more than five minutes on a single test, it may be terminated before the test finishes, resulting in a fail on that test. Your grade on the assignment will be the number of tests passed. There will be a total of twenty-two tests, each worth 5%; so, it is possible to score a maximum grade of 110% on this assignment.

### Sources

You are permitted to use sources that you find on the Internet, so long as it is clear that the source existed prior to the creation of this assignment and you provide a citation in your source code. For example, GitHub and StackOverflow content is permitted, so long as they are clearly dated prior to the beginning of this semester. If you do not include a citation in your source code, your work will be considered plagiarism.

You should, however, work through the assignment on your own. You are welcome to prepare for the assignment with peers in the class by working through the ungraded worksheets together.