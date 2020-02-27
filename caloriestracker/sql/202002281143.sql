select;
insert into public.companies(name, last, id ) values ('Arla Foods', '2019-12-16T20:26:55.115034+01:00'::timestamptz, 44);
insert into public.companies(name, last, id ) values ('Campina', '2020-01-03T09:36:01.979476+01:00'::timestamptz, 45);
insert into public.companies(name, last, id ) values ('Ferrero', '2019-12-27T10:23:21.103692+01:00'::timestamptz, 46);
insert into public.companies(name, last, id ) values ('Helios', '2020-02-10T08:08:40.575294+01:00'::timestamptz, 47);
insert into public.companies(name, last, id ) values ('Milbona', '2019-12-27T09:48:50.585410+01:00'::timestamptz, 48);
insert into public.companies(name, last, id ) values ('Puleva', '2019-12-12T05:53:11.896843+01:00'::timestamptz, 49);
insert into public.companies(name, last, id ) values ('Zanetti', '2019-12-27T09:42:05.911881+01:00'::timestamptz, 50);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Batido de chocolate 30% menos azucar', 100.00, 1.20, 3.20, 9.50, 49, '2020-01-28T14:42:28.012361+01:00'::timestamptz, 
                    NULL, NULL, 62.00, 0.18, NULL, NULL, 
                    NULL, 0.00, 9.50, 0.80, true, 16, '{}', 195);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Berlina Glacé', 100.00, 24.00, 5.40, 42.00, 1, '2020-01-28T14:42:40.932015+01:00'::timestamptz, 
                    NULL, NULL, 410.00, 0.94, NULL, NULL, 
                    NULL, 0.00, 16.00, 12.00, true, 16, '{}', 196);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Bizcochos recubiertos de chocolate. Corazón de Naranja', 100.00, 10.00, 3.00, 69.00, 1, '2020-02-25T15:02:16.878271+01:00'::timestamptz, 
                    NULL, NULL, 380.00, 0.15, NULL, NULL, 
                    NULL, 2.00, 52.00, 6.00, true, 16, ARRAY[177,294,316,185,412,405,367,186], 197);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Caldo casero de cocido 100% Natural', 100.00, 0.30, 0.30, 0.10, 19, '2020-01-28T14:42:54.644344+01:00'::timestamptz, 
                    NULL, NULL, 4.00, 0.75, NULL, NULL, 
                    NULL, 0.00, 0.00, 0.10, true, 17, '{}', 198);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Cherries Licor', 100.00, 19.00, 2.70, 58.00, 1, '2020-02-03T20:16:10.144397+01:00'::timestamptz, 
                    NULL, NULL, 451.00, 0.00, NULL, NULL, 
                    NULL, 3.40, 55.00, 12.00, true, 16, ARRAY[620,185], 199);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Chocolate con leche. Original 35% cacao', 100.00, 32.00, 7.30, 55.00, 39, '2020-01-28T16:48:24.646038+01:00'::timestamptz, 
                    NULL, NULL, 537.00, 0.35, NULL, NULL, 
                    NULL, 0.00, 54.00, 20.00, true, 16, '{}', 200);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Chocolate negro mini barritas 70% cacao', 100.00, 41.00, 9.00, 33.00, 1, '2020-01-28T14:43:02.267908+01:00'::timestamptz, 
                    NULL, NULL, 560.00, 0.10, NULL, NULL, 
                    NULL, 0.00, 21.00, 21.00, true, 16, '{}', 201);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Coca Cola', 100.00, 0.00, 0.00, 10.60, 6, '2020-01-29T10:30:46.624636+01:00'::timestamptz, 
                    NULL, NULL, 42.00, 0.00, NULL, NULL, 
                    NULL, 0.00, 10.60, 0.00, true, 13, ARRAY[43,206], 202);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Coca Cola Light', 100.00, 0.00, 0.00, 0.00, 6, '2020-01-29T11:57:11.037364+01:00'::timestamptz, 
                    NULL, NULL, 0.20, 0.00, NULL, 0.00, 
                    NULL, 0.00, 0.00, 0.00, true, 12, ARRAY[43,185,206,575,576,577], 203);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Coca Cola Zero', 100.00, 0.00, 0.00, 0.00, 6, '2020-01-29T10:28:15.913642+01:00'::timestamptz, 
                    NULL, NULL, 0.20, 0.02, NULL, NULL, 
                    NULL, 0.00, 0.00, 0.00, true, 12, ARRAY[43,577,575,206,186], 204);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Coca Cola Zero Zero', 100.00, 0.00, 0.00, 0.00, 6, '2020-01-29T22:20:50.101795+01:00'::timestamptz, 
                    NULL, NULL, 0.20, 0.02, NULL, NULL, 
                    NULL, 0.00, 0.00, 0.00, true, 12, ARRAY[43,579,575,576,206,186], 205);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Dátiles sin hueso', 100.00, 1.00, 2.10, 68.00, 1, '2020-01-28T14:39:56.876960+01:00'::timestamptz, 
                    NULL, NULL, 305.00, 0.00, NULL, NULL, 
                    NULL, 8.20, 65.00, 0.30, true, 1, ARRAY[94], 206);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Fabada', 100.00, 12.00, 6.10, 9.30, 1, '2020-02-05T17:02:19.543499+01:00'::timestamptz, 
                    NULL, NULL, 175.00, 0.90, NULL, NULL, 
                    NULL, 3.20, 0.50, 5.00, true, 3, ARRAY[264], 207);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Galletas campurrianas', 100.00, 15.00, 5.00, 74.00, 26, '2020-01-29T11:48:29.528445+01:00'::timestamptz, 
                    NULL, NULL, 455.00, 0.68, NULL, NULL, 
                    NULL, 0.00, 26.00, 7.20, true, 16, '{}', 208);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Galletas de mantequilla', 100.00, 26.00, 6.00, 62.00, 1, '2020-01-28T14:43:19.364167+01:00'::timestamptz, 
                    NULL, NULL, 507.00, 1.00, NULL, NULL, 
                    NULL, 1.50, 25.00, 17.50, true, 16, '{}', 209);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Grana Padano', 100.00, 29.00, 33.00, 0.00, 50, '2020-01-28T14:43:25.292123+01:00'::timestamptz, 
                    NULL, NULL, 398.00, 1.50, NULL, NULL, 
                    NULL, 0.00, 0.00, 18.00, true, 7, '{}', 210);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Kaffee sahne', 100.00, 10.20, 3.20, 4.20, 45, '2020-01-28T14:43:35.419795+01:00'::timestamptz, 
                    NULL, NULL, 122.00, 0.10, NULL, NULL, 
                    NULL, 0.00, 4.20, 7.30, true, 7, '{}', 211);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Mermelada de fresa  0% azúcares añadidos', 100.00, 0.00, 0.60, 10.40, 1, '2020-01-30T06:34:32.448891+01:00'::timestamptz, 
                    NULL, NULL, 38.00, 0.00, NULL, NULL, 
                    NULL, 1.60, 4.70, 0.00, true, 16, ARRAY[295,587,592,317,182,185,94], 212);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Mermelada de fresa extra', 100.00, 0.00, 0.50, 44.00, 47, '2020-02-10T08:11:25.440972+01:00'::timestamptz, 
                    NULL, NULL, 180.00, 0.00, NULL, NULL, 
                    NULL, 1.20, 42.70, 0.00, true, 16, ARRAY[317,185,94,97,154], 213);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Mon Cheri', 100.00, 20.30, 3.00, 52.80, 46, '2020-01-28T14:43:47.139565+01:00'::timestamptz, 
                    NULL, NULL, 455.00, 0.01, NULL, NULL, 
                    NULL, 0.00, 48.30, 13.20, true, 16, '{}', 214);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Natillas sabor fresa', 100.00, 4.40, 3.70, 19.20, 1, '2020-01-30T06:37:47.769096+01:00'::timestamptz, 
                    NULL, NULL, 133.00, 0.10, NULL, NULL, 
                    NULL, 0.00, 16.10, 2.90, true, 7, ARRAY[189], 215);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Nuez natural', 100.00, 67.00, 19.00, 3.50, 1, '2020-01-29T12:43:57.255927+01:00'::timestamptz, 
                    NULL, NULL, 702.00, 0.00, NULL, NULL, 
                    NULL, 5.60, 2.40, 5.70, true, 10, '{}', 216);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('PIM''s Orange', 100.00, 13.00, 3.30, 66.00, 37, '2020-01-28T14:43:59.195806+01:00'::timestamptz, 
                    NULL, NULL, 398.00, 0.41, NULL, NULL, 
                    NULL, 2.50, 48.00, 5.80, true, 16, '{}', 217);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Pimientos rellenos de bacalao', 100.00, 2.70, 4.70, 11.70, 1, '2020-01-28T14:44:17.683500+01:00'::timestamptz, 
                    NULL, NULL, 92.00, 0.00, NULL, 0.40, 
                    NULL, 0.00, 1.30, 0.50, true, 5, '{}', 218);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Pistachos Tostado Sal', 100.00, 51.00, 25.00, 10.00, 1, '2020-01-28T14:44:29.835664+01:00'::timestamptz, 
                    NULL, NULL, 617.00, 0.79, NULL, NULL, 
                    NULL, 8.90, 8.30, 6.40, true, 10, '{}', 219);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Queso Castello con Trufa', 100.00, 38.00, 14.00, 0.50, 44, '2020-01-28T14:44:40.083412+01:00'::timestamptz, 
                    NULL, NULL, 403.00, 1.50, NULL, NULL, 
                    NULL, 0.00, 0.50, 24.00, true, 7, '{}', 220);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Queso Emmental rallado', 100.00, 28.00, 28.00, 3.00, 48, '2020-02-28T10:19:19.814859+01:00'::timestamptz, 
                    NULL, NULL, 376.00, 0.50, NULL, NULL, 
                    NULL, 0.00, 0.10, 18.10, true, 7, '{}', 221);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Solomillo Añojo', 100.00, 3.30, 21.00, 0.00, 1, '2020-01-28T16:11:51.537196+01:00'::timestamptz, 
                    NULL, NULL, 116.00, 0.17, NULL, NULL, 
                    NULL, 0.00, 0.00, 1.20, true, 4, '{}', 222);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Strawberries', 100.00, 0.40, 0.81, 5.51, NULL, '2020-01-28T14:44:50.867462+01:00'::timestamptz, 
                    NULL, NULL, 32.24, NULL, 0.00, 1.40, 
                    161.00, 1.68, 2.17, 0.03, NULL, 1, '{}', 223);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Tortillas de trigo', 100.00, 5.40, 7.30, 55.00, 1, '2020-02-10T16:02:02.571886+01:00'::timestamptz, 
                    NULL, NULL, 302.00, 1.70, NULL, NULL, 
                    NULL, 2.00, 2.20, 2.60, true, 9, ARRAY[298,367,152,185,147,94,406,289,550], 224);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Tortitas de arroz con chocolate blanco sabor yogur', 100.00, 20.00, 7.20, 63.00, 1, '2020-01-28T14:44:57.411314+01:00'::timestamptz, 
                    NULL, NULL, 467.00, 0.72, NULL, NULL, 
                    NULL, 3.00, 29.00, 12.00, true, 16, '{}', 225);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Yogur Activia cremoso Lima & Limón', 100.00, 3.50, 3.70, 13.00, 3, '2020-01-28T14:45:06.795234+01:00'::timestamptz, 
                    NULL, NULL, 101.00, 0.12, NULL, NULL, 
                    NULL, 0.00, 12.70, 2.10, true, 7, '{}', 226);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Yogur Natural Bifidus 0%', 100.00, 0.00, 4.30, 4.20, 1, '2020-01-28T14:45:12.779117+01:00'::timestamptz, 
                    NULL, NULL, 34.00, 0.15, NULL, NULL, 
                    NULL, 0.00, 4.20, 0.00, true, 7, '{}', 227);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Zucchini', 100.00, 0.18, 1.21, 3.35, NULL, '2020-01-28T14:45:25.715293+01:00'::timestamptz, 
                    NULL, NULL, 16.00, NULL, NULL, 10.00, 
                    262.00, 1.10, 1.73, 0.04, NULL, 2, '{}', 228);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives
                    , id ) values ('Zumo de manzana', 100.00, 0.10, 0.10, 11.30, 1, '2020-01-28T14:45:37.698953+01:00'::timestamptz, 
                    NULL, NULL, 44.00, 0.00, NULL, NULL, 
                    NULL, 0.00, 0.00, 0.00, true, 13, '{}', 229);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 12.50, '2020-02-25T20:42:04.891899+01:00'::timestamptz, 197, true, 55);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Package', 145.00, '2020-02-03T20:16:38.728943+01:00'::timestamptz, 199, true, 56);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 12.00, '2020-02-03T20:16:25.703990+01:00'::timestamptz, 199, true, 57);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Little stick', 11.00, '2020-01-04T13:00:12.348919+01:00'::timestamptz, 201, true, 58);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Cookie', 15.62, '2019-12-10T06:06:56.764546+01:00'::timestamptz, 209, true, 59);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Package', 125.00, '2019-12-10T06:06:16.477968+01:00'::timestamptz, 209, true, 60);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 10.00, '2020-01-03T09:44:33.718484+01:00'::timestamptz, 211, true, 61);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 12.00, '2019-12-27T10:34:33.108892+01:00'::timestamptz, 214, true, 62);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 125.00, '2020-01-30T06:39:15.105293+01:00'::timestamptz, 215, true, 63);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Cookie', 12.50, '2020-01-05T10:14:21.440314+01:00'::timestamptz, 217, true, 64);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Package', 150.00, '2020-01-05T10:14:41.528697+01:00'::timestamptz, 217, true, 65);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Package', 200.00, '2019-12-27T09:50:23.662593+01:00'::timestamptz, 221, true, 66);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Package', 30.00, '2019-12-17T09:10:15.596595+01:00'::timestamptz, 225, true, 67);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 125.00, '2019-12-12T05:58:52.373216+01:00'::timestamptz, 226, true, 68);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 125.00, '2019-12-09T17:09:43.641657+01:00'::timestamptz, 227, true, 69);
