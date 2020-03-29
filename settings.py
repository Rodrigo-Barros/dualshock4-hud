# encoding:utf-8
# o simbolo # representa um comentário e nao e interpretado pelo programa
# Todos os valores de tempo sao dados em segundos
config = {
    'bat_sts':{
        'background-color':[27, 40, 56, .90], #rgba
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
        }
    },
    'player':{
        'background-color':[27,40,56, 1],
        'window':{
                'position':{
                    'x':15,
                    'y':15
                }
        },
        'font':{
            'color':'#fff',
            'size': 11
        }
    },
    'notification':{
        'keys':[310,311],
        'timeout':5
    },
    'scan-timeout': .1 #tempo para fazer a leitura dos atalhos do controle 
}
