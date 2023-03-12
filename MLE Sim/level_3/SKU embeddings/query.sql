with t1 as (select user_id,
                   item_id,
                   sum(units) as qty
            from default.karpov_express_orders
            where toDate(timestamp) between %(start_date)s and %(end_date)s
            group by user_id,
                     item_id),
      t2 as (select item_id,
                    round(avg(price), 2) as price
             from default.karpov_express_orders
             where toDate(timestamp) between %(start_date)s and %(end_date)s
             group by item_id)
select t1.user_id,
       t1.item_id,
       t1.qty,
       t2.price
from t1
join t2
on t1.item_id = t2.item_id
order by user_id, item_id