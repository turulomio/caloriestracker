ALTER TABLE public.personalproducts RENAME TO elaboratedproducts;
ALTER TABLE public.products_in_personalproducts RENAME TO products_in_elaboratedproducts;
ALTER SEQUENCE public.personalproducts_id_seq RENAME TO elaboratedproducts_id_seq ;
ALTER TABLE public.products RENAME personalproducts_id TO elaboratedproducts_id;
ALTER TABLE public.products ADD COLUMN system_company boolean;
ALTER TABLE public.formats ADD COLUMN system_product boolean;
ALTER TABLE public.meals ADD COLUMN system_product boolean;

CREATE SEQUENCE public.personalproducts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

CREATE TABLE public.personalproducts (
    id integer NOT NULL,
    name text,
    amount numeric(10,2),
    fat numeric(10,2),
    protein numeric(10,2),
    carbohydrate numeric(10,2),
    companies_id integer,
    ends timestamp with time zone,
    starts timestamp with time zone,
    elaboratedproducts_id integer,
    calories numeric(10,2) DEFAULT 0,
    salt numeric(10,2) DEFAULT 0,
    cholesterol numeric(10,2) DEFAULT 0,
    sodium numeric(10,2) DEFAULT 0,
    potassium numeric(10,2) DEFAULT 0,
    fiber numeric(10,2) DEFAULT 0,
    sugars numeric(10,2) DEFAULT 0,
    saturated_fat numeric(10,2) DEFAULT 0,
    languages integer[],
    system_company boolean
);

ALTER TABLE ONLY public.personalproducts ALTER COLUMN id SET DEFAULT nextval('public.personalproducts_id_seq'::regclass);


CREATE TABLE public.personalcompanies (
    id integer NOT NULL,
    name text,
    starts timestamp with time zone,
    ends timestamp with time zone
);


CREATE SEQUENCE public.personalcompanies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE ONLY public.personalcompanies ALTER COLUMN id SET DEFAULT nextval('public.personalcompanies_id_seq'::regclass);




DELETE FROM public.languages;
INSERT INTO public.languages VALUES (1, 'Spanish');
INSERT INTO public.languages VALUES (2, 'French');
INSERT INTO public.languages VALUES (3, 'English');


ALTER TABLE public.products DROP CONSTRAINT products_companies_fk;
DROP SEQUENCE public.companies_id_seq CASCADE;
DELETE FROM public.companies;
INSERT INTO public.companies VALUES (1, 'Hacendado', '2019-09-06 00:00:00+02', NULL);
INSERT INTO public.companies VALUES (2, 'Clesa', '2019-09-06 19:17:00.823865+02', NULL);
INSERT INTO public.companies VALUES (3, 'Danone', '2019-09-07 10:01:22.880883+02', NULL);
INSERT INTO public.companies VALUES (4, 'Pascual', '2019-09-07 11:13:36.508621+02', NULL);
INSERT INTO public.companies VALUES (5, 'Buitoni', '2019-09-07 11:13:43.130065+02', NULL);
INSERT INTO public.companies VALUES (6, 'Coca Cola', '2019-09-07 11:13:49.634123+02', NULL);
INSERT INTO public.companies VALUES (7, 'Cantorel', '2019-09-07 12:05:20.790591+02', NULL);
INSERT INTO public.companies VALUES (8, 'Nestle', '2019-09-09 13:08:09.317285+02', NULL);
INSERT INTO public.companies VALUES (9, 'Schara', '2019-09-09 15:35:30.185888+02', NULL);
INSERT INTO public.companies VALUES (10, 'Monter', '2019-09-09 16:00:11.945959+02', NULL);
INSERT INTO public.companies VALUES (11, 'Haribo', '2019-09-09 17:01:27.033788+02', NULL);
INSERT INTO public.companies VALUES (13, 'Auchan', '2019-09-09 22:12:32.032848+02', NULL);
INSERT INTO public.companies VALUES (14, 'Ubago', '2019-09-11 08:43:58.854739+02', NULL);
INSERT INTO public.companies VALUES (15, 'Pepsi', '2019-09-11 18:05:02.138348+02', NULL);
INSERT INTO public.companies VALUES (16, 'Central Lechera Asturiana', '2019-09-11 21:09:27.054824+02', NULL);

