
Live_url: https://sanctum-sanctorum-main-auld.onrender.com

just click create member and use

i used render for deployment 
and `neon` for the production PostgreSql database;

`reason for choice`:

render= I used Render because it provides a long-running web service that fits FastAPI's ASGI architecture and SQLAlchemy's connection pooling. Vercel uses a serverless function model, which requires additional adaptation for FastAPI. So, Render was a simpler fit for this project's architecture.

neon = I used Neon to keep the setup simple, since the project only needs a managed PostgreSQL database and a connection URL. Supabase is also a good option and provides Postgres too, but its additional backend services (auth, storage, realtime) weren't needed for this project.

SQLite connection settings: check_same_thread=False is SQLite-specific, so I made it conditional and only applied it when using SQLite.
Postgres driver: Added psycopg[binary] so SQLAlchemy can connect to PostgreSQL

github url: https://github.com/samradhi29/Sanctum-Sanctorum-main

`incremental commits on GitHub, adding a commit after each feature was completed. I also updated the progress in NOTES.md simultaneously`.

AI usage: Claude for generating some of the code and ChatGPT mainly for debugging. Instead of simply copy-pasting generated code, I reviewed each line carefully and made sure I understood the problem and the generated code.

For every AI-generated suggestion, I asked about the reason behind the implementation, compared it with the existing code, and made changes where necessary. I also compared my decisions with the `SPEC` and the TODO comments provided in the code.


`all 202 test cases are passed` also some extra added by me.

in the project, I followed proper modularity and structure by separating routes, functions, schemas, and services. I also used meaningful variable and function names instead of random abc names to improve the readability and maintainability of the project.


Below are the implementations and decisions I made while building the project, including issues I found and how i resolved them. 

__________________________________________________________________________________________________________________________________________________

1 i have pushed the initial code on github.

2.now starting with fixing book part.

in the schema.py fixed the normalized function for isbn check-
the highphe extraspace was laready build
- added - the check for last digit 

3. in services/books.py added reject a duplicate ISBN with 409 


I used Claude to help with the duplicate ISBN query.

4. Used Claude to generate the initial `update_book` function. It did not include `exclude_unset=True`, so I added it to ensure only the fields provided in the request are updated instead of unset fields being updated to `None`.

5. Implemented book filtering, sorting, and pagination, including `min_price`/`max_price` filters, sorting, and total count before pagination.

6.added patch route in app/routers/books.py for updating books.

7. after running using chatgpt for debugging
- fixed import errors



__________________________________________________________________________________________________________________________________________________
members

8. in memebers service fixed tier_at_least > to >=
9. fixed email normalization (strip+lower)
10. implmented reject an email that is already in use with 409

11. get_member_stats needs due_at returned_at and late fee_cents but it is not available yet. so i will implement it later.

12.  fixed typos.

__________________________________________________________________________________________________________________________________________________
orders

13. in ordercreate implemented reject an empty items list and the same book_id appearing twice (both 422)

__________________________________________________________________________________________________________________________________________________

14. added missing fields of Loan

Decision:
 `returned_at` can be null because the book might not be returned yet.
 `back_populates` is used to connect Member and Loan, so we can get all loans of a particular member using `member.loans`.


15. implemented loan_status in service/loans.py

16. implemented to_loan_out() use of this function is to convert the DB loan object into the API LoanOut object and calculate the current status before sending the response.

17. implemented calculate_late_fee

18. implemented `create_loan` Validated all borrowing conditions, then created the loan and decreased stock.

19. implemented get_loan

20. implemented return_loan

21. Implemented `list_member_loans`: gets all loans of the member and optionally filters by status.
__________________________________________________________________________________________________________________________________________________


22. Implemented `get_member_stats` to summarize a member's orders, spending, loans, overdue books, and late fees.

Implemented  after implementing loans because it depends on loan data.

_________________________________________________________________________________________________________________________________________________

23. missed some implementations of order realised after runing tests

24. implemented calculate_discount_percent

25. Implemented `create_order` with stock validation, discount calculation, and order creation.

26. Fixed `cancel_order` by adding stock restoration when an order is cancelled.

__________________________________________________________________________________________________________________________________________________

report

27. Implemented top_books to return the best-selling books based on paid orders.

__________________________________________________________________________________________________________________________________________________

28. Debug:
Return button was not working because the `loan-return` action was missing from the action handler. 
Added the action and called `returnLoan(id, target)`, resolving the issue.


29. Added `psycopg[binary]` as the only dependency exception because it is required to connect SQLAlchemy to Postgres for deployment; no new dependencies were added for business logic.

30. Made `check_same_thread=False` conditional on SQLite because this option is SQLite-specific and can cause connection issues when using PostgreSQL in production.


________________________________________________________________________________________________________________________________________________
completed the delopyment using render and neon

________________________________________________________________________________________________________________________________________________

extra part

1. A `GET /members` endpoint with pagination

Added GET /members with limit and offset pagination. Implemented a MemberPage response schema, a list_members() service with COUNT(*) for the total and a paginated query ordered by id, and a router endpoint with validation for limit and offset


2. Handle concurrent orders for the last copy of a book safely

To solve the concurrent access problem, which is essentially a race condition, I used SQLAlchemy's `with_for_update()` in both create_order and create_loan. It locks only the specific book row while the transaction is in progress, preventing another request from modifying the same book simultaneously.

This row-level locking is supported by PostgreSQL. SQLite does not support row-level locking and uses broader database-level locking for writes which is less efficient for this use case.


3. added some extra test cases in the extra_edge_case file

Mixed restricted items: Added to verify that one unauthorized restricted book blocks the entire order and does not change stock.
Search wildcard escaping: Added to ensure % in search queries is treated as a literal character, not a SQL wildcard.
Empty PATCH body: Added to verify that an empty update request does not modify the book.
Member pagination: Added to ensure total represents all members, not only the members in the current page.
Cancel order stock restore: Added to verify that cancelling an order restores exactly the quantity that was deducted.

_________________________________________________________________________________________________________________________________________

what i skipped:
No frontend UI for the new `GET /members` pagination endpoint — it's
implemented and tested at the API level, but not wired into the existing UI.

