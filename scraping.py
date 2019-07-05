#coding:utf-8
#---------------------------------IMPORT ------------------------------------#
from bs4 import BeautifulSoup
import requests
import pandas as pd
#----------------------------------------------------------------------------#
#-------------------------------CONSTANTS------------------------------------#
web_start = 0#web page start number
web_end = 500#wen pahe end number
titles = [] #LIST OF JOBS TITLE
companies = [] # LIST OF COMPANIES
locations = []# LIST OF LOCATIONS
salaries = []# LIST OF SALARIES
summaries = []#JOB SUMMARY LIST
urls = []#url of  jobs
#url = "https://ca.indeed.com/jobs?q=&l=canada&start="#url 
url_1 = "https://ca.indeed.com/jobs?q="
url_2 = "&l=Canada&radius=75&start="
company_name = ['PWC','EY','BDO', 'MNP','Grant Thornton',
'Accenture','ZS associate','A.T. Kearney','Deloitte','KPMG'
'Capgemini','Tata Consultancy Services','Cognizant Technology Solutions',
'Cisco Systems Consulting','Infosys Consulting','CGI Group','Mercer LLC',
'IBM', 'SAP Services Consulting','Oracle Consulting',
'Oliver Wyman','Aon Hewitt','FTI Consulting, Inc.',
'Sapient Corporation','Hitachi Consulting','Navigant Consulting, Inc.',
'Protiviti','L.E.K. Consulting','Simon-Kucher & Partners','Arthur D. Little',
'Birch Hill Equity Partners',
'Crestview Partners','Hellman & Friedman','TPG Capital','CPPIB',
'BELL','ROGERS','CIBC','RBC','TD','BMO','Scotiabank','3M Canada Company',
'Adobe Systems Canada Inc.','Air Canada','Bank of Canada',
'Best Buy Canada Ltd','Canada Revenue Agency','Canadian Tire Corporation Limited',
'Cargill Limited','Desjardins Group','Fidelity Canada',
'Ford Motor Company of Canada',"L'Oréal Canada Inc.",
'Loblaw Companies Limited','PepsiCo Canada',
'Procter & Gamble Inc.','Salesforce','Uber','facebook','google','amazon',
'Samsung Electronics Canada Inc.','Shopify Inc',
'Thomson Reuters Canada Limited','Toyota Motor Manufacturing Canada Inc.'
]# list of company
headers = ["Title","Location","Company","Salary", "Summary","url"]
df = pd.DataFrame(columns = headers)# HEADER OF CSV FILE
#-----------------------------------------------------------------------------#
#----------------------------------FUNCTIONS----------------------------------#
#-------------------job_location----------------------------------------------#
def job_location(soup): 
    """
    Get the job location from a given soup object
    
    Parameters:
        soup: the soup object
        
    Returns:
    """
    for div in soup.find_all(class_ = 'result'):
        for city in div.find_all('div',{'class':'recJobLoc'}):
           locations.append(city.get('data-rc-loc'))  
    return
#-----------------------------------------------------------------------------#
#-----------------------------------job_salary--------------------------------#
def job_salary(soup): 
    """
    Get the job salary from a given soup object
    
    Parameters:
        soup: the soup object
        
    Returns:
    """
    for div in soup.find_all(class_ = 'result'):
        try:
          salaries.append(div.find('span',{'class':'no-wrap'}).text)
        except:
            salaries.append('Nothing_found')
    return
#-----------------------------------------------------------------------------#
#----------------------------job_summary--------------------------------------#
def job_summary(soup): 
   """
    Grab all  job posting links from a Indeed search result page using the given soup object
    
    Parameters:
        soup: the soup object corresponding to a search result page
                e.g. https://ca.indeed.com/jobs?q=data+scientist&l=Winnipeg&start=10
        urls: a list of job posting URL's (when num_pages valid)
        full_url: full url of the job
        partial_url : parttial of the job url
        info_page: page contains the job description
    
    Returns:
    
   """
    
   for sjcl in soup.find_all('div',{'class':'sjcl'}):
       for company in sjcl.find_all('span',{'class':'company'}):
            companies.append(company.text.strip())
   for link in soup.find_all('div',{'class':'title'}):
        titles.append(link.a.get('title'))
        partial_url = link.a.get('href')
        full_url = "https://ca.indeed.com/"+partial_url
        urls.append(full_url)
        new_page = requests.get(full_url)
        new_soup = BeautifulSoup(new_page.text,'lxml')
        for description in new_soup.find_all('div',{'class':'jobsearch-jobDescriptionText'}):
            summaries.append(description.text.strip("\n"))
   return
#-----------------------------------------------------------------------------#
#-----------------------------------MAIN--------------------------------------#
def main():
    '''
    Puting all information together
    
    Parameters:
        df: the data frame contains all information of job
        soup: given the url of a page, this function returns the soup object.
        
    Returns:
    '''
    for name in company_name:
        url = url_1 + name + url_2
        for start in range(web_start, web_end, 10):
            page = requests.get(url + str(start))
            soup = BeautifulSoup(page.text, 'lxml')
            job_summary(soup)
            job_salary(soup)
            job_location(soup)
    return   
#-----------------------------------------------------------------------------#
#----------------------FUNCTION CALLS-----------------------------------------#        
main()
count = 0
while count < len(urls)*10:
    df = df.append({"Title":titles[count//10],
                    "Location":locations[count//10],
                    "Company":companies[count//10],
                    "Salary":salaries[count//10],
                    "Summary":summaries[count//10],
                    "url":urls[count//10]},ignore_index=True)
    count += 10
df.to_csv('C:\\Users\\raymond\\Desktop\\Scraping_From_Indeed4.csv',index=False)
      
      
    







