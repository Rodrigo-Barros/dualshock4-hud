#!/bin/sh
length=$# # número de argumentos passados aos sctipt

if [ $length = 0 ];then
  echo -e "esse script compila os programs escritos em clutter de form fácil \n"
  echo -e "forma de uso ./build.sh programa.c"
  exit 0
fi

gcc $1  -export-dynamic $(pkg-config --cflags clutter-1.0 --libs clutter-1.0) -o $1.out
