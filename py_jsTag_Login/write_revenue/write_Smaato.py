import xlrd
from xlutils import copy
import traceback
from public import comm_logging
from public import common

outPath = "D:/360security/data/"

def write_Smaato():
    read_excelName = "DailyReport_Smaato.xls"
    try:
        nowDate = common.getNowTime()[0:10]
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
        write_sheet = write_workbook.add_sheet('Smaato')

        # sum_sheet = xlrd.open_workbook(write_openPath).sheet_by_name("汇总")
        # sum_num_Row = sum_sheet.nrows
        #
        # dict = {}
        # for i in range(2, sum_num_Row):
        #     dict[sum_sheet.cell(i, 2).value] = sum_sheet.cell(i, 3).value
        #
        # for i in range(2,read_numRow):
        #      str = ''
        #      try:
        #          str = dict[read_sheet.row_values(i - 1)[0]]
        #      except KeyError:
        #          str = '#N/A'
        #      finally:
        #          write_sheet.write(i, 0, str)

        # for i in range(2,read_numRow):
        #     x = xlwt.Formula('=VLOOKUP(B' + str(i + 1) + ',汇总!C:D,2,FALSE)')
        #     sheet.write(i,0,xlwt.Formula('=VLOOKUP(B' + str(i + 1) + ',汇总!C:D,2,FALSE)'))

        for i in range(0, read_numRow):
            for j in range(0, 12):
                write_sheet.write(i + 1, j + 1, read_sheet.row_values(i)[j])


        save_excelName = nowDate + "_data_total.xls"
        savePath = outPath + save_excelName
        write_workbook.save(savePath)
        print("  Smaato  " + "  保存成功")
    except:
        errorTnfo = traceback.format_exc()
        print(errorTnfo)
        comm_logging.myLogger.write_logger(errorTnfo)

# def write_formula():
#     nowDate = common.getNowTime()[0:10]
#     write_excelName = nowDate + "_data_total.xls"
#     write_openPath = outPath + write_excelName
#     write_workbook = copy.copy(xlrd.open_workbook(write_openPath))
#     write_sheet = write_workbook.get_sheet(2)
#     write_num_row = xlrd.open_workbook(write_openPath).sheet_by_name('Smaato').nrows
#
#     for i in range(2, write_num_row):
#         x = xlwt.Formula('VLOOKUP(B' + str(i + 1) + ',汇总!C:D,2,FALSE)')
#         write_sheet.write(i, 0, xlwt.Formula('VLOOKUP(B' + str(i + 1) + ',汇总!C:D,2,FALSE)'))
#
#     save_excelName = nowDate + "_data_total.xls"
#     savePath = outPath + save_excelName
#     write_workbook.save(savePath)
#     print("  Smaato  " + "  保存成功")

if __name__ == '__main__':
    write_Smaato()
