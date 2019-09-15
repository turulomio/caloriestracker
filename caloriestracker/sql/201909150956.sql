ALTER TABLE public.biometrics RENAME COLUMN dietwish TO weightwish;
COMMENT ON TABLE public.biometrics IS NULL;
COMMENT ON TABLE public.users IS NULL;
