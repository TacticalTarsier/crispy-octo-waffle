select distinct toDate(timestamp) as day,
       uniqExact(user_id) over(order by day range between 6 preceding and current row) as wau
from default.churn_submits