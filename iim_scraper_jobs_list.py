#!/usr/bin/env python3
# https://github.com/PrinceShaji
""" Module to scrape the number of jobs with basic info from iimjobs.com """

import itertools
import csv
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def scrape_all_jobs(base_url):
    """ base_url should be a valid url two placeholder {} for incrementing job number and page.\n
    example: https://www.iimjobs.com/search/All-3_6_36_1_40_41_8_37_4_5_2_38_7-0-{}-{}.html \n
    This function returns a list with all scraped data as a dictionary with following keys.\n
    'job_id', 'job_title', 'job_location', 'date_posted', 'experience_min', 'experience_max'"""

    # For storing all the scraped data.
    scraped_data = []

    for i in itertools.count():
        # Jobs start from 0, and page number starts from 1.
        url = base_url.format((i*100), (i+1))
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'lxml')
        jobs_table = soup.find_all('div', {'class': 'jobRow'})

        # Breaking if there are no job postings, aka the page after the last page.
        if not jobs_table:
            break
        else:
            for jobs in jobs_table:
                template = {}
                template['job_id'] = jobs.find_all('a', attrs={'class': 'mrmob5 hidden-xs'})[0].get('data-jobid')
                template['job_title'] = jobs.find_all('a', attrs={'class': 'mrmob5 hidden-xs'})[0].text.strip()
                template['job_location'] = jobs.find_all('span', attrs={'class': 'disp768 mobloc'})[0].get('title')
                template['date'] = jobs.find_all('span', {'class': 'gry_txt txt12 original'})[0].text
                # Getting min and max experience.
                experience = template['job_title'].split('(')[-1].split(' ')[0].split('-')
                template['min_exp'] = experience[0]
                template['max_exp'] = experience[1]

                scraped_data.append(template)

    return scraped_data

if __name__ == "__main__":
    BASE_URL = 'https://www.iimjobs.com/search/All-3_6_36_1_40_41_8_37_4_5_2_38_7-0-{}-{}.html'
    SCRAPED_DATA = scrape_all_jobs(BASE_URL)
    FILENAME = str(datetime.now()) + '.csv'

    with open(FILENAME, 'w', newline='') as csvfile:
        FIELDNAMES = ['job_id', 'min_exp', 'max_exp', 'job_title', 'job_location', 'date']
        WRITER = csv.DictWriter(csvfile, fieldnames=FIELDNAMES)
        WRITER.writeheader()

        for jobs in SCRAPED_DATA:
            WRITER.writerow(jobs)
    print(f'Number of jobs: {len(SCRAPED_DATA)}')
