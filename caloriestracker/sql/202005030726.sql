--  Adds calcium to products
ALTER TABLE public.products ADD COLUMN calcium NUMERIC(10,2) DEFAULT 0;
ALTER TABLE public.personalproducts ADD COLUMN calcium NUMERIC(10,2) DEFAULT 0;

