from superlinked import framework as sl

from spaces.noc_space import (
    noc_name_space,
    year_space,
    population_space,
    gdp_per_capita_space,
    income_group_space,
    gold_medals_space,
    silver_medals_space,
    bronze_medals_space,
    total_medals_space,
)
from schemas.noc_stat import noc_stat_schema

noc_index = sl.Index(
    spaces=[
        noc_name_space,
        year_space,
        population_space,
        gdp_per_capita_space,
        income_group_space,
        gold_medals_space,
        silver_medals_space,
        bronze_medals_space,
        total_medals_space,
    ],
    fields=[
        noc_stat_schema.year,
        noc_stat_schema.population,
        noc_stat_schema.gdp_per_capita,
        noc_stat_schema.gold,
        noc_stat_schema.silver,
        noc_stat_schema.bronze,
        noc_stat_schema.total_medals,
        noc_stat_schema.income_group,
    ],

)
