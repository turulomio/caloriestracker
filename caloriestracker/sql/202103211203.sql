select;
insert into public.companies(name, last, obsolete, id ) values ('Agrupación de cooperativas Valle del Jerte', '2020-12-23T10:37:34.725044+01:00'::timestamptz, false, 52);
insert into public.companies(name, last, obsolete, id ) values ('Carrefour', '2020-03-08T10:08:39.860971+01:00'::timestamptz, false, 53);
insert into public.companies(name, last, obsolete, id ) values ('Galbusera', '2020-04-29T19:35:52.652333+02:00'::timestamptz, false, 54);
insert into public.companies(name, last, obsolete, id ) values ('Hatherwood', '2020-03-03T18:24:22.282633+01:00'::timestamptz, false, 55);
insert into public.companies(name, last, obsolete, id ) values ('Heineken', '2020-06-02T20:17:04.719272+02:00'::timestamptz, false, 56);
insert into public.companies(name, last, obsolete, id ) values ('Häagen-Dazs', '2020-07-01T20:07:17.144089+02:00'::timestamptz, false, 57);
insert into public.companies(name, last, obsolete, id ) values ('IFA', '2020-06-02T20:14:27.769515+02:00'::timestamptz, false, 58);
insert into public.companies(name, last, obsolete, id ) values ('Kellogg''s', '2020-04-09T08:56:22.905749+02:00'::timestamptz, false, 59);
insert into public.companies(name, last, obsolete, id ) values ('La hacienda del ibérico', '2020-02-28T15:32:36.479397+01:00'::timestamptz, false, 60);
insert into public.companies(name, last, obsolete, id ) values ('Pagani', '2020-12-22T16:01:16.152613+01:00'::timestamptz, false, 61);
insert into public.companies(name, last, obsolete, id ) values ('Supersol', '2020-07-25T14:46:11.032873+02:00'::timestamptz, false, 62);
insert into public.companies(name, last, obsolete, id ) values ('Yaranza', '2020-11-28T19:14:45.670798+01:00'::timestamptz, false, 63);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Almendra tostada 0 sal', 100.00, 57.00, 23.00, 3.00, 1, '2020-04-18T13:19:18.767321+02:00'::timestamptz, 
                    NULL, NULL, 628.00, 0.00, 0.00, NULL, 
                    NULL, 11.00, 1.00, 4.80, true, 10, '{}',
                    true, 3.30, 230.00, 539.00, NULL, false , 232);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Anguriñas de Surimi', 100.00, 13.60, 8.80, 7.50, 38, '2020-02-29T11:29:42.903796+01:00'::timestamptz, 
                    NULL, NULL, 188.00, 1.60, NULL, NULL, 
                    NULL, 0.00, 1.20, 1.30, true, 5, '{}',
                    true, NULL, NULL, NULL, NULL, false , 233);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Bizcochos de caramelo y chocolate', 100.00, 28.40, 5.40, 56.40, 55, '2020-03-03T18:29:07.376419+01:00'::timestamptz, 
                    NULL, NULL, 507.00, 0.28, NULL, NULL, 
                    NULL, 0.00, 31.80, 15.00, true, 16, ARRAY[405,411,177,316],
                    false, NULL, NULL, NULL, NULL, false , 234);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Cerveza Heineken', 100.00, 0.00, 0.00, 0.00, 56, '2020-06-02T20:18:06.958418+02:00'::timestamptz, 
                    NULL, NULL, 42.00, 0.00, NULL, NULL, 
                    NULL, 0.00, 0.00, 0.00, true, 15, '{}',
                    false, NULL, NULL, NULL, NULL, false , 235);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Chorizo mini ibérico extra', 100.00, 36.40, 32.20, 1.00, 60, '2020-02-28T15:37:04.658409+01:00'::timestamptz, 
                    NULL, NULL, 461.60, 2.90, NULL, NULL, 
                    NULL, 0.00, 0.50, 14.70, true, 14, ARRAY[631,331,171,130,132,15],
                    false, NULL, NULL, NULL, NULL, false , 236);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Corn Flakes', 30.00, 0.30, 2.10, 25.00, 59, '2020-04-09T09:00:10.996323+02:00'::timestamptz, 
                    NULL, NULL, 113.00, NULL, NULL, 340.00, 
                    NULL, 0.90, 2.40, 0.10, true, 9, '{}',
                    false, 2.40, NULL, NULL, NULL, false , 237);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Crema de chocolate y nata', 100.00, 8.30, 3.10, 18.00, 1, '2020-07-11T17:11:13.389073+02:00'::timestamptz, 
                    NULL, NULL, 160.00, 0.13, NULL, NULL, 
                    NULL, 0.00, 16.00, 5.40, true, 7, ARRAY[367,370,280],
                    true, NULL, NULL, NULL, NULL, false , 238);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Estrellitas', 100.00, 26.00, 3.60, 57.00, 62, '2020-07-25T14:48:39.757885+02:00'::timestamptz, 
                    NULL, NULL, 484.00, 3.50, NULL, NULL, 
                    NULL, 3.70, 1.10, 3.20, true, 14, ARRAY[496],
                    false, NULL, NULL, NULL, NULL, false , 239);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Foie gras Tapa Negra -50% grasas', 100.00, 12.00, 14.00, 3.20, 20, '2020-06-04T21:14:53.029774+02:00'::timestamptz, 
                    NULL, NULL, 181.00, 1.80, NULL, NULL, 
                    NULL, 0.00, 1.50, 4.20, true, 14, ARRAY[280,338,496,130],
                    false, NULL, NULL, NULL, NULL, false , 240);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Gin', 100.00, 0.00, 0.00, 0.00, NULL, '2020-05-03T07:49:23.810034+02:00'::timestamptz, 
                    NULL, NULL, 221.00, NULL, NULL, 2.00, 
                    NULL, 0.00, 0.00, 0.00, NULL, 15, '{}',
                    true, 0.10, NULL, NULL, NULL, false , 241);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Gominolas Boca Fruit', 100.00, 0.00, 3.40, 80.00, 1, '2020-02-29T06:10:01.506358+01:00'::timestamptz, 
                    NULL, NULL, 340.00, 0.21, NULL, NULL, 
                    NULL, 0.00, 69.00, 0.00, true, 16, ARRAY[317,185,186,2,15],
                    false, NULL, NULL, NULL, NULL, false , 242);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Helado Juicy White Peach & Raspberry', 100.00, 13.50, 3.50, 23.40, 57, '2020-07-01T20:10:13.915785+02:00'::timestamptz, 
                    NULL, NULL, 230.00, NULL, NULL, NULL, 
                    NULL, 0.50, 23.20, 8.30, true, 7, ARRAY[316],
                    true, NULL, NULL, NULL, NULL, false , 243);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Helado cucurucho nata', 72.00, 12.00, 2.80, 28.00, 1, '2020-09-08T20:27:25.370447+02:00'::timestamptz, 
                    NULL, NULL, 233.00, 0.12, NULL, NULL, 
                    NULL, 1.00, 22.00, 8.20, true, 7, ARRAY[367,286,284,280],
                    false, NULL, NULL, NULL, NULL, false , 244);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Higos secos', 100.00, 1.27, 2.90, 59.50, 52, '2020-12-23T10:39:27.660224+01:00'::timestamptz, 
                    NULL, NULL, 278.00, 0.00, NULL, NULL, 
                    NULL, 7.40, 54.90, 0.00, true, 10, '{}',
                    true, NULL, NULL, NULL, NULL, false , 245);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Huevos de codorniz', 100.00, 11.10, 13.10, 0.40, NULL, '2020-02-28T15:36:54.158478+01:00'::timestamptz, 
                    NULL, NULL, 154.00, 0.34, NULL, NULL, 
                    NULL, 0.00, 0.40, 3.60, NULL, 6, '{}',
                    false, NULL, NULL, NULL, NULL, false , 246);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Kefir con fresas', 100.00, 3.00, 2.70, 12.90, 63, '2020-11-28T19:16:41.518278+01:00'::timestamptz, 
                    NULL, NULL, 89.00, 0.00, NULL, NULL, 
                    NULL, 0.00, 12.00, 1.90, true, 7, '{}',
                    true, NULL, NULL, NULL, NULL, false , 247);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Magdalenas', 100.00, 22.00, 5.50, 52.00, 1, '2020-03-18T06:34:00.910159+01:00'::timestamptz, 
                    NULL, NULL, 424.00, 0.78, NULL, NULL, 
                    NULL, 2.00, 28.00, 2.70, true, 16, ARRAY[294,405,198,94],
                    false, NULL, NULL, NULL, NULL, false , 248);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Maíz dulce', 100.00, 1.30, 0.00, 12.00, 1, '2020-07-26T12:05:31.410942+02:00'::timestamptz, 
                    NULL, NULL, 79.00, 0.01, NULL, NULL, 
                    NULL, 3.30, 5.50, 0.30, true, 2, '{}',
                    true, NULL, NULL, NULL, NULL, false , 249);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Mermelada de Arándano extra', 100.00, 0.20, 0.80, 42.00, 47, '2020-03-08T10:27:41.478881+01:00'::timestamptz, 
                    NULL, NULL, 176.00, 0.00, NULL, NULL, 
                    NULL, 1.70, 39.10, 0.00, true, 16, ARRAY[317,185],
                    false, NULL, NULL, NULL, NULL, false , 250);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Muslitos de Surimi', 100.00, 4.30, 6.90, 26.10, 38, '2020-05-19T19:29:30.367924+02:00'::timestamptz, 
                    NULL, NULL, 173.00, 1.55, NULL, NULL, 
                    NULL, 1.30, 2.10, 0.50, true, 14, ARRAY[81],
                    true, NULL, NULL, NULL, NULL, false , 251);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Orange', 100.00, 0.12, 0.94, 11.75, NULL, '2020-05-04T06:30:13.456347+02:00'::timestamptz, 
                    NULL, NULL, 47.00, NULL, 0.00, 0.00, 
                    NULL, 2.40, 9.35, 0.02, NULL, 1, '{}',
                    true, NULL, NULL, NULL, NULL, false , 252);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Pan Naan', 100.00, 8.10, 8.10, 49.00, 53, '2020-03-08T10:17:33.589515+01:00'::timestamptz, 
                    NULL, NULL, 307.00, 1.30, NULL, NULL, 
                    NULL, 3.00, 2.80, 0.60, true, 9, ARRAY[79,329,405,432,218,147,373,154],
                    false, NULL, NULL, NULL, NULL, false , 253);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Pan burger Maxi', 100.00, 4.50, 10.00, 45.00, 1, '2020-06-13T09:38:36.403798+02:00'::timestamptz, 
                    NULL, NULL, 270.00, 1.10, NULL, NULL, 
                    NULL, 3.50, 5.50, 0.80, true, 9, ARRAY[373,367,147,94,92],
                    false, NULL, NULL, NULL, NULL, false , 254);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Pan de leche', 100.00, 15.00, 8.90, 50.00, 1, '2020-03-25T08:50:03.235763+01:00'::timestamptz, 
                    NULL, NULL, 375.00, 1.10, NULL, NULL, 
                    NULL, 2.10, 14.00, 6.10, true, 9, ARRAY[367,384,94,147,291,185,50],
                    false, NULL, NULL, NULL, NULL, false , 255);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Panela', 100.00, 0.00, 0.70, 94.00, 1, '2020-05-28T12:19:57.030781+02:00'::timestamptz, 
                    NULL, NULL, 376.00, 0.00, NULL, 60.00, 
                    160.00, 0.26, 94.00, 0.00, true, 16, '{}',
                    false, 5.00, NULL, 65.00, 200.00, false , 256);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Queso Gorgonzola', 100.00, 27.00, 19.40, 0.98, 1, '2020-04-16T14:29:02.430214+02:00'::timestamptz, 
                    NULL, NULL, 325.00, 1.81, NULL, NULL, 
                    NULL, 0.00, 0.10, 19.40, true, 7, '{}',
                    false, NULL, NULL, NULL, NULL, false , 257);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Salpicks', 100.00, 19.50, 8.00, 64.50, 54, '2020-04-29T19:39:53.679427+02:00'::timestamptz, 
                    NULL, NULL, 471.00, 2.25, NULL, NULL, 
                    NULL, 2.50, 7.00, 10.30, true, 9, ARRAY[412,216,405],
                    false, NULL, NULL, NULL, NULL, false , 258);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Schoko-Bons', 100.00, 36.60, 8.30, 52.50, 27, '2020-07-04T09:00:16.917486+02:00'::timestamptz, 
                    NULL, NULL, 576.00, 0.28, NULL, NULL, 
                    NULL, 0.00, 52.20, 21.20, true, 16, '{}',
                    false, NULL, NULL, NULL, NULL, false , 259);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Snack Gamba', 100.00, 37.70, 2.50, 58.10, 1, '2020-03-12T19:57:33.211496+01:00'::timestamptz, 
                    NULL, NULL, 576.00, 1.43, NULL, NULL, 
                    NULL, 0.00, 2.64, 3.64, true, 14, ARRAY[496],
                    false, NULL, NULL, NULL, NULL, false , 260);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Snikis de patata', 100.00, 26.00, 1.10, 60.00, 58, '2020-06-02T20:16:06.420828+02:00'::timestamptz, 
                    NULL, NULL, 489.00, 2.80, NULL, NULL, 
                    NULL, 5.40, 0.25, 3.30, true, 14, ARRAY[496],
                    false, NULL, NULL, NULL, NULL, false , 261);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Sweet corn', 100.00, 1.18, 3.22, 19.02, NULL, '2020-07-13T15:50:37.605216+02:00'::timestamptz, 
                    NULL, NULL, 86.00, 0.04, 0.00, NULL, 
                    270.00, 2.70, 3.22, 0.18, NULL, 9, '{}',
                    true, NULL, NULL, NULL, NULL, false , 262);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Tortellini con carne', 100.00, 9.00, 14.00, 61.00, 61, '2020-12-22T16:03:44.884800+01:00'::timestamptz, 
                    NULL, NULL, 387.00, 2.00, NULL, NULL, 
                    NULL, 3.00, 2.00, 3.60, true, 9, '{}',
                    false, NULL, NULL, NULL, NULL, false , 263);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Tortilla de patatas con cebolla', 100.00, 9.20, 5.30, 13.00, 1, '2020-09-08T17:04:23.148374+02:00'::timestamptz, 
                    NULL, NULL, 158.00, 1.30, NULL, NULL, 
                    NULL, 0.00, 1.00, 1.60, true, 14, ARRAY[97,185],
                    true, NULL, NULL, NULL, NULL, false , 264);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Tostadas sin gluten', 100.00, 2.90, 6.40, 84.00, 1, '2020-06-04T21:12:51.463272+02:00'::timestamptz, 
                    NULL, NULL, 391.00, 1.60, NULL, NULL, 
                    NULL, 1.50, 2.70, 0.50, true, 9, '{}',
                    true, NULL, NULL, NULL, NULL, false , 265);
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('White wine', 100.00, 0.00, 0.07, 2.58, NULL, '2020-11-29T13:06:13.975373+01:00'::timestamptz, 
                    NULL, NULL, 83.00, 0.01, 0.00, NULL, 
                    71.00, 0.00, 0.95, 0.00, NULL, 15, '{}',
                    true, NULL, NULL, NULL, NULL, false , 266);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Package', 200.00, '2020-03-03T18:39:44.177329+01:00'::timestamptz, 234, true, 76);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 50.00, '2020-03-03T18:39:36.439263+01:00'::timestamptz, 234, true, 77);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Can', 330.00, '2020-06-02T20:19:26.304289+02:00'::timestamptz, 235, true, 78);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 115.00, '2020-07-11T17:11:33.597879+02:00'::timestamptz, 238, true, 79);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Package', 50.00, '2020-07-25T14:48:53.605235+02:00'::timestamptz, 239, true, 80);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Can', 73.00, '2020-06-04T21:09:11.903018+02:00'::timestamptz, 240, true, 81);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Bag', 200.00, '2020-02-29T06:10:19.964238+01:00'::timestamptz, 242, true, 82);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 7.00, '2020-02-29T06:10:55.306791+01:00'::timestamptz, 242, true, 83);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 400.00, '2020-07-01T20:22:10.574696+02:00'::timestamptz, 243, true, 84);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 72.00, '2020-09-08T20:27:37.446534+02:00'::timestamptz, 244, true, 85);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Bottle', 500.00, '2020-11-28T19:18:49.913585+01:00'::timestamptz, 247, true, 86);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 34.00, '2020-03-18T06:34:12.339017+01:00'::timestamptz, 248, true, 87);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Package', 240.00, '2020-03-08T10:17:51.580240+01:00'::timestamptz, 253, true, 88);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 120.00, '2020-03-08T10:17:57.211516+01:00'::timestamptz, 253, true, 89);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 75.00, '2020-06-13T09:38:47.538611+02:00'::timestamptz, 254, true, 90);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 40.00, '2020-03-25T08:50:12.829159+01:00'::timestamptz, 255, true, 91);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 25.00, '2020-04-29T19:40:15.540607+02:00'::timestamptz, 258, true, 92);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 5.80, '2020-07-04T09:01:07.087009+02:00'::timestamptz, 259, true, 93);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Package', 60.00, '2020-03-12T19:57:51.610483+01:00'::timestamptz, 260, true, 94);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Package', 75.00, '2020-06-02T20:16:22.093152+02:00'::timestamptz, 261, true, 95);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 5.55, '2020-06-04T21:13:37.181630+02:00'::timestamptz, 265, true, 96);
