from pprint import pprint
from pathlib import Path

from superlinked import framework as sl
import pandas as pd

from settings import Settings
from schemas.noc_stat import noc_stat_schema
from indexes.noc_index import noc_index
from queries.noc_query import search_query

settings = Settings()


def main():
    source = sl.InMemorySource(
        noc_stat_schema,
        parser=sl.DataFrameParser(schema=noc_stat_schema),
    )

    executor = sl.InMemoryExecutor(sources=[source], indices=[noc_index])
    df = pd.read_csv(Path(settings.dataset.path))
    df['id'] = range(1, len(df) + 1)
    df.columns = df.columns.str.lower()

    app = executor.run()
    source.put([df])

    results = app.query(
        search_query,
        natural_query='Which top-3 best SEA country in 2016?',
        limit=3,
    )

    pprint(results.entries)


if __name__ == '__main__':
    main()
