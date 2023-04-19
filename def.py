def moeda(valor):
    try:
        if valor.strip() == '':
            return
        #valor = str(login.txt_usuario.text().strip().replace('.', '').replace(',', ''))
        if len(valor) == 1:
            valor2 = '0,0' + valor[0]
        if len(valor) == 2:
            valor2 = '0,' + valor[0:2]
        if len(valor) == 3:
            valor2 = valor[0] + ',' + valor[1:3]
        if len(valor) == 4:
            valor2 = valor[0:2] + ',' + valor[2:4]
        if len(valor) == 5:
            valor2 = valor[0:3] + ',' + valor[3:5]
        if len(valor) == 6:
            valor2 = valor[0] + '.' + valor[1:4] + ',' + valor[4:6]
        if len(valor) == 7:
            valor2 = valor[0:2] + '.' + valor[2:5] + ',' + valor[5:7]
        if len(valor) == 8:
            valor2 = valor[0:3] + '.' + valor[3:6] + ',' + valor[6:8]
        if len(valor) == 9:
            valor2 = valor[0] + '.' + valor[1:4] + '.' + valor[4:7] + ',' + valor[7:9]
        if len(valor) == 10:
            valor2 = valor[0:2] + '.' + valor[2:5] + '.' + valor[5:8] + ',' + valor[8:10]
        if len(valor) == 11:
            valor2 = valor[0:3] + '.' + valor[3:6] + '.' + valor[6:9] + ',' + valor[9:11]
        if len(valor) == 12:
            valor2 = valor[0] + '.' + valor[1:4] + '.' + valor[4:7] + '.' + valor[7:10] + ',' + valor[10:12]
        return valor2
        #login.txt_usuario.setText(f'{valor2}')
    except: 'erro'
