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

