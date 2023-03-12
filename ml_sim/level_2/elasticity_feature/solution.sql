select sku,
       dates,
       price,
       count(sku) as qty
from 
    transactions
group by
    sku,
    dates,
    price