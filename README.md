Si ocurren problemas con SSL usando HuggingFace, en la descarga de que se hace desde el repositorio, se debe realizar lo siguiente:

1. Ir dentro del entorno de la aplicación al archivo que se encuentra en esta ruta: Lib\site-packages\requests\sessions.py

2. Buscar esta línea `verify = merge_setting(verify, self.verify)` y setear el valor a `False`. Esto hará que se ignoren la verificación de certificados, por lo cual una vez se descarguen los recursos se recomienda devolver al valor original.