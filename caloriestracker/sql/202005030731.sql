UPDATE public.products set calcium=NULL;
ALTER TABLE public.products ALTER COLUMN calcium SET default NULL;
UPDATE public.personalproducts set calcium=NULL;
ALTER TABLE public.personalproducts ALTER COLUMN calcium SET default NULL;

