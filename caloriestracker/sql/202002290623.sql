--  Removed elaboratedproduct_id from products
UPDATE public.products set elaboratedproducts_id=null where id= 78;

