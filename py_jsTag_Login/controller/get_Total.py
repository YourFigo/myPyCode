from write_revenue import write_Adview
from write_revenue import write_Mobfox
from write_revenue import write_Mopub
from write_revenue import write_NewCM
from write_revenue import write_Openx
from write_revenue import write_Pubnative
from write_revenue import write_Smaato
from write_revenue import write_Solo
from write_revenue import write_Tappx
from write_revenue import write_cmcm
from write_revenue import write_AOL

import xlrd
import xlwt
from xlutils import copy

from public.common import getNowTime

outPath = "D:/360security/data/"

#新建workbook
def creatWorkbook():

    save_excelName = getNowTime()[0:10] + "_data_total.xls"
    totalWorkbook = xlwt.Workbook(encoding='utf-8')
    sheetNone = totalWorkbook.add_sheet('汇总')
    totalWorkbook.save(outPath + save_excelName)

#复制汇总数据
def copySheet():
    #读取原日报数据
    read_excelName = "2018.814日报-JS+tag.xls"
    outPath = "D:/360security/data/"
    read_openPath = (outPath + read_excelName).strip()
    read_workbook = xlrd.open_workbook(read_openPath)

    read_sheetName = read_workbook.sheet_names()[13]
    read_sheet = read_workbook.sheet_by_name(read_sheetName)
    read_numRow, read_numCol = read_sheet.nrows,read_sheet.ncols
    #将汇总 sheet 数据 加载到list
    read_rowList = []
    for i in range(0, read_numRow):
        read_rowList.append(read_sheet.row_values(i))


    #读取新建的表格的sheet
    write_excelName = getNowTime()[0:10] + "_data_total.xls"
    write_openPath = outPath + write_excelName
    write_workbook = copy.copy(xlrd.open_workbook(write_openPath))
    write_sheet = write_workbook.get_sheet(0)
    # write_num_row = xlrd.open_workbook(write_openPath).sheet_by_index(0).nrows

    #复制数据
    for i in range(0, read_numRow):
        for j in range(0, read_numCol):
            write_sheet.write(i, j, read_rowList[i][j])
    savePath = outPath + write_excelName
    write_workbook.save(savePath)

def get_Total():
    print("新建数据总表.....")
    creatWorkbook()

    print("正在写入 Mobfox .........")
    write_Mobfox.write_Mobfox()
    print("正在写入 Smaato.........")
    write_Smaato.write_Smaato()
    print("正在写入 AOL.........")
    write_AOL.write_AOL()
    print("正在写入 cmcm.........")
    write_cmcm.write_cmcm()
    print("正在写入 cmcm.........")
    write_Tappx.write_Tappx()
    print("正在写入 Mopub.........")
    write_Mopub.write_Mopub()
    print("正在写入 NewCM ........")
    write_NewCM.write_NewCM()
    print("正在写入 Openx ........")
    write_Openx.write_Openx()
    print("正在写入 Pubnative ........")
    write_Pubnative.write_Pubnative()
    print("正在写入 Solo ........")
    write_Solo.write_Solo()
    print("正在写入 Adview ........")
    write_Adview.write_Adview()

    print("保存路径： ",outPath)
    print("爬取数据汇总成功")

if __name__ == '__main__':
    get_Total()

