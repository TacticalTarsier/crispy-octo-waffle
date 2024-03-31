with cte_base as (select email_id
                       , sum_amount
                       , max(sum_amount) over() as max_amount
                  from (select email_id
                       , sum(amount) as sum_amount
                  from new_payments
                  where status = 'Confirmed'
                  and mode in ('Visa', 'МИР', 'MasterCard')
                  group by email_id) as sub
                  )
select *
from (
select case
            when sum_amount between 0 and 20000 then '0-20000'
            when sum_amount between 20000 and 40000 then '20000-40000'
            when sum_amount between 40000 and 60000 then '40000-60000'
            when sum_amount between 60000 and 80000 then '60000-80000'
            when sum_amount between 80000 and 100000 then '80000-100000'
            else concat('100000-', max_amount::integer::varchar)
            end as purchase_range
     , count(email_id) as num_of_users
from cte_base
group by 1) as sub
order by case
            when purchase_range = '0-20000' then 1
            when purchase_range = '20000-40000' then 2
            when purchase_range = '40000-60000' then 3
            when purchase_range = '60000-80000' then 4
            when purchase_range = '80000-100000' then 5
            else 6 end