sql_dict = dict(
    insert_category='insert into category(category_name) values (?)',
    insert_product='insert into product(category_id, product_name, price, count_in_market, count_in_warehouse) \
                    values (?, ?, ?, ?, ?)',
    update_product='update product\
                    set count_in_market = coalesce(?, count_in_market),\
                    count_in_warehouse = coalesce(?, count_in_warehouse),\
                    product_name = coalesce(?, product_name),\
                    price = coalesce(?, price),\
                    where product.id = ?\
                      and (count_in_market <> coalesce(?, count_in_market)\
                      or count_in_warehouse <> coalesce(?, count_in_warehouse)\
                      or product_name <> coalesce(?, product_name)\
                      or price <> coalesce(?, price))',
    get_product_by_cat_name_prod_name='select\
                                        id,\
                                        product_name,\
                                        price,\
                                        count_in_market,\
                                        count_in_warehouse,\
                                        count_in_market + count_in_warehouse overall_count\
                                      from product\
                                      where category_id = (select id from category where category_name = ?)\
                                        and product_name = ?',
    select_products_by_category_name='select\
                                            id,\
                                            product_name\
                                        from product\
                                        where category_id = (select id from category where category_name = ?)',
    select_categories='select\
                         id,\
                         category_name\
                       from category\
                       where category_name = coalesce(?, category_name)\
                       order by case when id=0 then \'zzzzzzzzzz\' else category_name end'
)