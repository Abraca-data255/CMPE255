import logging
import pandas as pd
from urllib.request import urlopen
from bs4 import BeautifulSoup


# function to extract new york times website published articles links
def new_york_times_sitemap():
    """
    Functions return article links and save them in excel file

    :return: excel file
    """

    # initializing the logger
    logging.basicConfig(filename='../Logs/newyork-times-sitemap-crawler.log',
                        filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')

    # sitemap url
    newyork_sitemap_url = "https://www.nytimes.com/sitemap/{current_year}/{current_month}/{current_date}/"

    # dates configuration
    months_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    dates_list = []
    years_list = ["2020", "2021"]

    # creating dates and appending them in a list
    for date in range(1, 32):
        if date < 10:
            dates_list.append("0" + str(date))
        else:
            dates_list.append(str(date))

    # iterating through all dates and getting all article links
    for year in years_list:
        for month in months_list:
            all_article_links = []
            for date in dates_list:
                # creating sitemap url link
                paper_link = newyork_sitemap_url.format(current_year=year,
                                                        current_month=month,
                                                        current_date=date)
                date_timestamp = year + "-" + month + "-" + date
                try:
                    # parsing the sitemap link
                    html_source = urlopen(paper_link)

                    # reading and extracting href links
                    soup = BeautifulSoup(html_source.read(),
                                         'lxml')
                    for ul in soup.find_all('ul', class_='css-cmbicj'):
                        for li in ul.find_all('li'):
                            a_href = li.find('a')
                            # appending all article links
                            all_article_links.append((date_timestamp,
                                                      a_href['href']))
                except Exception as e:
                    logging.error(e)

            # saving file output in excel files
            file_name = "newyork-times-{year}-{month}.xlsx".format(year=year, month=month)
            newyork_times_articles = pd.DataFrame(all_article_links, columns=['Date', 'Article_Link'])
            newyork_times_articles.to_excel(file_name, index=False)


# function to extract cnbc website published articles links
def cnbc_sitemap():
    """
    Functions return article links and save them in excel file

    :return: excel file
    """

    # initializing the logger
    logging.basicConfig(filename='../Logs/cnbc-sitemap-crawler.log',
                        filemode='w',
                        format='%(name)s - %(levelname)s - %(message)s')

    # sitemap url
    cnbc_sitemap_url = "https://www.cnbc.com/site-map/articles/{current_year}/{current_month}/{current_date}/"

    # dates configuration
    months_list = {"January": "01", "February": "02", "March": "03", "April": "04", "May": "05", "June": "06",
                   "July": "07", "August": "08", "September": "09", "October": "10", "November": "11", "December": "12"}
    dates_list = []
    years_list = ["2020", "2021"]

    # creating dates and appending them in a list
    for date in range(1, 32):
        dates_list.append(str(date))

    # iterating through all dates and getting all article links
    for year in years_list:
        for month in months_list:
            all_article_links = []
            for date in dates_list:
                # creating sitemap url link
                paper_link = cnbc_sitemap_url.format(current_year=year,
                                                     current_month=month,
                                                     current_date=date)

                date_timestamp = year + "-" + months_list[month] + "-" + date
                try:
                    # parsing the sitemap link
                    html_source = urlopen(paper_link)

                    # reading and extracting href links
                    soup = BeautifulSoup(html_source, 'html.parser')
                    for div in soup.find_all('div', class_='SiteMapArticleList-articleData'):
                        for li in div.find_all('li'):
                            a_href = li.find('a')
                            # appending all article links
                            all_article_links.append((date_timestamp,
                                                      a_href['href']))
                except Exception as e:
                    logging.error(e)

                # saving file output in excel files
                file_name = f"cnbc-news-{year}-{months_list[month]}.xlsx"
                cnbc_times_articles = pd.DataFrame(all_article_links, columns=['Date', 'Article_Link'])
                cnbc_times_articles.to_excel(file_name, index=False)


if __name__ == '__main__':
    new_york_times_sitemap()
    cnbc_sitemap()
