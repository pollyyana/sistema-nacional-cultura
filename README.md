# Sistema Nacional de Cultura
O Sistema Nacional de Cultura é um modelo de gestão e promoção de políticas públicas de cultura que pressupõe a ação conjunta dos entes da federação (governos federal, estadual e municipal) para democratização do setor. (http://pt.wikipedia.org/wiki/Sistema_Nacional_de_Cultura)

Este aplicativo cadastra os entes federados e coordena o processo de adesao desses no SNC. Por meio deste cadastro, os estados e municípios podem gerar seus acordos de cooperação técnica para a entrada no SNC, e também manter atualizados os dados de monitoramentos das metas pactuadas no ACT.

#Da Tecnologia
O cadastro do SNC é feito sobre o framework Python-Django, Python3, com banco de dados Postgres. É possível rodar em qualquer banco de dados, basta ajustar as settings.
As dependencias de pacotes estão no requirements.txt


##Requisitos

* Python3
* PIP
* python3-virtualenv
* Postgresql
* libmagic-dev
* python-magic
* wkhtmltopdf
* postgresql-server-dev-9.4

##Passos da Instalação para Debian/Ubuntu

1. Instale o PIP que é o instalador de pacotes do python3

    Baixe o arquivo get-pip.py que é um arquivo instalador executado pelo Python. O arquivo se encontra no link https://bootstrap.pypa.io/get-pip.py. 
O arquivo pode ser baixado de forma direta e rápida utilizando o comando wget -c. A opção -c tem a função de continuar o download em caso de perda de conexão.

    ```
    wget -c https://bootstrap.pypa.io/get-pip.py

    sudo python3 get-pip.py
    ```

2. Instale o construtor de ambiente virtual
    ```
    sudo apt-get install python3-virtualenv python3-venv
    ```

3. Instale a biblioteca de manipulação de imagem libmagic e o python magic
    ```
    sudo apt-get install libmagic-dev python-magic
    ```

4. Instale o wkhtmltopdf que é o aplicativo para renderizar html em pdf 
    ```
    sudo apt-get install wkhtmltopdf
    ```

5. Instale o PostgreSQL e as bibliotecas de desenvolvimento
    ```
    sudo apt-get install postgresql-9.4 postgresql-server-dev-9.4
 
    ```    
6. Crie o ambiente virtual
    ```
    pyvenv /caminho/para/o/ambiente/virtual
 
    ```    
7. Clone o repositório do projeto do github
    ```
    git clone https://github.com/culturagovbr/sistema-nacional-cultura.git snc & cd snc

    ```
    
8. Ative o ambiente virtual
    ```
    source /caminho/para/o/ambiente/virtual/bin/activate

    ```

9. Instale as dependências python do projeto
    ```
    sudo pip3 install -r requirements.txt

    ```
10. Configure o arquivo settings.py

11. Configure o banco de dados

12. Execute a aplicação (É preciso ter o ambiente virtual ativado)
    ```
    python3 manage.py runserver

    ```
