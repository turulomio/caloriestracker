DROP SEQUENCE formats_id_seq CASCADE;
DELETE FROM public.formats;
CREATE TABLE public.personalformats (
	id serial,
	name text,
	amount numeric(10, 2),
	starts date DEFAULT NOW(),
	ends date,
	products_id integer,
	system_product boolean
);
ALTER TABLE public.personalformats ADD CONSTRAINT personalformats_id PRIMARY KEY(id);
INSERT INTO public.formats(name, amount, starts, ends, products_id, system_product, id) VALUES ('Unidad', 62.5, NOW(),NULL, 45, TRUE, 1);


