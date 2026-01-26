from superlinked import framework as sl
from schemas.noc_stat import noc_stat_schema

EMBEDDING_MODEL = 'sentence-transformers/all-MiniLM-L6-v2'

noc_name_space = sl.TextSimilaritySpace(
    text=noc_stat_schema.noc,
    model=EMBEDDING_MODEL,
)

year_space = sl.NumberSpace(
    number=noc_stat_schema.year,
    min_value=1900,    # Minimum year
    max_value=2024,   # Maximum year
    mode=sl.Mode.MAXIMUM,
)

population_space = sl.NumberSpace(
    number=noc_stat_schema.population,
    min_value=100000,    # Minimum price
    max_value=1000000000,   # Maximum price
    mode=sl.Mode.MINIMUM,
)

gdp_per_capita_space = sl.NumberSpace(
    number=noc_stat_schema.gdp_per_capita,
    min_value=500,    # Minimum gdp_per_capita
    max_value=100000,   # Maximum gdp_per_capita
    mode=sl.Mode.MAXIMUM,
)

income_group_space = sl.CategoricalSimilaritySpace(
    category_input=noc_stat_schema.income_group,
    categories=[
        'Low income',
        'Lower-middle income',
        'Upper-middle income',
        'High income',
    ],
)

gold_medals_space = sl.NumberSpace(
    number=noc_stat_schema.gold,
    min_value=0,    # Minimum gold medals
    max_value=500,   # Maximum gold medals
    mode=sl.Mode.MAXIMUM,
)

silver_medals_space = sl.NumberSpace(
    number=noc_stat_schema.silver,
    min_value=0,    # Minimum silver medals
    max_value=500,   # Maximum silver medals
    mode=sl.Mode.MAXIMUM,
)

bronze_medals_space = sl.NumberSpace(
    number=noc_stat_schema.bronze,
    min_value=0,    # Minimum bronze medals
    max_value=500,   # Maximum bronze medals
    mode=sl.Mode.MAXIMUM,
)

total_medals_space = sl.NumberSpace(
    number=noc_stat_schema.total_medals,
    min_value=0,    # Minimum total medals
    max_value=1500,   # Maximum total medals
    mode=sl.Mode.MAXIMUM,
)
