from appJar import gui
from os import listdir
from os.path import isfile, join, exists, splitext
from PIL import Image
from tqdm import tqdm
import concurrent.futures
import pandas as pd

imgs = 'imgs\Pt2_codbarras'
csv_path = 'cods_barras.csv'
desired_size = (300,400)

def convert_img(path : str, pbar=None):
    if not exists(join(imgs, splitext(path)[0] + '.gif')):
        img = Image.open(join(imgs,path))
        width, height = img.size
        ratio = width/height
        if ratio > 1:
            img = img.rotate(90)
        img = img.resize(desired_size)
        img.save(join(imgs, splitext(path)[0] + '.gif'), format='GIF')
    else:
        #print(f'File {splitext(path)[0]}.gif already exists.')
        pass
    if pbar:
        pbar.update(1)

def prepare_gifs():
    path_imgs = listdir(imgs)

    pool = concurrent.futures.ThreadPoolExecutor()

    pbar = tqdm(total=len(path_imgs))
    for img in path_imgs:
        if splitext(img)[1] == '.png':
            pool.submit(convert_img, img, pbar)
        else:
            pbar.update(1)
    pool.shutdown()

def press(button):

    pass



i = 0
def AssistenteVerificacaoApp():
    path_imgs = []
    for file in listdir(imgs):
        if splitext(file)[1] == '.gif':
            path_imgs.append(file)

    df = pd.read_csv(csv_path, delimiter=',')

    df["img_path"] = df["img_path"].map(lambda x : splitext(x)[0] + '.gif')
    df["barcode_data"] = df["barcode_data"].map(lambda x : x.split("'")[1] if len(str(x).split("'")) > 1 else 0)

    with gui("Assistente de Verificação de Produtos v0.01", "800x600") as app:
        def next_img(button):
            global i
            i += 1
            print(join(imgs, path_imgs[i]))
            app.setImage('img_produto', join(imgs,df.iloc[i]['img_path']))
            app.setLabel('num_img', f'Número da imagem: {i}, Imagem: {join(imgs, df.iloc[i]["img_path"])}')
            app.setEntry('cod_barras_input', f'{df.iloc[i]["barcode_data"]}')
            #app.clearEntry('cod_barras_input', callFunction=False)
            
        
        with app.frame('ImageFrame', row=0, column=0, stretch='COLUMN'):
            app.addImage('img_produto', join(imgs,df.iloc[i]["img_path"]))
            app.setImageSize('img_produto', desired_size[0], desired_size[1])
        with app.frame('Controle',row=0,column=1, stretch='COLUMN'):
            # Identificador img
            app.addLabel('num_img', f'Número da imagem: {i}, Imagem: {join(imgs, df.iloc[i]["img_path"])}')
            # Codigo de barras
            app.addLabel('COD BARRAS', f'Cod de barras:')
            app.addNumericEntry('cod_barras_input')
            app.setEntry('cod_barras_input', f'{df.iloc[i]["barcode_data"]}')
            # Codigo do produto
            app.addLabel('cod_produto', f'Cod Produto:')
            app.addNumericEntry('cod_produto')
            app.setEntry('cod_produto', f'{df.iloc[i]["cod_produto"]}')
            # Grupo
            # Subgrupo
            # Custo
            # Preço
            app.addButton('prox_img', next_img)
        app.go()

if __name__ == '__main__':
    prepare_gifs()
    AssistenteVerificacaoApp()