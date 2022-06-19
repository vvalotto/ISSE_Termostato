
python3 setup_entidades.py sdist
rm -rf entidades.egg-info
echo "Paquete de entidades construido"

python3 setup_servicios_dominio.py sdist
rm -rf servicios_dominio.egg-info
echo "Paquete de servicios del dominio construido"

python3 setup_registrador.py sdist
rm -rf registrador.egg-info
echo "Paquete de registrador construido"

python3 setup_gestores_entidades.py sdist
rm -rf gestores_entidades.egg-info
echo "Paquete de gestores construido"

python3 setup_servicios_aplicacion.py sdist
rm -rf servicios_aplicacion.egg-info
echo "Paquete de servicios de aplicacion construido"

python3 setup_configurador.py sdist
rm -rf configurador.egg-info
echo "Paquete de configurador construido"

python3 setup_agentes_sensores.py sdist
rm -rf agentes_sensores.egg-info
echo "Paquete de agentes sensores construido"

python3 setup_agentes_actuadores.py sdist
rm -rf agentes_actuadores.egg-info
echo "Paquete de agentes actuadores construido"

cp ejecutar.py ./dist
cp termostato.json ./dist
tar -cvzf termostato-1.0.0.tar.gz dist
rm ./dist/*tar.gz
rm ./dist/ejecutar.py
rm ./dist/termostato.json
cp termostato-1.0.0.tar.gz ./dist

