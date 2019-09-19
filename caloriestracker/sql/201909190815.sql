alter table public.formats drop constraint products_formats_fk;
update public.products set companies_id=1, system_company=True where id=77;