# dualshock4-hud
Simple ds4 battery indicator for linux.
![image](https://lh3.googleusercontent.com/2QFmNSqS--EFF3b9KHQuKxmlW5FxBSqmKcGVfL_bSiFlFeP7tWMYcYguE4EkVT6nTrsAKSf-ZpDWMWjZBKHKmmyEqFyCPYk1CuuZ5kRAy3Aaag1lVThRLp_ATU-BMzgNKfqP0eClhLCPQnv2QNU6LS18mNMwFXAmRH9w_jesizDnO9X39vwrC5xN7wH7qYAn1Z3C_3RNtB2NcSJlBJJNgiKoRJ7n7uLXohEsmtuXAqfa4eWOLfTin2alsUitEtnBGLJK-eHR05mSwrAQb7J3okSaD1cSAXqvGwqfNl8vid8Wvqin2HPpkK-ol9ighlsBt5Yb1AYaQi_8qzbhJ5ji1V64zGAFRLn21MvylSHpuMLhs8uYy8Nq_pXsEQiRMHlX1qHJQdcbyw3_gq0mI5Ytva1yuOKrtNaLLO1XC4V3UbbMANMWa_2J_s9I2hm75ieXzXtq39mQhWp4QpGU8taBENmDtmmBmTSl7wxLoklRDOUw_lAM9apbtNWbsxOvrBgER9FYZm4UoQxXPr4c1w3pm7JkLNjSSdYQ_jo6sQDs1ANQBTvi_SksbVl78vtF8AFkibd2zpUVM1-1-Bd-GfUEn2UWXF-VNmrF4ZHWhQH0dyIZDFTiMgVnIIAwOOze6pU_v--lfK55xsjyxQaM7LVLefOMeMtEHP9r_Y_91lexEjivevqeBrfK74QzDOw=w1366-h629-ft)
## Descrição
Esse script monitora o nível de bateria do seu Dualshock 4 connectado via bluetooth quando você executa a combinação de Botões <kbd>L1</kbd>+<kbd>R1</kbd> no seu controle além de oferecer uma opção de desligar o controle conectado por bluetooth usando a seguinte combinação de botões: <kbd>PS Button</kbd> + <kbd>Triângulo</kbd>.

## Como funciona?
Bem o script tem dois modos se é que posso dizer assim, sendo eles automático e manual.
+ modo manual: após a instalação você tem que ir até a pasta onde você baixou o repositório e executar o seguinte comando:`python3 ds4battery-hud.py`, após isso o script deverá estar exibindo notificações quando as os botoẽs configurados estiverem pressionados.
+ modo automático: o 'modo automático' permite que o script só seja executado quando o seu controle tiver conectado por bluetooth isso permite que você ecomize recursos para não executar programas desnecessriamente, nesse modo é criado uma regra dentro de /etc/udev/rules.d/ mas como lado negativo necessita de permissões de administrador/root para desfrutar dessa funcionalidade.
Vale mencionar aqui que o modo automático é usado com o udev.

## Dependências

- python3
- python3-pip / pip3
- pycairo
- evdev
- pygobject
- udev (A maioria das distribuições já oferece esse pacote por padrão)


## Instalação
`git clone https://github.com/Rodrigo-Barros/dualshock4-hud`
Antes de tudo conecte seu controle via bluetooth para começar.
Após isso execute o comando `$ bluetoothctl` para listar seus dispositvos bluetooth, localize o seu controle copie o mac address Após isso abra o arquivo `01-baterry_hud.rules` e modifique o valor 1c:66:6d:55:e3:ea pelo valor do mac address de seu controle.
Após isso execute o script `$ ./install` na pasta na qual você copiou o repositório/projeto.
No meio do script de instalação você terá a opção de instalar o modo automático para isso será perguntado se você deseja instalar e partir de então o script será executado como root.
### Somente para o método automático
Ao final do script o seu controle será desconectado, mais uma vez ele deverá ser conectado e a partir de agora deverá estar funcionando conforme com as combinações de botões padrão.

# Configuração
## Estilização
Tentei dar um pouco de customização ao esse script, existe um arquivo settings.py que o usuário pode modificar conforme as suas necessidades.

## Teclas
Dentro do arquivo de settings.py há uma seção chamada keys, você pode substituir o valor dela por outros de sua preferência, para isso, basta executar `$ python3 keys.py` para descobrir os valores dos botões correspondentes a sua preferência.

## Debug
Se por qualquer motivo você tiver algum problema com o script dentro da pasta do projeto haverá um arquivo log que pode te auxiliar.
