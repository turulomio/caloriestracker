ALTER TABLE public.users DROP COLUMN dietwish;
ALTER TABLE public.biometrics ADD COLUMN dietwish integer not null DEFAULT 1;
