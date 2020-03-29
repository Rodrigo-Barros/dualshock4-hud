#!/bin/bash
function get_error_code(){
	echo $?
}

function install_rule(){
	echo "Aviso essa parte do script precisa de privilegios de super usuario para prosseguir, se não 
	quiser prosseguir Aperte Ctrl+C, se quiser prosseguir aperte Enter"
	read 

	sed -i "s|@user|$USER|g" 01-baterry_hud.rules
	sed -i "s|@script_path|$PWD|g" 01-baterry_hud.rules
	sed -i "s|@script_path|$PWD|g" start

	python3 -m pip install -r requirements.txt --user
	sudo cp "01-baterry_hud.rules" "/etc/udev/rules.d/01-baterry_hud.rules"
	sudo udevadm control --reload-rules
	echo "Desabilitando o Bluetooth ..."
	echo power off | bluetoothctl
	echo "Ligando o Bluetooth novamente ..."
	echo power on | bluetoothctl
	echo "Instalação concluída com sucesso"
	echo "Para começar a utilizar é necessário apenas conectar o seu controle via Bluetooth"
}


echo Conecte o seu controle antes de começar
echo Aperte Enter para continuar quando estiver pronto
read 

ls /sys/class/power_supply/sony_controller* &> /dev/null

if [ $(get_error_code) == 0 ];then
	echo -e "Dispositivos dectados:"
	for i in /sys/class/power_supply/sony_controller* ;do
		echo $i
		controller_path=$i
	done 
	#arquivo de leitura do nivel de bateria do controle
	echo atulizando o arquivo de configuração:
	#sed -E "s|\/sys.+(')|$controller_path/capacity'|g" -i ds4battery-hud.py
	
	echo -e "
	Esse script oferece a opção de hot reload, mas você pode estar se perguntando o que é isso?
	para resumir o hotreload descrito aqui vai atuar assim, quando seu controle for conectado o programa irá
	rodar em segundo plano para maior comodidade.
	No entanto para desfrutar dessa comodidade o script deve ser instalado como super usuário, ou você pode mover o arquivo que 
	termina em .rules para /etc/udev/rules.d e executar o seguinte comando: 'sudo udevadm control --reload-rules' para recarregar
	as regras do udev
	"
	echo "instalar a regra do udev? [S/n]"
	read user_action
	case $user_action in
		"")
			echo Nenhum comando informado saindo do script
			exit 0;;
		's' | 'S' )
			install_rule;;

		'n' | 'N')
			echo Script finalizado pelo usuario;;
		*)
			echo Opção invalida 
			exit 1;;
	esac
fi

if [ -z $controller_path ];then 
	echo "Controle Não detectado saindo do script"
	exit 1 
fi
