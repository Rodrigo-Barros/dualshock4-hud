# dualshock4-hud
Simple battery status indicator for linux

## Descrição
Esse script monitora o nível de bateria do seu Dualshock 4 connectado via bluetooth quando você executa a combinação de Botões <kbd>L1</kbd>+<kbd>R1</kbd> no seu controle além de oferecer uma opção de desligar o controle conectado por bluetooth usando a seguinte combinação de botões: <kbd>PS Button</kbd> + <kbd>Triângulo</kbd>

## Como funciona?
Bem o script tem dois modos se é que posso dizer assim, sendo eles automático e manual.
+ modo manual: após a instalação você tem que ir até a pasta onde você baixou o repositório e executar o seguinte comando:`python3 ds4battery-hud.py`, após isso o script deverá estar exibindo notificações quando as os botoẽs configurados estiverem pressionados.
+ modo automático: o 'modo automático' permite que o script só seja executado quando o seu controle tiver conectado por bluetooth isso permite que você ecomize recursos para não executar programas desnecessriamente, nesse modo é criado uma regra dentro de /etc/udev/rules.d/ mas como lado negativo necessita de permissões de administrador/root para desfrutar dessa funcionalidade.

## Dependências

- python3
- python3-pip / pip3
- pycairo
- pip
- evdev
- pygobject


## Instalação
Antes de tudo conecte seu controle via bluetooth para começar.
Após isso execute o comando `$ bluetoothctl` para listar seus dispositvos bluetooth, localize o seu controle copie o mac address Após isso abra o arquivo `01-baterry_hud.rules` e modifique o valor 1c:66:6d:55:e3:ea pelo valor do mac address de seu controle.
Após isso execute o script `$ ./install` na pasta na qual você copiou o repositório/projeto.

# Configuração
## Estilização
Tentei dar um pouco de customização ao esse script, existe um arquivo settings.py que o usuário pode modificar conforme as suas necessidades.

## Teclas
Dentro do arquivo de settings.py há uma seção chamada keys, você pode substituir o valor dela por outros de sua preferência, para isso, basta executar `$ python3 keys.py` para descobrir os valores dos botões correspondentes a sua preferência.
