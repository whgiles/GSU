from AggregateData import AggregateData
from WsbScrape import WsbScrape
from FinanceData import FinanceData

scrape_data = False

if __name__ == '__main__':
    if scrape_data:
        WsbScrape(start_date='4/01/2021', end_date='4/02/2021', random=True)

    aggregate_data_from_raw_table = AggregateData('unique_wsb_submissions', ['2020-01-02', '2020-01-04'])
    print(aggregate_data_from_raw_table.raw_copy_table)

    if not aggregate_data_from_raw_table.raw_copy_table:
        aggregate_data_from_raw_table.copy_raw_table()
        print('-------------> copied table')

    aggregate_data_from_raw_table.aggregate_data()

    yfinance_data_to_aggregate_table = FinanceData()
