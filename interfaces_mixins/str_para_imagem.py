import sys
from PIL import Image

class Str_Para_Imagem():
    def __init__(self):
      pass

    def get_imagem(self, que_numero, lista_diretorio_imagens: list, diretorio_salvar: str):

      images = [Image.open(x) for x in lista_diretorio_imagens]
      widths, heights = zip(*(i.size for i in images))

      total_width = sum(widths)
      max_height = max(heights)

      new_im = Image.new('RGB', (total_width, max_height))

      x_offset = 0
      for im in images:
        new_im.paste(im, (x_offset, 0))
        x_offset += im.size[0]

      new_im.save(diretorio_salvar)

      return new_im

    def get_imagem_dinheiro(self, que_numero: str, nome_arquivo_para_salvar: str):
      que_numero = que_numero.rjust(7,'#')
      lista_imagens = []
      for i in range(10):
        lista_imagens.append(f'../src/dinheiro/numero_{i}.png')

      img_numero = []
      img_numero.append('../src/dinheiro/moeda.png')
      if(len(que_numero)>7):
        return False

      for i,j in enumerate(que_numero):
        if(j == '#'):
          img_numero.append('../src/dinheiro/nada.png')
        else:
          img_numero.append(lista_imagens[int(j)])

      images = [Image.open(x) for x in img_numero]
      widths, heights = zip(*(i.size for i in images))

      total_width = sum(widths)
      max_height = max(heights)

      new_im = Image.new('RGB', (total_width, max_height))

      x_offset = 0
      for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]

      new_im.save(f'../src/dinheiro/{nome_arquivo_para_salvar}_off.png')
      new_im.save(f'../src/dinheiro/{nome_arquivo_para_salvar}_on.png')

      return f'../src/dinheiro/{nome_arquivo_para_salvar}'
