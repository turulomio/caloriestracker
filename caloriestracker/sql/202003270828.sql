--  Add a new food type. obsolete field
UPDATE public.products SET glutenfree=False WHERE glutenfree IS NULL;
UPDATE public.personalproducts SET glutenfree=False WHERE glutenfree IS NULL;
UPDATE public.elaboratedproducts SET glutenfree=False WHERE glutenfree IS NULL;
ALTER TABLE public.products ALTER COLUMN glutenfree SET default False;
ALTER TABLE public.personalproducts ALTER COLUMN glutenfree SET default False;
ALTER TABLE public.elaboratedproducts ALTER COLUMN glutenfree SET default False;
ALTER TABLE public.products ALTER COLUMN glutenfree SET NOT NULL;
ALTER TABLE public.personalproducts ALTER COLUMN glutenfree SET NOT NULL;
ALTER TABLE public.elaboratedproducts ALTER COLUMN glutenfree SET NOT NULL;


