select sku,
       dates,
       price,
       count(sku) as qty
from transactions
group by 1, 2, 3