import datetime
import uuid
from typing import List, Iterator

from analytics_api.utils.errors import NoDataError


def _extract_table_year(table_name: str) -> int:
    return int(table_name.split('_')[-1])


def get_table_names_with_start_end_dates(start_date: datetime.datetime,
                                         end_date: datetime.datetime,
                                         tables: List) -> List:
    table_names = [table for table in tables
                   if (_extract_table_year(table) >= start_date.year)
                   and (_extract_table_year(table) <= end_date.year)
                   ]
    return table_names


def _create_union_query_between_different_tables(table_names: Iterator[str],
                                                 common_columns: Iterator[str] = ('*',),
                                                 ) -> str:
    queries = map(lambda table_name: f"SELECT {', '.join(common_columns)} FROM `{table_name}`",
                  table_names)
    return " UNION ALL\n".join(queries)


def fill_sql_from_clause_using_table_names_and_columns(sql: str, table_names: List, columns: Iterator = ('*',),
                                                       tables_keyword: str = 'tables'):
    if not len(table_names):
        raise NoDataError

    unique_temporary_name = f"{uuid.uuid3(uuid.NAMESPACE_OID, ''.join(table_names))}"

    with_clause = f"""WITH `{unique_temporary_name}` AS
                  ({_create_union_query_between_different_tables(table_names, columns)})\n"""
    sql = sql.replace('WITH', ',')

    sql = sql.replace(f'{{{tables_keyword}}}', unique_temporary_name)
    return f"""{with_clause}\n{sql}"""
