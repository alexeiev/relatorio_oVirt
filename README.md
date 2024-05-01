# Criar relatorio personalizado de VMs no oVirt Vanilla

# Definições do Projeto:
Devido a necessidade de gerar relatório de todas as maquinas virtuais hospedadas no
cluster oVirt Vanilla, coisa que não se consegue realizar na sua UI, criei este script
que compartilho com vocês.

Foi utilizada as seguintes informações como base para a coleta:

**[ Nome; Processador; Memória; Sistema Operacional; Disco ]**

## Docker
Para facilitar a a utilização e a portabilidade, criei uma imagem Docker com todo o ambiente
necessário para esta utilização.
Teremos os seguintes passos a seguir

### 1- Download da CA utilizada no oVirt
Para fazer o download do Certificado CA, poderemos executar o comando a seguir.
```bash
openssl s_client -connect SITELOCAL.ovirt:443 -showcerts
```
O segundo certificado é a CA que deverá ser copiado para dentro do novo arquivo ca.pem e salvar na raiz do projeto

### 2- Criando arquivo de environment

Para criar o arquivo de Envinroment, poderemos utilizar o comando na raiz do nosso projeto.

 ```bash
cat <<EOF>> .env
USERNAME='admin@internal'
PASSWORD='XXX'
SITE='meuservidor.local'
FILE='relatorio.csv'
EOF
 ```
Deveremos modificar o valor das variáveis para adequar aos nossos valores.

### 3- Execução
Com o arquivo .env e o ca.pem criados, poderemos executar o container com o comando a seguir.

```bash
docker run -it -v "$PWD/ca.pem:/app/relatorio_oVirt-1.0.0/ca.pem:ro" -v "$PWD/.env:/app/relatorio_oVirt-1.0.0/.env:rw" ceievfa/relatorio_ovirt:1.0
```
desta forma, teremos o container em execução e pronto para a execução do script. 

```bash
./ovirt-rel.py
```

Será gerado um arquivo CSV com o nome indicado na variável FILE. Caso já exista um arquivo
no diretório com o mesmo nome, será perguntado se é para substituir ou poderá indicar um nome
para o novo arquivo.

Existe uma variável no script que poderá ser modificada para filtrar as maquinas que serão listadas no relatório.

```bash
vms = vms_service.list(search='name=srv-app*', max=30)
```

Pode usar o parâmetro **max=\<int>**, para indicar um número máximo de resultados
Pede usar o parâmetro **search=\<str>** , para indicar uma pesquisa de nomes para o relatório.

Para um relatório completo, não passar parâmetro nesta variável, deixando da seguinte forma:
```bash
vms = vms_service.list()
```


**Link de Referência**

[oVirt SDK](https://www.ovirt.org/documentation/doc-Python_SDK_Guide/#Installing_the_Software_Development_Kit)