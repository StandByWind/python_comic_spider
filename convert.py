import img2pdf
import os


def img_remove(webp_path):

   path = os.chdir(webp_path)
   lists = os.listdir(path)
   for list in lists:
        name, ext = os.path.splitext(list)
        if ext == '.webp':
            os.remove(name + '.webp')


def creat_pdf(jpg):
    name = input('请输入漫画名字：')
    output = f'{name}.pdf'
    with open(output, 'wb') as file:
        write_content = img2pdf.convert(jpg)
        file.write(write_content)


img_remove('image')
jpg = os.listdir(os.getcwd())
creat_pdf(jpg)