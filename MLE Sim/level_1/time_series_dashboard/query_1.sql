select date_trunc('week', date)::date as weeks
     , sum(amount)                    as sum_receipt
from new_payments
where status = 'Confirmed'
group by date_trunc('week', date)
order by 1;