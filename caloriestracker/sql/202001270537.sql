--  Additivesrisk foreign key
ALTER TABLE public.additives RENAME COLUMN risk to additiverisks_id;
ALTER TABLE public.additives ADD CONSTRAINT additives_additiverisks_fk FOREIGN KEY (additiverisks_id) REFERENCES additiverisks(id) ON DELETE NO ACTION ON UPDATE NO ACTION;

