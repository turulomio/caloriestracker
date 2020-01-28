-- Adding two more additiverisks
INSERT INTO public.additiverisks (id, name) VALUES (0, 'No risk');
INSERT INTO public.additiverisks (id, name) VALUES (-1, 'Not evaluated');
UPDATE public.additives set additiverisks_id=-1 where additiverisks_id is null;
ALTER TABLE public.products ALTER COLUMN additives SET DEFAULT '{}';
UPDATE public.products SET additives='{}' WHERE additives IS NULL;
ALTER TABLE public.personalproducts ALTER COLUMN additives SET DEFAULT '{}';
UPDATE public.personalproducts SET additives='{}' WHERE additives IS NULL;
