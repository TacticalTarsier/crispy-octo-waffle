select
  vendor,
  count(distinct brand) as brand
from
  sku_dict_another_one
group by
  vendor
order by brand desc
limit 10