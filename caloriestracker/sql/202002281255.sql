-- Companies inserts

-- Companies updates

-- Products inserts

-- Products updates
update public.products set name='Anchoas (filetes) en aceite de oliva', amount=100.00, fat=10.00, protein=25.00, carbohydrate=2.00, companies_id=1, last='2020-02-28T12:52:46.064488'::timestamp,
            elaboratedproducts_id=NULL, languages=NULL, calories=192.00, salt=0.00, cholesterol=0.00, sodium=0.00, potassium=0.00, fiber=0.00, sugars=0.00, saturated_fat=0.00, 
            system_company=true, foodtypes_id=5, additives='{}' 
            where id=22;

-- Formats inserts
insert into formats(name, amount, last, products_id, system_product, id ) values ('Drained can', 29, '2020-02-28T12:55:14.134528'::timestamp, 22, true, 70);
insert into formats(name, amount, last, products_id, system_product, id ) values ('Can', 40, '2020-02-28T12:55:33.870411'::timestamp, 22, true, 71);

-- Formats updates
