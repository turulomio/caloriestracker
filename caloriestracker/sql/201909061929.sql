ALTER TABLE biometrics DROP COLUMN ends;
ALTER TABLE biometrics DROP COLUMN name;
ALTER TABLE biometrics RENAME COLUMN starts TO datetime;