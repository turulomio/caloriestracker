-- Adding foodtypes to elaborated products
ALTER TABLE public.elaboratedproducts ADD COLUMN foodtypes_id INTEGER;
ALTER TABLE public.elaboratedproducts ADD CONSTRAINT elaboratedproducts_foodtypes_fk FOREIGN KEY (foodtypes_id) REFERENCES foodtypes(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
