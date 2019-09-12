UPDATE public.meals set system_product=True;
UPDATE public.products set system_company=True;
create or replace view allproducts as (select *, True as system_product from products UNION select *, False as system_product from personalproducts);