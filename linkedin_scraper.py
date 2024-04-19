import requests
import os
import json
from selenium import webdriver
from bs4 import BeautifulSoup

# url = 'https://arxiv.org/abs/2404.04253'
# URL to scrape
def single_page_scraper(url):
    # Send a GET request to the URL
    driver = webdriver.Chrome()
    driver.get(url)
    # html = requests.get(url).response
    html = driver.page_source

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html, 'html.parser')

    body = soup.body
    print(body)
    # text = body.get_text(separator=' ', strip=True)
    with open("jd.txt", "w") as file:
        file.writelines(str(body))

    # # Extract contents based on the provided web structure descriptions
    # # body = soup.find('body', class_='render-mode-BIGPIPE nav-v2 ember-application icons-loaded boot-complete')
    # body = soup.find('body')
    # print(body)
    # div_application_outlet = body.find('div', class_='application-outlet')
    # div_authtication_outlet = div_application_outlet.find('div', class_='authtication_outlet')
    # div_scaffold_layout = div_authtication_outlet.find('div', class_='scaffold-layout scaffold-layout--breakpoint-xl scaffold-layout--list-detail scaffold-layout--reflow scaffold-layout--has-list-detail jobs-search-two-pane__layout')
    # div_scaffold_layout_inner = div_scaffold_layout.find('div', class_='scaffold-layout__row scaffold-layout__content scaffold-layout__content--list-detail')
    # scaffold_layout_main = div_scaffold_layout_inner.find('main', id='main')
    # div_scaffold_layout_container = scaffold_layout_main.find('div', class_='scaffold-layout__list-detail-container')
    # div_scaffold_layout_detail = div_scaffold_layout_container.find('div', class_='scaffold-layout__list-detail-inner scaffold-layout__list-detail-inner--grow')
    # div_scaffold_layout_detail_overflow = div_scaffold_layout_detail.find('div', class_='scaffold-layout__detail overflow-x-hidden jobs-search__job-details')
    # div_job_search = div_scaffold_layout_detail_overflow.find('div', class_='jobs-search__job-details--wrapper')
    # div_job_search_container = div_job_search.find('div', class_='jobs-search__job-details--container')
    # div_job_view_layout = div_job_search_container.find('div', class_='job-view-layout jobs-details')
    # div_job_view_firstchild = div_job_view_layout.find_all('div')[0]
    # div_job_detail_main = div_job_view_firstchild.find('div', class_='jobs-details__main-content jobs-details__main-content--single-pane full-width')
    # div_job_detail_all_children = div_job_detail_main.find_all('div')
    # div_job_detail_firstchild = div_job_detail_all_children[0]
    # div_job_detail_secondchild = div_job_detail_all_children[1]

    # div_t_14 = div_job_detail_firstchild.find('div', class_='t-14')
    # div_relative_job_detail = div_t_14.find('div', class_='relative job-details-jobs-unified-top-card__container--two-pane')
    # div_relative_job_firstchild = div_relative_job_detail.find_all('div')[0]
    # div_position = div_relative_job_firstchild.find('div', class_='display-flex justify-space-between flex-wrap')
    # div_job_detail_unified = div_relative_job_firstchild.find('div', class_='job-details-jobs-unified-top-card__primary-description-container')
    # div_mt2_mb2 = div_relative_job_firstchild.find('div', class_='mt2 mb2')
    # div_mt2_mb2_ul = div_mt2_mb2.find('ul')
    # div_mt2_mb2_ul_li = div_mt2_mb2_ul.find_all('li')

    # div_mt2_mb2_job_type = div_mt2_mb2_ul_li[0]
    # div_mt2_mb2_company = div_mt2_mb2_ul_li[1]
    # div_mt2_mb2_alumni = div_mt2_mb2_ul_li[2]
    # div_mt2_mb2_skills = div_mt2_mb2_ul_li[3]

    # div_jobs_box = div_job_detail_secondchild.find('div', class_='jobs-box--fadein jobs-box--full-width jobs-box--with-cta-large jobs-description jobs-description--reformatted mt4')
    # div_jobs_description_container = div_jobs_box.find('div', class_='jobs-description__container')
    # div_jobs_description_content = div_jobs_description_container.find('div', class_='jobs-description__content jobs-description-content')
    # div_jobs_box_content = div_jobs_description_content.find('div', id='job-details')
    # div_mt4 = div_jobs_box_content.find('div', class_='mt4')


    # return div_mt2_mb2_job_type.text, div_mt2_mb2_company.text, div_mt2_mb2_alumni.text, div_mt2_mb2_skills.text, div_mt4.text

single_page_scraper('https://www.linkedin.com/jobs/search/?alertAction=viewjobs&currentJobId=3767462861&f_E=2%2C3&f_TPR=r86400&geoId=90000084&keywords=machine%20learning&location=&origin=JOB_SEARCH_PAGE_SEARCH_BUTTON&refresh=true')
