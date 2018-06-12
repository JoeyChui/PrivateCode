
import xlrd, xlwt

def rdXLSFile(file, sheet = 0):
    xlsTable = []
    f = xlrd.open_workbook(file)
    table = f.sheets()[sheet]
    for ii in range(table.nrows):
        aRow = table.row_values(ii)
        xlsTable.append(aRow)
    return xlsTable

# mergeList(): 合并两个列表
def mergeList(lista, listb):
    for ele in listb:
        lista.append(ele)
    return lista

def wtToXLS(content, filename):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok = True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % filename)
    return

def addQuota(table):
    for ii in range(len(table)):
        table[ii][0] = str(table[ii][0])
        if '.' in table[ii][0]:
            table[ii][0] = table[ii][0][:table[ii][0].find('.')]
        for j in range(len(table[ii])):
            #table[ii][j] = '"' + str(table[ii][j]) + '"'
            table[ii][j] = str(table[ii][j])

    return table


rdFile = r"C:\Users\Joey\Desktop\1234.xlsx"
xlsTable = rdXLSFile(rdFile, 0)
#print(xlsTable)

xlsTable = addQuota(xlsTable)
print(xlsTable)


