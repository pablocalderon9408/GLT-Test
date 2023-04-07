# GLT-Test

Proyecto FastAPI - CRUD de Usuarios, Productos y Órdenes

Este proyecto implementa un API CRUD (Create, Read, Update, Delete) utilizando el framework FastAPI de Python. El API tiene tres modelos principales: User, Product y Order.
Requerimientos

Antes de ejecutar este proyecto, asegúrate de tener instalado lo siguiente:

    Python 3.7 o superior
    pip (el instalador de paquetes de Python)

Para ejecutar el proyecto, sigue los siguientes pasos:

    Clona el repositorio en tu computadora: git clone https://github.com/tu_usuario/proyecto-fastapi.git
    Entra al directorio del proyecto: cd proyecto-fastapi
    Crea un ambiente virtual con python -m venv venv
    Activa el ambiente virtual con source venv/bin/activate (en Linux/Mac) o venv\Scripts\activate (en Windows)
    Instala las dependencias con pip install -r requirements.txt
    Ejecuta la aplicación con uvicorn main:app --reload

Esto iniciará el servidor en http://localhost:8000/.


Autenticación:

- Debes irte al endpoint de signup donde vas a poder ver los datos obligatorios.
- Cuando haces el signup, se te envía al correo un token de autenticación. Es posible que
no te llegue al correo, pero en la terminal lo debes poder ver.
- Lo debes usar en el endpoint de validación, para que puedas quedar con la cuenta verificada.
- Una vez estés verificado, debes hacer el login, el cual te retorna un token que debes usar para
los endpoints bloqueados.