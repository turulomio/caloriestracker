--  Update bad company
update products set companies_id=NULL, system_company=NULL where id=23;
update products set companies_id=8, system_company=True where id=66; 
