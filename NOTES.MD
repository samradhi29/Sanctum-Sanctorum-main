i am using free claude and chatgpt help to complete the assesment
list of task i am doing to complete the assesment

1 i have pushed the initial code on github.

2.now starting with fixing book part.

in the schema.py fixed the normalized function for isbn check-
the highphe extraspace was laready build
- added - the check for last digit 

3. in services/books.py added reject a duplicate ISBN with 409 
## AI usage

I used Claude to help with the duplicate ISBN query.

4. Used Claude to generate the initial `update_book` function. It did not include `exclude_unset=True`, so I added it to ensure only the fields provided in the request are updated instead of unset fields being updated to `None`.

5. Implemented book filtering, sorting, and pagination, including `min_price`/`max_price` filters, sorting, and total count before pagination.

6.added patch route in app/routers/books.py for updating books.

7. after running using chatgpt for debugging
- fixed import errors


____________________________________________________
members

8. in memebers service fixed tier_at_least > to >=
9. fixed email normalization (strip+lower)
10. implmented reject an email that is already in use with 409

11. get_member_stats needs due_at returned_at and late fee_cents but it is not available yet. so i will implement it later.

12.  fixed typos.

___________________________________________________
orders

13. in ordercreate implemented reject an empty items list and the same book_id appearing twice (both 422)