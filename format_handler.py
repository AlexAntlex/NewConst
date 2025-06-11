from csv import excel

import aspose.cad as cad
from aspose.cad.imageoptions import PdfOptions
import win32com
import os
import random
import string

def SLT_to_PDF(filename, way_to_file):
    image = cad.Image.load(f'{filename}.stl')

    cadRasterizationOptions = cad.imageoptions.CadRasterizationOptions()
    cadRasterizationOptions.page_height = 800.5
    cadRasterizationOptions.page_width = 800.5
    cadRasterizationOptions.zoom = 1.5
    cadRasterizationOptions.layers = "Layer"
    cadRasterizationOptions.background_color = cad.Color.green

    options = PdfOptions()
    options.vector_rasterization_options = cadRasterizationOptions
    full_naming = f'{way_to_file}{filename}.pdf'
    image.save(full_naming, options)
    return full_naming

def DWG_to_PDF(filename, way_to_file):
    # Load an existing DWG file
    image = cad.Image.load(f'{filename}.dwg')
    # Specify PDF Options
    pdfOptions = cad.imageoptions.PdfOptions()
    # Save as PDF
    full_naming = f'{way_to_file}{filename}.pdf'
    image.save(full_naming, pdfOptions)
    return full_naming


# Требует наличие программы COMPAS-3D на сервере с приложением
def CDW_to_PDF(filename, way_to_file):

    try:
        # подключаемся к API КОМПАС-3D
        kompas = win32com.client.Dispatch("Kompas.Application.5")
        kompas.Visible = True # Можно скрыть (False), если не нужен интерфейс
        # Получаем API документа
        doc = kompas.Documents.Open(filename)
        if not doc:
            print("Ошибка: не удалось открыть файл.")
            return False
        # Настройка экспорта в PDF
        export_params = kompas.GetParamStruct(101) # 101 - тип параметров экспорта в PDF
        if export_params:
            export_params.Init()
            export_params.lResolution = 600    # DPI разрешение
            export_params.bShowWatermark = False    # Отключаем водяные знаки
        # Выполняем экспорт
        result = doc.SaveAs(way_to_file, 101, export_params)  # 101 - формат PDF
        doc.Close()
        if result:
            print(f"Файл успешно сохранен: {way_to_file}")
        else:
            print("Ошибка при сохранении PDF.")
            return False

    except Exception as e:
        print(f"Ошибка: {e}")
        return False

def rename_file_on_server(ext, path):
    let = string.ascii_letters + string.digits
    name = ''.join(random.choice(let) for i in range(42)) + f'.{ext}'
    while os.path.exists(path + name):
        name = ''.join(random.choice(let) for i in range(42)) + f'.{ext}'
    return name


