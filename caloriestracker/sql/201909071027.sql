ALTER TABLE users ADD COLUMN dietwish integer default 1;
COMMENT ON TABLE users IS '0 perder, 1 mantenimiento, 2 aumentar';
