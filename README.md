## Crear Variables de Projecto en Gitlab CI/CD

---

Con el objetivo de hacer mas sencilla la carga de variables en un repositorio, hemos creado un script para poder realizar una carga masiva en menor tiempo sobre la API de Gitlab.

<aside>
⚠️ Es necesario tener instalado Python 3.6 o mayor y tener la libreria requests (En caso de no tenerla, se instala con **pip install requests**)

</aside>

Para ello, debemos entrar a la cuenta nuestra de Gitlab, luego ir a nuestro perfil y posteriormente acceder a **[Personal Access Token](https://gitlab.com/-/profile/personal_access_tokens).**

Una vez dentro, debemos rellenar el campo **Token name** con el nombre que deseemos ponerle y seleccionar el checkbox **API** para poder tener acceso de lectura/escritura dentro de los repositorios donde tengamos acceso de edición.

Una vez creado, debemos agregar ese Token al siguiente script:

- En ID pondremos el ID del proyecto en el cual queremos agregar las variables
- En TOKEN agregamos el TOKEN que obtuvimos con anterioridad.
- En los diferentes **VALUE, debemos agregar los valores que mencionamos con anterioridad.**
- En **environment_scope**, debemos agregar a cual environment pertenece (**prod, qa**)
