from superlinked import framework as sl


class NOCStat(sl.Schema):
    id: sl.IdField
    noc: sl.String  # Here, we will concat NOC + year + total medals
    year: sl.Integer
    population: sl.Integer
    gdp_per_capita: sl.Float
    income_group: sl.String
    athletes_sent: sl.Integer
    sports_participated: sl.Integer
    gold: sl.Integer
    silver: sl.Integer
    bronze: sl.Integer
    total_medals: sl.Integer


noc_stat_schema = NOCStat()
