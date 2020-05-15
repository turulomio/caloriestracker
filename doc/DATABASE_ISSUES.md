# Database Issues

To debug problems with caloriestracker you must call `caloriestracker --debug DEBUG` and try to fix with the following issues

If you can't resolve problem, please fill an issue in Github

## ERROR psycopg2.errors.UndefinedColumn: column "global" does not exist LINE 1: select value from public.globals where global='Version'

If you get this error you must open a psql session and write the following commands

`ALTER TABLE public.globals RENAME COLUMN name TO global;`

`ALTER TABLE public.globals DROP COLUMN id;`

`ALTER TABLE public.globals ADD PRIMARY KEY (global);`

`UPDATE public.globals SET global='Version' WHERE global='Database version';`

For your information the last sql it work before this bug was 202004061139.sql
