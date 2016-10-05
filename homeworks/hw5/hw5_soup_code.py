response = urlopen("https://www.wunderground.com/history/airport/%s/%s/1/1/CustomHistory.html?dayend=31&monthend=12&yearend=%s" \
                   % ('KATL', '2008', '2008'))
html = response.read()
response.close()

soup = BeautifulSoup(html,"html5lib")

tbody = soup.find('table', id = 'obsTable', class_ = 'responsive obs-table daily').find_all('tbody')