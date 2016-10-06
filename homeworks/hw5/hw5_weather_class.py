class weather:
    
    def __init__(self):
        self.begin = None
        self.end = None
        self.icao = None
        self.tbody = None
        self.y = None
        self.m = None
        self.d = None
        self.icao = None

    global sql
    
    def fetch (self, icao, date):

        response = urlopen("https://www.wunderground.com/history/airport/%s/%s/1/1/CustomHistory.html?dayend=31&monthend=12&yearend=%s" \
                           % (icao, date, date))
        html = response.read()
        response.close()

        soup = BeautifulSoup(html,"html5lib")

        tbody = soup.find('table', id = 'obsTable', class_ = 'responsive obs-table daily').find_all('tbody')

        return tbody
    
    def callback (self, row):
    
        if 'avg' in row.text:
            self.m += 1
            self.d = 0

        #print(self.y, self.m, self.d)

        if self.d != 0:
            td = row.find_all('td')

            MaxT = td[2].text.strip()
            MeanT = td[1].text.strip()
            MinT = td[3].text.strip()
            MaxH = td[8].text.strip()
            MeanH = td[7].text.strip()
            MinH = td[9].text.strip()
            Prep = td[-2].text.strip()
            Date = datetime(self.y, self.m, self.d)

            #print(MaxT, MeanT, MinT, MaxH, MeanH, MinH, Prep)
            
            sql.cursor.execute("""INSERT INTO Weather (ICAO, Date, MaxT, MeanT,
                            MinT, MaxH, MeanH, MinH, Prep) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                                  (self.icao, Date, MaxT, MeanT, MinT, MaxH, MeanH, MinH, Prep))

        self.d += 1

    def Populate_data (self, begin, end, icao):
    
        self.icao = icao
        
        for i in range(begin, end+1):

            tbody = self.fetch(icao, i)

            self.y = i
            self.m = 0
            self.d = 0

            a = list(map(self.callback, tbody))