from AggregateData import AggregateData
from WsbScrape import WsbScrape
from FinanceData import FinanceData
import pandas as pd
from datetime import date

scrape_data = False

if __name__ == '__main__':
    if scrape_data:
        WsbScrape(start_date='1/02/2020', end_date='1/04/2021', random=True)

    sdate = date(2020, 1, 1)
    edate = date(2021, 5, 31)
    dates = pd.date_range(sdate, edate, freq='d').strftime('%Y-%m-%d').to_list()
    aggregate_data_from_raw_table = AggregateData('unique_wsb_submissions', dates=dates)

    if not aggregate_data_from_raw_table.raw_copy_table:
        aggregate_data_from_raw_table.copy_raw_table()
        print('-------------> copied table')

    aggregate_data_from_raw_table.aggregate_data()

    get_finance_data_for_aggregate_table = FinanceData('2020-01-01', '2021-05-31')
    get_finance_data_for_aggregate_table.collect_data()
    get_finance_data_for_aggregate_table.persist_data()
