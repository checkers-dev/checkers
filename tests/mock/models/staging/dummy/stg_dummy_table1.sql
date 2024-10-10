select *
from {{ source('dummy', 'table1')}}
