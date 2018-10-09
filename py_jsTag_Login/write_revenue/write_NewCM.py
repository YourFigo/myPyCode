import traceback

import xlrd
from xlutils import copy
from public import comm_logging
from public import common

outPath = "D:/360security/data/"

def write_NewCM():
    read_excelName = "DailyReport_NewCM.xls"
    try:
        nowDate = common.getNowTime()[0:10]
        read_openPath = (outPath + nowDate + "/" + read_excelName).strip()
        read_workbook = xlrd.open_workbook(read_openPath)

        read_sheetName = read_workbook.sheet_names()[0]
        read_sheet = read_workbook.sheet_by_name(read_sheetName)
        read_numRow, read_numCol = read_sheet.nrows, read_sheet.ncols

        write_excelName = nowDate + "_data_total.xls"
        write_openPath = outPath + write_excelName
        write_workbook = copy.copy(xlrd.open_workbook(write_openPath))
        write_sheet = write_workbook.add_sheet('NewCM')

        for i in range(0, read_numRow):
            for j in range(1, 8):
                x = read_sheet.row_values(i)[j]
                if j >= 2 and j <= 7 and i != 0:
                    if x == '':
                        x = 0
                    elif x =='-':
                        x = x
                    else:
                        x = str(x).replace(",","").replace("%","").replace("$","")
                        x = float(x)
                write_sheet.write(i, j + 1, x)

        save_excelName = nowDate + "_data_total.xls"
        savePath = outPath + save_excelName
        write_workbook.save(savePath)
        print("  NewCM  " + "  保存成功")
    except:
        errorTnfo = traceback.format_exc()
        print(errorTnfo)
        comm_logging.myLogger.write_logger(errorTnfo)


if __name__ == '__main__':
    write_NewCM()