select;
insert into formats(name, amount, last, products_id, system_product, id) values ('Tostada', 11.25, now(), 19, true, 34);
insert into formats(name, amount, last, products_id, system_product, id) values ('Loncha', 25, now(), 46, true, 35);
update products set companies_id=1, system_company=True where id in (64,65); 
