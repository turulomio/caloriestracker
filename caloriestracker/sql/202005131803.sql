-- Companies inserts
insert into public.companies(name, last, obsolete, id ) values ('Campbells', '2020-05-13T18:00:04.115686'::timestamp, false, 51);

-- Companies updates

-- Companies deletes

-- Products inserts
insert into products (
                    name, amount, fat, protein, carbohydrate, companies_id, last,
                    elaboratedproducts_id, languages, calories, salt, cholesterol, sodium, 
                    potassium, fiber, sugars, saturated_fat, system_company, foodtypes_id, additives,
                    glutenfree, ferrum, magnesium, phosphor, calcium, obsolete
                    , id ) values ('Shortbread rounds. All butter', 100, 30.1, 5.4, 59.6, 51, '2020-05-13T18:02:05.012028'::timestamp, 
                    NULL, NULL, 526, 1, NULL, NULL, 
                    NULL, NULL, 18.5, 17.6, true, 9, '{}',
                    false, NULL, NULL, NULL, NULL, false , 231);

-- Products updates
update public.products set name='Peppers from Padrón', amount=100.00, fat=0.10, protein=0.90, carbohydrate=5.10, companies_id=NULL, last='2020-05-13T18:03:15.455405'::timestamp,
            elaboratedproducts_id=NULL, languages=NULL, calories=21.00, salt=0.00, cholesterol=0.00, sodium=1173.00, potassium=187.00, fiber=1.30, sugars=3.12, saturated_fat=0.01, 
            system_company=NULL, foodtypes_id=2, additives='{}', glutenfree=true, ferrum=NULL, magnesium=NULL, phosphor=NULL, calcium=NULL, obsolete=false
            where id=110;

-- Formats inserts
insert into formats(name, amount, last, products_id, system_product, id ) values ('Unit', 20, '2020-05-13T18:05:14.820244'::timestamp, 231, true, 75);

-- Formats updates
