import os
import glob

from openpyxl import load_workbook
from win32com.client import Dispatch


class excelUtil():

    def __init__(self):
        pass

    def remove_all_xlsx_files_name_ranges(self, folder_path):
        xlsx_glob_path = os.path.join(folder_path, "*.xlsx")
        xlsx_path_list = glob.glob(xlsx_glob_path)
        for xlsx_file_path in xlsx_path_list:
            self.remove_all_name_ranges(xlsx_file_path)


    def remove_all_name_ranges(self, xlsx_file_path):
        wb = load_workbook(xlsx_file_path)
        length = len(wb.defined_names)


        while length > 0:
            for defined_name_range in wb.defined_names.definedName:
                del wb.defined_names[defined_name_range.name]
            length = len(wb.defined_names)

        wb.save(xlsx_file_path)
        wb.close()


        excel = Dispatch('Excel.Application')
        wb = excel.Workbooks.Open(xlsx_file_path)
        
        # fileformat 51은 xlsx에 대한 magic number입니다. 
        wb.Save()
        wb.close
        excel.Quit()


    def xls_files_convert(self, folder_path):
        xls_file_list = []
        for root, dirs, files in os.walk(folder_path):
            xls_glob_path = os.path.join(root, "*.xls")
            xls_file_list = xls_file_list + glob.glob(xls_glob_path)

        for xls_file_path in xls_file_list:
            xlsx_file_path = self.xls_to_xlsx(xls_file_path)
            print(f"xls_file : {xls_file_path}\nxlsx_file_path : {xlsx_file_path}")

    def xls_to_xlsx(self, xls_file_path):
        
        # replace 함수를 통해서 *.xls 에서 *.xlsx로 새로운 문자열을 만들어줍니다.
        xlsx_file_path = xls_file_path.replace(".xls", ".xlsx").replace("/", "\\")
        excel = Dispatch('Excel.Application')
        wb = excel.Workbooks.Open(xls_file_path)
        
        # fileformat 51은 xlsx에 대한 magic number입니다. 
        wb.SaveAs(xlsx_file_path, FileFormat=51)
        wb.close
        excel.Quit()
        
    #     os.remove(xls_file_path)
        return xlsx_file_path
