import xlrd
from xlutils import copy
import traceback

from public import comm_logging
from public import common

outPath = "D:/360security/data/"

def write_cmcm():
    read_excelName = "DailyReport_cmcm.xls"
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
        write_sheet = write_workbook.add_sheet('cmcm')

        for i in range(0, read_numRow):
            for j in range(0, 12):
                write_sheet.write(i, j + 2, read_sheet.row_values(i)[j])

        save_excelName = nowDate + "_data_total.xls"
        savePath = outPath + save_excelName
        write_workbook.save(savePath)
        print("  cmcm  " + "  保存成功")
    except:
        errorTnfo = traceback.format_exc()
        print(errorTnfo)
        comm_logging.myLogger.write_logger(errorTnfo)



if __name__ == '__main__':
    write_cmcm()