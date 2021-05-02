#pdf extractor

import camelot
from tabula import read_pdf
from tabulate import tabulate

###find out what week we are in and sub in here
week = 0
page1 = 2*week
page2 = page1 +1
meal = 0
week_meal= 3*week + meal


# directory for where menu is
menu = "menu.pdf"

# a func that inputs the week and finds the corresponding table
def get_week_menu(week_meal):
    thisweek = tables[week_meal]
    return thisweek


#tables = camelot.read_pdf(menu, pages = str(page1), flavor='stream')


'''this is an attempt to define the weeks menus as the seperate tables
week_1 = tables[0]
week_2 = tables[0]
week_3 = tables[0]
week_4 =tables[0]
'''

#converts each page of menu in .html file
for i in range(1,9):
    print(i)
    tables = camelot.read_pdf(menu, pages='%d' %  i) #table_regions=["95,36,660,1176"],)
    try:
        print (tabulate(tables[0].df))
        print(tables[0])
        print(tables[1])
        tables[0].to_html(str(str(i) + ".html"))
        tables[1].to_html(str(str(int(i)+0.5) + ".html"))
        #print (tabulate(tables[1].df))
    except IndexError:
        print('NOK')

'''
print(get_week_menu(week_meal).df) #prints the respective table for the week
print(get_week_menu(week_meal))
print(week_meal)
'''

#get_week_menu(week_meal).to_csv("menu.csv")


