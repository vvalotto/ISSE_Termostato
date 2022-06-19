
tar xvzf entidades-1.0.0.tar.gz
cd entidades-1.0.0
python3 setup_entidades.py install
cd ..
rm -rf entidades-1.0.0
echo "entidades instalado"

tar xvzf servicios_dominio-1.0.0.tar.gz
cd servicios_dominio-1.0.0
python3 setup_servicios_dominio.py install
cd ..
rm -rf servicios_dominio-1.0.0
echo "servicios_dominio instalado"

tar xvzf registrador-1.0.0.tar.gz
cd registrador-1.0.0
python3 setup_registrador.py install
cd ..
rm -rf registrador-1.0.0
echo "registrador instalado"

tar xvzf gestores_entidades-1.0.0.tar.gz
cd gestores_entidades-1.0.0
python3 setup_gestores_entidades.py install
cd ..
rm -rf gestores_entidades-1.0.0
echo "gestores_entidades instalado"

tar xvzf servicios_aplicacion-1.0.0.tar.gz
cd servicios_aplicacion-1.0.0
python3 setup_servicios_aplicacion.py install
cd ..
rm -rf servicios_aplicacion-1.0.0
echo "servicios_aplicacion instalado"

tar xvzf configurador-1.0.0.tar.gz
cd configurador-1.0.0
python3 setup_configurador.py install
cd ..
rm -rf configurador-1.0.0
echo "servicios_aplicacion instalado"

tar xvzf agentes_actuadores-1.0.0.tar.gz
cd agentes_actuadores-1.0.0
python3 setup_agentes_actuadores.py install
cd ..
rm -rf agentes_actuadores-1.0.0
echo "agentes_actuadores instalado"

tar xvzf agentes_sensores-1.0.0.tar.gz
cd agentes_sensores-1.0.0
python3 setup_agentes_sensores.py install
cd ..
rm -rf agentes_sensores-1.0.0
echo "agentes_sensores instalado"

cd ..
mkdir termostato
cp dist/ejecutar.py termostato
cp dist/termostato.json termostato
rm -rf dist
cd termostato
python3 ejecutar.py



