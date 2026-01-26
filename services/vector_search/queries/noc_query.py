from superlinked import framework as sl

from indexes.noc_index import noc_index
from schemas.noc_stat import noc_stat_schema
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
from config import openai_config

# Define the semantic search query with parameterized weights and filters
search_query = (
    sl.Query(
        noc_index,
        weights={
            noc_name_space: sl.Param('noc_name_weight'),
            year_space: sl.Param('year_weight'),
            population_space: sl.Param('population_weight'),
            gdp_per_capita_space: sl.Param('gdp_per_capita_weight'),
            income_group_space: sl.Param('income_group_weight'),
            gold_medals_space: sl.Param('gold_medals_weight'),
            silver_medals_space: sl.Param('silver_medals_weight'),
            bronze_medals_space: sl.Param('bronze_medals_weight'),
            total_medals_space: sl.Param('total_medals_weight'),
        },
    )
    # Explicit mention to the schema
    .find(noc_stat_schema)
    # Define natural query as a way to decompose the user's query
    .with_natural_query(sl.Param('natural_query'), openai_config)
    .similar(
        noc_name_space,
        sl.Param(
            'noc_query',
            description="The user's natural language query for \
                NOC statistics search.",
        ),
    )
    # Filters - these are hard constraints
    .filter(
        noc_stat_schema.year
        == sl.Param(
            'year',
            description='Used to filter by Olympic year',
        ),
    )
    .filter(
        noc_stat_schema.population
        >= sl.Param(
            'min_population',
            description='Used to find NOCs with population \
                equal to or greater than the specified number',
        ),
    )
    .filter(
        noc_stat_schema.gdp_per_capita
        >= sl.Param(
            'min_gdp_per_capita',
            description='Used to find NOCs with GDP per capita \
                equal to or greater than the specified number',
        ),
    )
    .filter(
        noc_stat_schema.gold
        >= sl.Param(
            'min_gold_medals',
            description='Used to find NOCs with gold medals \
                equal to or greater than the specified number',
        ),
    )
    .filter(
        noc_stat_schema.silver
        >= sl.Param(
            'min_silver_medals',
            description='Used to find NOCs with silver medals \
                equal to or greater than the specified number',
        ),
    )
    .filter(
        noc_stat_schema.bronze
        >= sl.Param(
            'min_bronze_medals',
            description='Used to find NOCs with bronze medals \
                equal to or greater than the specified number',
        ),
    )
    .filter(
        noc_stat_schema.total_medals
        >= sl.Param(
            'min_total_medals',
            description='Used to find NOCs with total medals \
                equal to or greater than the specified number',
        ),
    )
    .filter(
        noc_stat_schema.income_group
        == sl.Param(
            'income_group',
            description='Used to filter NOCs by income group',
        ),
    )
    .limit(sl.Param('limit'))
    .select_all()
)
