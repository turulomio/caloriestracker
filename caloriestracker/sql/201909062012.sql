ALTER TABLE users ADD COLUMN birthday date;
INSERT INTO USERS (name,starts,male,birthday) VALUES('Default', now(), true, '1970-1-1');