from os import listdir
from bs4 import BeautifulSoup
from pandas import DataFrame

#
# So what we're trying to do here is to parse the data from the html file
# and find all the reinvestment percentages 
#

#TODO(ian): Turn into a "Parser" class which the "UtimcoBase" class
# inherits from so that each class can parse inherently

excel_data = []

def parse_short_name(soup):
    #Parse the short name
    if soup.find("td", attrs={"colspan":"3"}):
        soups = []
        for s in soup.find_all("td", attrs={"colspan":"3"}):
            soups.append(s)
        if len(soups) > 0:
           return soups[0].text.encode('utf-8')
    return "No Short Name"

def parse_prin_account(soup):
    finds = []
    for find in soup.find_all("td"):
        finds.append(find)
    i = 1
    for find in finds:
        if "UTIMCO Principal" in find.text.encode('utf-8'):
            return finds[i].text.encode('utf-8')
        i +=1
    return "No Principal"

def parse_comp_acct(soup):
    finds = []
    for find in soup.find_all("td"):
        finds.append(find)
        
    i = 1
    for find in finds:
        if "Component Principal" in find.text.encode('utf-8'):
            return finds[i].text.encode('utf-8')
        i +=1
    return "No Comp Prin"

def parse_market_values(f, soup):
    data = []
    finds = []
    for find in soup.find_all("a", href=True):
        finds.append(find)
        
    i = 1
    for find in finds:
        if 'javascript:void(0)'  in find.text.encode('utf-8'):
            data.append(find)
    
    if len(data) > 0:
        return data[-1]
    
    return "No Market Value"

def parse_data(file_name):
    i = 1
    data = []
    global excel_data
    with open(file_name, 'r') as f:
        soup = BeautifulSoup(f.read(), 'html.parser')
        
        #Parse the short name
        data.append(parse_short_name(soup))
        
        #Parse the UTIMCO PRINCIPAL ACCOUNT NUMBER
        data.append(parse_prin_account(soup))

        #Parse the COMPONENT PRINCIPAL ACCOUNT NUMBER
        data.append(parse_comp_acct(soup))
        
        #Parse the reinvestment percentages
        #TODO(ian): Turn this into a method.
        for i in xrange(0, 5):
            data.append('None')
        if soup.find("td", attrs={'width': '45'}):
            for i, find in enumerate(soup.find_all("td", attrs={'width':'45'})):
                percent = find.text.encode('utf-8').split()[0]
                if percent == b'\xc2\xa0':
                    data[-5 + i] = '0'
                else:
                    data[-5 + i] = percent

    # clean the data up
    i = 0
    replace_list = ['\n', ' ',   b'\xc2\xa0']
    for item in data:
        for rep in replace_list:
            data[i] = item.strip().replace(rep, '')
        i += 1
    excel_data.append(data)

def write_to_excel(data):
    # Model the data as such:
    #     List [
    #       0    Principle Account,
    #       1    Component Principle Account,
    #       2    Endowment Name,
    #       3    Long Term, 
    #       4    Temp
    #       5    Misc
    #          ]

    variables = [[],[],[],[],[],[],[],[]]
    col_names = ['Endowment Name', 'Component Principle Account', 'Principle Account', 'Long Term', 'Temp', 'Misc', 'Misc2', 'Misc2']
    
    
    for i in data:
        for x, j in enumerate(i):
            if x > len(variables):
                variables.append([])
            variables[x].append(j)
    

    df = DataFrame(variables)
    
    df = df.T
    df.columns = col_names
    df.to_excel("test.xlsx", sheet_name="Data", index=False)

if __name__ == "__main__":
    for file in listdir("./utimco/profiles"):
        #if file == "/57350004.html":
        parse_data('./utimco/{}'.format(file))
    write_to_excel(excel_data)
