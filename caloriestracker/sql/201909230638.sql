ALTER TABLE public.formats DROP COLUMN starts CASCADE;
ALTER TABLE public.formats DROP COLUMN ends CASCADE;
ALTER TABLE public.formats ADD COLUMN last TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE public.personalformats DROP COLUMN starts CASCADE;
ALTER TABLE public.personalformats DROP COLUMN ends CASCADE;
ALTER TABLE public.personalformats ADD COLUMN last TIMESTAMP WITH TIME ZONE DEFAULT now() NOT NULL;

ALTER TABLE public.companies RENAME COLUMN starts TO last;
ALTER TABLE public.companies DROP COLUMN ends CASCADE;
ALTER TABLE public.companies ALTER COLUMN last SET NOT NULL;
ALTER TABLE public.companies ALTER COLUMN last SET DEFAULT NOW();

ALTER TABLE public.personalcompanies RENAME COLUMN starts TO last;
ALTER TABLE public.personalcompanies DROP COLUMN ends CASCADE;
ALTER TABLE public.personalcompanies ALTER COLUMN last SET NOT NULL;
ALTER TABLE public.personalcompanies ALTER COLUMN last SET DEFAULT NOW();

ALTER TABLE public.products RENAME COLUMN starts TO last;
ALTER TABLE public.products DROP COLUMN ends CASCADE;
ALTER TABLE public.products ALTER COLUMN last SET NOT NULL;
ALTER TABLE public.products ALTER COLUMN last SET DEFAULT NOW();

ALTER TABLE public.personalproducts RENAME COLUMN starts TO last;
ALTER TABLE public.personalproducts DROP COLUMN ends CASCADE;
ALTER TABLE public.personalproducts ALTER COLUMN last SET NOT NULL;
ALTER TABLE public.personalproducts ALTER COLUMN last SET DEFAULT NOW();


