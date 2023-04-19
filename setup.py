import sys
from cx_Freeze import setup, Executable
build_exe_options = {"packages":["barcode","reportlab","PyQt5","requests","num2words"]}

base = None
if sys.platform == 'win32':
    base = 'win32GUI'
executables = [
    Executable('funções.py',base=base,icon='icone.ico')
]
buildOptions = dict (
    packages = ["barcode","reportlab","PyQt5","requests","num2words"],
    includes = [],
    include_files = [
    'cadastrar.png','caixa2.png','carrinho.png','compras.png','cons_venda.png','contas.png','editar.png',
    'excluir.png','fecha.png','icone.ico','icons8-cardápio-64.png','icons8-comprimir-64.png',
    'icons8-maximize-32.png','impressora.png','login.png','login100x100.jpg','logo.jpg','novo.png','pagar.png','pesquisar.png',
    'produto.png','receber.png','recibo.png','salvar.png','usuarios.png'
    ],
)


#includeFiles = [
    #'cadastrar.png','caixa2.png','carrinho.png','compras.png','cons_venda.png','contas.png','editar.png',
    #'excluir.png','fecha.png','icone.ico','icons8-cardápio-64.png','icons8-comprimir-64.png',
    #'icons8-maximize-32.png','impressora.png','login.png','login100x100.png','logo.jpg','novo.png','pagar.png','pesquisar.png',
    #'produto.png','receber.png','recibo.png','salvar.png','usuarios.png'
#]



setup(
    name = 'Systembar',
    version = '1.0',
    description = 'Systema de Vendas',
    options = dict(build_exe =  buildOptions),
    executables=executables
)
