CREATE TABLE companies (
	id serial,
	name text,
	countries_id integer,
	starts timestamp with time zone,
	ends timestamp with time zone
);
ALTER TABLE companies ADD CONSTRAINT companies_pk PRIMARY KEY(id);
CREATE TABLE countries (
	id serial,
	name text
);
ALTER TABLE countries ADD CONSTRAINT countries_pk PRIMARY KEY(id);
CREATE TABLE products (
	id serial,
	name text,
	amount numeric(10, 2),
	fat numeric(10, 2),
	protein numeric(10, 2),
	carbohydrate numeric(10, 2),
	companies_id integer,
	ends timestamp with time zone,
	starts timestamp with time zone,
	personalproducts_id integer,
	countries_id integer
);
ALTER TABLE products ADD CONSTRAINT products_pk PRIMARY KEY(id);
CREATE TABLE formats (
	id serial,
	name text,
	amount numeric(10, 2),
	starts date,
	ends date,
	products_id integer
);
ALTER TABLE formats ADD CONSTRAINT formats_id PRIMARY KEY(id);
CREATE TABLE users (
	id serial,
	name text,
	starts timestamp with time zone,
	ends timestamp with time zone
);
ALTER TABLE users ADD CONSTRAINT users_id PRIMARY KEY(id);
CREATE TABLE meals (
	id serial,
	user_id integer,
	name text,
	amount numeric(10, 2),
	products_id integer,
	datetime timestamp with time zone
);
ALTER TABLE meals ADD CONSTRAINT meals_id PRIMARY KEY(id);
CREATE TABLE personalproducts (
	id serial,
	name text
);
ALTER TABLE personalproducts ADD CONSTRAINT personalproducts_pk PRIMARY KEY(id);
CREATE TABLE products_in_personalproducts (
	id serial,
	products_id integer,
	amount numeric(10, 2),
	personalproducts_id integer
);
ALTER TABLE products_in_personalproducts ADD CONSTRAINT products_in_personalproducts_pk PRIMARY KEY(id);
CREATE TABLE biometrics (
	id serial,
	name text,
	starts timestamp with time zone,
	ends timestamp with time zone,
	weight numeric(10, 2),
	height numeric(10, 2),
	users_id integer
);
ALTER TABLE biometrics ADD CONSTRAINT users_id_CLONE PRIMARY KEY(id);
ALTER TABLE companies ADD CONSTRAINT companies_countries_fk FOREIGN KEY (countries_id) REFERENCES countries(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE products ADD CONSTRAINT products_companies_fk FOREIGN KEY (companies_id) REFERENCES companies(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE formats ADD CONSTRAINT products_formats_fk FOREIGN KEY (products_id) REFERENCES products(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE products_in_personalproducts ADD CONSTRAINT products_in_personalproducts_products_fk FOREIGN KEY (products_id) REFERENCES products(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE products_in_personalproducts ADD CONSTRAINT products_in_personalproducts_personalproducts_fk FOREIGN KEY (personalproducts_id) REFERENCES personalproducts(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE meals ADD CONSTRAINT meals_products_fk FOREIGN KEY (products_id) REFERENCES products(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE meals ADD CONSTRAINT meals_users_fk FOREIGN KEY (products_id) REFERENCES users(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE products ADD CONSTRAINT products_personalproducts_fk FOREIGN KEY (personalproducts_id) REFERENCES personalproducts(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
ALTER TABLE products ADD CONSTRAINT products_countries_fk FOREIGN KEY (countries_id) REFERENCES countries(id) ON DELETE NO ACTION ON UPDATE NO ACTION;
CREATE TABLE globals (
	id serial,
	name text,
	value text
);
INSERT INTO public.globals(id,name,value) values (1, 'Database version', 0);