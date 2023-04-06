import requests
import webbrowser
from bs4 import BeautifulSoup

url = "https://cs.uwaterloo.ca/~dtompkin/music/year/index.html" #replace with your desired website URL
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

# find the table on the page
table_year = "simple"
table = soup.find("table",table_year)

# find the links in the table
links = []
for tr in table.find_all("tr"):
    row_links = []
    for td in tr.find_all("td"):
        link = td.find("a")
        if link:
            row_links.append(link.get("href"))
    links.append(row_links)

for row_links in links:
    for link_url in row_links:
        # follow the link and get the content of the next page
        response = requests.get(link_url)
        next_soup = BeautifulSoup(response.content, "html.parser")

        # find the table on the page
        table_music = "music"
        table_2nd_page = soup.find("table",table_music)

        link_2nd_page = table_2nd_page.find("a", text = "details...")
        
        # follow the link and get the content of the next page
        response = requests.get(link_2nd_page)
        next_soup = BeautifulSoup(response.content, "html.parser")

        # find the table on the page
        table = soup.find("table")

        # extract the table headers and data
        headers = []
        data = []
        for th in table.find_all("th"):
            headers.append(th.text.strip())
        for tr in table.find_all("tr"):
            row = []
            for td in tr.find_all("td"):
                row.append(td.text.strip())
            if row:
                data.append(row)
        
# create a pandas DataFrame from the data and headers
df = pd.DataFrame(data, columns=headers)

# save the DataFrame to an Excel file
df.to_excel("table.xlsx", index=False)