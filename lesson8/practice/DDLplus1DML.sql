CREATE TABLE category (
	id INTEGER primary key AUTOINCREMENT,
	category_name TEXT NOT NULL
);

create UNIQUE index i_u_category_name on category(upper(category_name));


create table product (
	id integer primary key AUTOINCREMENT,
	category_id integer not null references category(id) default 0,
	product_name text not null,
	price integer,
	count_in_market integer not null default 0,
	count_in_warehouse integer not null default 0,
	constraint c_check_cin_mrkt_cnt check (count_in_market >= 0),
	constraint c_check_cin_wrhs_cnt check (count_in_warehouse >= 0)
)
;

create UNIQUE index i_u_product_category on product(upper(product_name),category_id);

insert into category 
values (0, 'Other');

insert into product(category_id,product_name,price,count_in_market,count_in_warehouse)
values (0, 'Test product', 5699, 43, 12);

commit;