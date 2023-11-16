import scraping, pre_processing_for_postgres ,pandas_to_sql

# TODO add logger and make better prints :)

# Scrape and collect data
print('Start scraping...')
scraping.main()
print('Scraping Done')

# Pre-processing 
print('Start Pre-processing...')
pre_processing_for_postgres.main()
print('Pre-processing Done')

# Pre-processing 
print('Adding data to DB tables...')
pandas_to_sql.main()
print('All tasks completed')