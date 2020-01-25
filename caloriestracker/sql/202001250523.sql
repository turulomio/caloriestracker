--  Add food types

CREATE TABLE public.foodtypes (
    id integer NOT NULL,
    name text
);

INSERT INTO public.foodtypes(id,name) VALUES (1, 'Fruit');
INSERT INTO public.foodtypes(id,name) VALUES (2, 'Vegetables');
INSERT INTO public.foodtypes(id,name) VALUES (3, 'Legumes');
INSERT INTO public.foodtypes(id,name) VALUES (4, 'Meat');
INSERT INTO public.foodtypes(id,name) VALUES (5, 'Fish');
INSERT INTO public.foodtypes(id,name) VALUES (6, 'Eggs');
INSERT INTO public.foodtypes(id,name) VALUES (7, 'Dairy products');
INSERT INTO public.foodtypes(id,name) VALUES (8, 'Oils and fats');
INSERT INTO public.foodtypes(id,name) VALUES (9, 'Bread and cereals');
INSERT INTO public.foodtypes(id,name) VALUES (10, 'Dry nuts');
INSERT INTO public.foodtypes(id,name) VALUES (11, 'Water');
INSERT INTO public.foodtypes(id,name) VALUES (12, 'Diet drinks');
INSERT INTO public.foodtypes(id,name) VALUES (13, 'Sugary drinks');
INSERT INTO public.foodtypes(id,name) VALUES (14, 'Processed foods');
INSERT INTO public.foodtypes(id,name) VALUES (15, 'Alcoholic drinks');
INSERT INTO public.foodtypes(id,name) VALUES (16, 'Sweets');
INSERT INTO public.foodtypes(id,name) VALUES (17, 'Soups and infusions');
INSERT INTO public.foodtypes(id,name) VALUES (18, 'Spices');

ALTER TABLE ONLY public.foodtypes
    ADD CONSTRAINT foodtypes_pk PRIMARY KEY (id);

ALTER TABLE public.products ADD COLUMN foodtypes_id INTEGER;
ALTER TABLE public.personalproducts ADD COLUMN foodtypes_id INTEGER;

UPDATE public.products SET foodtypes_id=1 WHERE ID IN (2,8,35,42,55,57,58,59,60,104,108,115,119,124,143,150,152,164,185,186); -- Fruit
UPDATE public.products SET foodtypes_id=2 WHERE ID IN (12,30,49,50,62,67,74,78,84,86,110,117,147,169); -- Vegetables
UPDATE public.products SET foodtypes_id=3 WHERE ID IN (70,71,141); -- Legumes
UPDATE public.products SET foodtypes_id=4 WHERE ID IN (6,29,47,51,68,76,85,103,109,128,132,134,142,149,168,170,181); -- Meat
UPDATE public.products SET foodtypes_id=5 WHERE ID IN (10,22,44,93,139,167,177,183,189); -- Fish
UPDATE public.products SET foodtypes_id=6 WHERE ID IN (11,101,114,137); -- Eggs
UPDATE public.products SET foodtypes_id=7 WHERE ID IN (1,4,17,18,20,33,39,43,46,56,69,75,99,111,112,116,130,133,140,153,154,155,163,172,173,187,188,192,193,194); -- Dairy
UPDATE public.products SET foodtypes_id=8 WHERE ID IN (7,14,24,40,91,106,165); -- Fats
UPDATE public.products SET foodtypes_id=9 WHERE ID IN (9,13,19,23,32,48,52,64,72,77,92,102,123,127,135,144,151,191); -- Bread and cereals
UPDATE public.products SET foodtypes_id=10 WHERE ID IN (79,94,122,166); -- Dry nuts
UPDATE public.products SET foodtypes_id=11 WHERE ID IN (61); -- Water
UPDATE public.products SET foodtypes_id=12 WHERE ID IN (96); -- Diet drinks
UPDATE public.products SET foodtypes_id=13 WHERE ID IN (65); -- Sugary drinds
UPDATE public.products SET foodtypes_id=14 WHERE ID IN (31,41,53,81,82,83,88,89,90,97,107,118,129,131,148,157,159,161,171,178,180,190); -- Processed foods
UPDATE public.products SET foodtypes_id=15 WHERE ID IN (95,105,113); -- Alcoholic drinks
UPDATE public.products SET foodtypes_id=16 WHERE ID IN (5,15,21,25,26,28,34,45,63,66,80,87,98,100,120,125,126,136,138,145,146,158,160,162,174,175,176,179,182,184); -- Sweets
UPDATE public.products SET foodtypes_id=17 WHERE ID IN (121); -- Soaps and infusions
UPDATE public.products SET foodtypes_id=18 WHERE ID IN (156); -- Spices

ALTER TABLE public.products ALTER COLUMN foodtypes_id SET NOT NULL;