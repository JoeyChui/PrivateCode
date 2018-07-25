
import xlrd, xlwt

def rdXLSFile(file):
    xlsTable = []
    f = xlrd.open_workbook(file)
    table = f.sheets()[0]
    for ii in range(table.nrows):
        aRow = table.row_values(ii)
        xlsTable.append(aRow)
    return xlsTable

# mergeList(): 合并两个列表
def mergeList(lista, listb):
    for ele in listb:
        lista.append(ele)
    return lista

def findDataFromdoubanTable(name, doubanTable):
    for ii, row in enumerate(doubanTable):
        if row[0] == name:
            return ii
    return None

def mean(i, j):
    if j == '':
        return j
    if i == '':
        return i
    return round((float(i) + float(j)) / 2, 2)

def merge(row1, row2):
    row1[1] = mean(row1[1], row2[1])
    row1[6] = mean(row1[6], row2[6])
    row1[7] = mean(row1[7], row2[7])
    return row1

def wtToXLS(content, filename):
    workbook = xlwt.Workbook(encoding = 'utf-8')
    booksheet = workbook.add_sheet('Sheet 1', cell_overwrite_ok = True)
    for i, rowVal in enumerate(content):
        for j, colVal in enumerate(rowVal):
            booksheet.write(i, j, colVal)
    workbook.save('%s.xls' % filename)
    return

def mergeData(doubanFile, maoyanFile):
    doubanTable = rdXLSFile(doubanFile)
    maoyanTable = rdXLSFile(maoyanFile)

    bigTable = [['name', 'score', 'director', 'actors', 'id', 'url', 'votes', 'commentNum', 'movieClass', 'ticketoOffice']]
    maoyanTable.pop(0)
    for maoyanRow in maoyanTable:
        ii = findDataFromdoubanTable(maoyanRow[0], doubanTable)
        if ii == None:
            bigTable.append(maoyanRow)
            continue
        row = merge(maoyanRow, doubanTable[ii])
        bigTable.append(row)
        doubanTable.pop(ii)

    bigTable = mergeList(bigTable, doubanTable)
    print(bigTable)
    wtToXLS(bigTable, "MergeData")
    return


doubanFile = "DoubanDianYing.xls"
maoyanFile = "MaoyanDianYing.xls"