DROP SEQUENCE public.products_id_seq CASCADE;

ALTER TABLE public.meals DROP CONSTRAINT meals_products_fk;
DELETE FROM public.products;
INSERT INTO public.products VALUES (50, 'Pimiento verde', 100.00, 0.17, 0.86, 4.64, NULL, NULL, '2019-09-11 16:07:11.749803+02', NULL, 20.00, 0.00, 0.00, 0.00, 0.00, 1.70, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (1, 'Crema Bombón 0.7% M.G.', 100.00, 2.80, 2.90, 18.50, 2, NULL, '2019-09-06 19:18:50.230204+02', NULL, 111.00, 0.25, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (2, 'Paraguaya', 100.00, 0.20, 0.80, 12.20, NULL, NULL, '2019-09-06 21:01:18.733059+02', NULL, 49.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (5, 'Cola Cao Original', 100.00, 2.70, 6.70, 73.30, NULL, NULL, '2019-09-06 22:05:37.645989+02', NULL, 361.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (6, 'Mermelada', 100.00, 0.10, 0.50, 66.60, NULL, NULL, '2019-09-06 22:07:53.399506+02', NULL, 260.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (7, 'Mantequilla', 100.00, 81.10, 0.90, 0.10, NULL, NULL, '2019-09-06 22:10:00.775081+02', NULL, 717.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (9, 'Bread', 100.00, 1.60, 8.47, 51.50, NULL, NULL, '2019-09-06 22:35:00.08475+02', NULL, 261.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (13, 'Pan con Avena', 100.00, 6.30, 11.00, 39.00, 1, NULL, '2019-09-07 09:34:23.407804+02', NULL, 269.00, 0.00, 0.00, 0.00, 0.00, 6.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (14, 'Mantequilla sin sal añadida', 100.00, 82.00, 0.50, 0.80, 1, NULL, '2019-09-07 09:49:39.334281+02', NULL, 743.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (15, 'Mermelada de albaricoque 0% azucares añadidos', 100.00, 0.00, 0.60, 10.10, 1, NULL, '2019-09-07 09:55:38.646295+02', NULL, 38.00, 0.00, 0.00, 0.00, 0.00, 1.60, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (17, 'Danacol fresa 0% azucares añadidos', 100.00, 1.10, 3.20, 4.30, 3, NULL, '2019-09-07 10:01:27.615502+02', NULL, 43.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (18, 'Roquefort', 100.00, 32.00, 19.00, 1.00, 7, NULL, '2019-09-07 12:06:57.721367+02', NULL, 368.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (19, 'Pan tostado bajo en sal y azúcares', 100.00, 6.10, 12.80, 73.80, 1, NULL, '2019-09-07 12:11:39.288315+02', NULL, 410.00, 0.00, 0.00, 0.00, 0.00, 4.20, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (20, 'Leche entera', 100.00, 3.60, 3.00, 4.80, 4, NULL, '2019-09-08 09:46:34.121118+02', NULL, 64.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (21, 'Miel', 100.00, 0.00, 0.30, 82.00, NULL, NULL, '2019-09-08 09:52:54.846265+02', NULL, 304.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (22, 'Anchoas en aceite de oliva', 100.00, 10.00, 25.00, 2.00, 1, NULL, '2019-09-08 11:47:00.161188+02', NULL, 192.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (23, 'Pan blanco', 100.00, 3.29, 7.64, 50.61, NULL, NULL, '2019-09-09 06:27:31.051315+02', NULL, 266.00, 0.00, 0.00, 0.00, 0.00, 2.40, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (24, 'Mantequilla', 100.00, 82.00, 0.70, 1.10, 4, NULL, '2019-09-09 08:55:15.148407+02', NULL, 745.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (25, 'Mermelada de fresa', 100.00, 0.20, 0.31, 62.60, NULL, NULL, '2019-09-09 09:00:34.565411+02', NULL, 255.04, 0.00, 0.00, 0.00, 0.00, 0.80, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (26, 'Barquillos de nata', 29.00, 9.00, 1.20, 16.60, 1, NULL, '2019-09-09 11:26:58.568289+02', NULL, 153.00, 0.00, 0.00, 0.00, 0.00, 1.20, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (28, 'Leche condensada entera. Nutricia', 100.00, 8.00, 7.50, 55.30, 8, NULL, '2019-09-09 13:09:20.958017+02', NULL, 323.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (29, 'Salchichas', 100.00, 15.37, 9.62, 0.06, 9, NULL, '2019-09-09 15:36:16.092362+02', NULL, 177.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (30, 'Espárragos trigueros', 100.00, 0.12, 2.20, 3.88, NULL, NULL, '2019-09-09 15:40:53.504792+02', NULL, 20.00, 0.00, 0.00, 0.00, 0.00, 2.10, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (31, 'Chorizo de pavo imperial extra', 100.00, 19.00, 31.00, 3.50, 10, NULL, '2019-09-09 16:01:39.132713+02', NULL, 309.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (32, 'Pan burger', 100.00, 4.00, 9.00, 48.00, 1, NULL, '2019-09-09 16:04:00.982274+02', NULL, 269.00, 0.00, 0.00, 0.00, 0.00, 2.50, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (33, 'Gelatina +Proteínas sabor frutos salvajes', 100.00, 0.00, 6.00, 3.80, 1, NULL, '2019-09-09 16:16:13.346164+02', NULL, 39.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (34, 'Chamallows Soft-Kiss Extra', 100.00, 16.00, 3.80, 67.00, 11, NULL, '2019-09-09 17:03:59.834988+02', NULL, 426.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (35, 'Banana', 100.00, 0.50, 1.64, 34.26, NULL, NULL, '2019-09-09 19:09:52.922781+02', NULL, 134.00, 0.00, 0.00, 0.00, 0.00, 3.90, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (51, 'Carne de ternera picada', 100.00, 12.00, 17.00, 0.90, 1, NULL, '2019-09-11 16:12:10.417755+02', NULL, 182.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (52, 'Pan de espelta con masa madre', 100.00, 2.30, 10.00, 49.00, 1, NULL, '2019-09-11 16:16:12.842266+02', NULL, 264.00, 0.00, 0.00, 0.00, 0.00, 3.20, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (39, 'Cuajada', 100.00, 5.00, 4.90, 7.20, 1, NULL, '2019-09-09 22:41:59.82184+02', NULL, 94.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (40, 'Aceite de oliva virgen extra', 100.00, 99.90, 1.00, 0.00, NULL, NULL, '2019-09-10 06:28:57.976416+02', NULL, 899.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (41, 'Lasaña boloñesa', 100.00, 5.60, 6.20, 12.00, 1, NULL, '2019-09-10 10:54:38.590577+02', NULL, 127.00, 0.00, 0.00, 0.00, 0.00, 1.70, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (42, 'Nectarina', 100.00, 0.32, 1.06, 10.55, NULL, NULL, '2019-09-10 19:10:16.904302+02', NULL, 44.00, 0.00, 0.00, 0.00, 0.00, 1.70, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (43, 'Yogur Natural Activia 0%', 125.00, 0.50, 5.10, 5.50, 3, NULL, '2019-09-10 19:12:01.6529+02', NULL, 51.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (44, 'Salmón ahumado', 100.00, 15.20, 22.30, 0.60, 14, NULL, '2019-09-11 08:44:21.966773+02', NULL, 228.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (45, 'Mousse de chocolate', 62.50, 5.00, 3.20, 15.00, 1, NULL, '2019-09-11 08:47:29.087433+02', NULL, 117.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (46, 'Queso Havarti en lonchas', 100.00, 35.00, 20.00, 0.90, 1, NULL, '2019-09-11 08:49:01.127926+02', NULL, 399.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (8, 'Manzana', 100.00, 0.20, 0.30, 14.00, NULL, NULL, '2019-09-06 22:28:33.797846+02', NULL, 52.00, 0.00, 0.00, 0.00, 0.00, 2.02, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (11, 'Huevos', 100.00, 12.10, 12.68, 0.68, NULL, NULL, '2019-09-06 22:40:38.233617+02', NULL, 162.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (4, 'Leche entera', 100.00, 2.00, 3.30, 4.70, NULL, NULL, '2019-09-06 21:58:32.352071+02', NULL, 50.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (12, 'Setas', 100.00, 1.20, 4.25, 0.54, NULL, NULL, '2019-09-07 08:48:01.202385+02', NULL, 33.56, 0.00, 0.00, 0.00, 0.00, 1.90, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (10, 'Gambas', 100.00, 1.80, 18.00, 1.50, NULL, NULL, '2019-09-06 22:38:05.645695+02', NULL, 94.20, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (47, 'Salchichas Gourmet', 100.00, 20.80, 12.30, 0.70, 1, NULL, '2019-09-11 08:53:05.200498+02', NULL, 239.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (48, 'Pan de molde', 100.00, 3.80, 7.77, 49.90, NULL, NULL, '2019-09-11 11:35:07.237965+02', NULL, 272.00, 0.00, 0.00, 0.00, 0.00, 3.60, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (49, 'Ajo', 100.00, 0.23, 4.30, 24.30, NULL, NULL, '2019-09-11 16:00:04.593467+02', NULL, 119.00, 0.00, 0.00, 0.00, 0.00, 1.20, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (53, 'Tomate frito', 100.00, 3.50, 1.50, 9.50, 1, NULL, '2019-09-11 16:22:08.89987+02', NULL, 79.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, 0.00, NULL);
INSERT INTO public.products VALUES (55, 'Plátano', 100.00, 0.27, 1.06, 20.80, NULL, NULL, '2019-09-11 21:06:02.585289+02', NULL, 95.03, NULL, NULL, NULL, NULL, 2.55, NULL, NULL, NULL);
INSERT INTO public.products VALUES (56, 'Leche Entera', 100.00, 3.60, 3.10, 4.60, 16, NULL, '2019-09-11 21:38:54.046659+02', NULL, 63.00, NULL, NULL, NULL, NULL, 0.00, NULL, NULL, NULL);
INSERT INTO public.products VALUES (57, 'Manzana roja deshidratada', 20.00, 0.50, 0.50, 17.00, 1, NULL, '2019-09-11 21:55:45.090247+02', NULL, 73.00, NULL, NULL, NULL, NULL, 2.50, NULL, NULL, NULL);
INSERT INTO public.products VALUES (58, 'Piña deshidratada', 100.00, 0.80, 3.40, 82.00, 1, NULL, '2019-09-11 21:57:50.221022+02', NULL, 314.00, NULL, NULL, NULL, NULL, 9.40, NULL, NULL, NULL);
INSERT INTO public.products VALUES (59, 'Mango deshidratado', 100.00, 1.20, 2.50, 70.00, 1, NULL, '2019-09-11 21:58:32.512495+02', NULL, 317.00, NULL, NULL, NULL, NULL, 8.10, NULL, NULL, NULL);
INSERT INTO public.products VALUES (60, 'Orejones de albaricoque', 100.00, 0.80, 3.70, 60.00, 1, NULL, '2019-09-11 22:01:20.448431+02', NULL, 274.00, NULL, NULL, NULL, NULL, 6.30, NULL, NULL, NULL);

