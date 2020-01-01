# ecoding:utf-8
# o simbolo # representa um comentário e nao e interpretado pelo programa
# Todos os valores de tempo sao dados em segundos
config = {
    'background-color':[27, 40, 56, .95], #rgba
    'window':{
        'position':{
        'x':15,
        'y': 15
        },
        'size':{
            'width':100,
            'height':200
        }
    },
    'font':{
        'color': '#fff',
        'size': '20'
    },
    'notification':{
        'keys':[310,311],
        'timeout':5
    },
    'scan-timeout': .2 # tempo minimo para apertar os botões antes da notificação aparecer
 }
