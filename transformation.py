import sqlite3
import xlrd


# 建立数据库
def createDataBase():
    cn = sqlite3.connect('retea.db')

    cn.execute('''CREATE TABLE IF NOT EXISTS TB_TEA
         (id INTEGER PRIMARY KEY AUTOINCREMENT,
         name TEXT,
         details TEXT,
         score float,
         number int,
         price int,
         address TEXT);''')

    cn.commit()
    cn.close()


# 解析excel文件并将其存储到数据库
def readExcel(filename, cn):
    # 读取
    workbook = xlrd.open_workbook(filename)
    # 获取sheet
    sheet_name = workbook.sheet_names()[0]
    sheet = workbook.sheet_by_name(sheet_name)

    for i in range(1, sheet.nrows):
        temp = []
        for j in range(0, sheet.ncols):
            temp.append(sheet.cell(i, j).value)

        cn.execute("insert into TB_TEA ('name', 'details', 'score', 'number', 'price', 'address') "
                   'values("%s","%s","%s","%s","%s","%s")'
                   % (temp[0], temp[1], temp[2], temp[3], temp[4], temp[5]))

        # itemCount = itemCount + 1
        # if itemCount != 0:
        cn.commit()
        cn.close


# 使用上面的两个函数
def importData(path):
    createDataBase()
    database = sqlite3.connect("tea.db")
    readExcel(path, database)


# 显示茶饮名单里的信息
def show(filename):
    conn = sqlite3.connect(filename)
    c = conn.cursor()
    print("\nThe %s information is as follows:" % filename)

    cursor = c.execute('SELECT name, details, score, number, price, address from TB_TEA')
    for row in cursor:
        print("name = ", row[0])
        print("details = ", row[1])
        print("score = ", row[2])
        print("number = ", row[3])
        print("price = ", row[4])
        print("address = ", row[5], "\n")

    print("\n\t\tEND")
    conn.close()


path = input("Please enter the excel file's name:")
importData(path)
show("tea.db")
