--  Add a new food type. obsolete field
INSERT INTO public.foodtypes(id,name) VALUES (19, 'Homemade food');

ALTER TABLE public.products ADD COLUMN obsolete boolean default false NOT NULL;
ALTER TABLE public.personalproducts ADD COLUMN obsolete boolean default false NOT NULL;
ALTER TABLE public.elaboratedproducts ADD COLUMN obsolete boolean default false NOT NULL;
ALTER TABLE public.companies ADD COLUMN obsolete boolean default false NOT NULL;
ALTER TABLE public.personalcompanies ADD COLUMN obsolete boolean default false NOT NULL;

ALTER TABLE public.products ADD COLUMN ferrum NUMERIC(10,2);
ALTER TABLE public.products ADD COLUMN magnesium NUMERIC(10,2);
ALTER TABLE public.products ADD COLUMN phospor NUMERIC(10,2);
ALTER TABLE public.products ADD COLUMN glutenfree boolean;
ALTER TABLE public.products ALTER COLUMN amount SET default 100;
ALTER TABLE public.products ALTER COLUMN amount SET NOT NULL;
ALTER TABLE public.products ALTER COLUMN name SET NOT NULL;

ALTER TABLE public.personalproducts ADD COLUMN ferrum NUMERIC(10,2);
ALTER TABLE public.personalproducts ADD COLUMN magnesium NUMERIC(10,2);
ALTER TABLE public.personalproducts ADD COLUMN phospor NUMERIC(10,2);
ALTER TABLE public.personalproducts ADD COLUMN glutenfree boolean;
ALTER TABLE public.personalproducts ALTER COLUMN amount SET default 100;
ALTER TABLE public.personalproducts ALTER COLUMN amount SET NOT NULL;
ALTER TABLE public.personalproducts ALTER COLUMN name SET NOT NULL;

