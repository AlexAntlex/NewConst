import aspose.cad as cad
from aspose.cad.imageoptions import PdfOptions
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


def rename_file_on_server(ext, path):
    let = string.ascii_letters + string.digits
    name = ''.join(random.choice(let) for i in range(42)) + f'.{ext}'
    while os.path.exists(path + name):
        name = ''.join(random.choice(let) for i in range(42)) + f'.{ext}'
    return name


