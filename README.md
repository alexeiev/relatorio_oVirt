# Criar relatorio personalizado de VMs no oVirt vanilla

# Definições do Projeto:
É necessario gerar relatório de todas as  maquinas virtuais hospedadas no
cluster oVirt e devem conter a seguinte informação:

 Nome; CPU; RAM; OS; DISCO(se possível o consumo); AMBIENTE;

## Requirements
Instalação do repositório do oVirt e suas dependências
 ```bash
sudo dnf install http://resources.ovirt.org/pub/yum-repo/ovirt-release44.rpm
sudo dnf install -y python3-ovirt-engine-sdk4 gcc libxml2-devel
pip3 install -r requirements.txt --user
 ```

Deve fazer o download da CA utilizada no oVirt
```bash
openssl s_client -connect SITELOCAL.ovirt:443 -showcerts
```
O segundo certificado é a CA que deves copiar para dentro do ficheiro ca.pem e salvar na raiz do projeto


### Criar ficheiro de environment
 ```bash
cat <<EOF>> .env
USERNAME='admin@internal'
PASSWORD='XXX'
SITE='meuservidor.local'
FILE='relatorio.csv'
EOF
 ```
