import traceback

import xlrd
from xlutils import copy
from public import comm_logging
from public import common

def write_Mobfox():
    read_excelName = "DailyReport_Mobfox.xls"
    try:
        nowDate = common.getNowTime()[0:10]
        outPath = "D:/360security/data/"
        read_openPath = (outPath + nowDate + "/" + read_excelName).strip()
        read_workbook = xlrd.open_workbook(read_openPath)

        read_sheetName = read_workbook.sheet_names()[0]
        read_sheet = read_workbook.sheet_by_name(read_sheetName)
        read_numRow, read_numCol = read_sheet.nrows, read_sheet.ncols

        # read_rowList = []
        # for i in range(1, read_numRow + 1):
        #     read_rowList.append(read_sheet.row_values(i))

        write_excelName = nowDate + "_data_total.xls"
        write_openPath = outPath + write_excelName
        write_workbook = copy.copy(xlrd.open_workbook(write_openPath))
        sheet = write_workbook.add_sheet('Mobfox')

        for i in range(0, read_numRow):
            for j in range(1, 10):
                sheet.write(i, j + 1, read_sheet.row_values(i)[j])
        save_excelName = nowDate + "_data_total.xls"
        savePath = outPath + save_excelName
        write_workbook.save(savePath)
        print("  Mobfox  " + "  保存成功")
    except:
        errorTnfo = traceback.format_exc()
        print(errorTnfo)
        comm_logging.myLogger.write_logger(errorTnfo)

if __name__ == '__main__':
    write_Mobfox()