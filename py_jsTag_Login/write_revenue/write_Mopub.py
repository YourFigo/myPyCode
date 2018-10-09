import xlrd
from xlutils import copy
import traceback
from public import comm_logging
from public import common

outPath = "D:/360security/data/"

def write_Mopub():
    read_excelName = "DailyReport_Mopub.xls"
    try:
        nowDate = common.getNowTime()[0:10]
        read_openPath = (outPath + nowDate + "/" + read_excelName).strip()
        read_workbook = xlrd.open_workbook(read_openPath)

        read_sheetName_native = read_workbook.sheet_names()[1]
        read_sheet_native = read_workbook.sheet_by_name(read_sheetName_native)
        read_numRow_native, read_numCol_native = read_sheet_native.nrows, read_sheet_native.ncols

        read_sheetName_Banner = read_workbook.sheet_names()[0]
        read_sheet_Banner = read_workbook.sheet_by_name(read_sheetName_Banner)
        read_numRow_Banner, read_numCol_Banner = read_sheet_Banner.nrows, read_sheet_Banner.ncols

        write_excelName = nowDate + "_data_total.xls"
        write_openPath = outPath + write_excelName
        write_workbook = copy.copy(xlrd.open_workbook(write_openPath))
        write_sheet_native = write_workbook.add_sheet('Mopub_native')
        write_sheet_Banner = write_workbook.add_sheet('MKT')

        for i in range(0, read_numRow_native):
            for j in range(0, 8):
                write_sheet_native.write(i + 1, j + 2, read_sheet_native.row_values(i)[j])
        print("  Mopub_native  " + "  保存成功")

        for i in range(0, read_numRow_Banner):
            for j in range(0, 8):
                write_sheet_Banner.write(i + 1, j + 2, read_sheet_Banner.row_values(i)[j])
        print("  Mopub_Banner  " + "  保存成功")

        save_excelName = nowDate + "_data_total.xls"
        savePath = outPath + save_excelName
        write_workbook.save(savePath)
        print("Mopub  " + "  保存成功")
    except:
        errorTnfo = traceback.format_exc()
        print(errorTnfo)
        comm_logging.myLogger.write_logger(errorTnfo)


if __name__ == '__main__':
    write_Mopub()