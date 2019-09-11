ALTER TABLE companies DROP COLUMN countries_id;
ALTER TABLE countries RENAME TO languages;
ALTER TABLE products DROP COLUMN countries_id;
ALTER TABLE products ADD COLUMN languages int[];
DROP SEQUENCE countries_id_seq CASCADE;
DELETE FROM languages;
INSERT INTO languages(id,name) VALUES (1, 'Spanish');
INSERT INTO languages(id,name) VALUES (2, 'French');
INSERT INTO languages(id,name) VALUES (3, 'English');