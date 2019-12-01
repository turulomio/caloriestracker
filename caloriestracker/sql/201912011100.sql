-- Removed undeleted personal products without elaboratedproducts
delete from personalproducts where elaboratedproducts_id  not in (select elaboratedproducts.id from personalproducts,elaboratedproducts where elaboratedproducts.id=personalproducts.elaboratedproducts_id);
