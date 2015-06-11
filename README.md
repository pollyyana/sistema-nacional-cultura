# Sistema Nacional de Cultura
O Sistema Nacional de Cultura é um modelo de gestão e promoção de políticas públicas de cultura que pressupõe a ação conjunta dos entes da federação (governos federal, estadual e municipal) para democratização do setor. (http://pt.wikipedia.org/wiki/Sistema_Nacional_de_Cultura)

Este aplicativo cadastra os entes federados e coordena o processo de adesao desses no SNC. Por meio deste cadastro, os estados e municípios podem gerar seus acordos de cooperação técnica para a entrada no SNC, e também manter atualizados os dados de monitoramentos das metas pactuadas no ACT.

#Da Tecnologia
O cadastro do SNC é feito sobre o framework Python-Django, Python3, com banco de dados Postgres. É possível rodar em qualquer banco de dados, basta ajustar as settings.
As dependencias de pacotes estão no requirements.txt



#Instalação

##Requisitos

* Python3
* PIP
* python3-virtualenv
* Postgresql
* libmagic-dev
* python-magic
* wkhtmltopdf

##Passos

+ Instale o python3
```
sudo apt-get install python3.4
```
+ Instale o PIP no python3
```
sudo python3 get-pip.py
```
+ Instale o construtor de ambiente virtual
```
python3-virtualenv
```
+ Instale o Postgre
```
sudo apt-get install postgresql-9.4
```
+ Instale a libmagic e o python magic
```
sudo apt-get install libmagic-dev
sudo apt-get install python-magic
```
+ Instale o wkhtmltopdf
```
sudo apt-get install wkhtmltopdf
```

