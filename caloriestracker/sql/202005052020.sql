-- Companies inserts

-- Companies updates

-- Companies deletes

-- Products inserts
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Caldo de verduras', 100, 0.6, 0.5, 0.5, 1, '2020-05-05T20:20:19.655366'::timestamp, 
                    NULL, NULL, 5, 0.7, NULL, NULL, 
                    NULL, 0.5, 0.5, 0.2, true, 17, '{}',
                    true, NULL, NULL, NULL, NULL, false , 230);

-- Products updates

-- Formats inserts
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 87.5, '2020-05-05T20:19:14.820244'::timestamp, 47, true, 74);

-- Formats updates
