commit = guardar versión
push = subir versión a GitHub
pull = bajar cambios de otros
branch/rama = trabajar separado sin romper main
master = versión estable del proyecto

Explicación simple de las ramas en Git

Una rama es como una copia separada del proyecto donde podemos trabajar sin afectar directamente la versión principal.

La rama principal normalmente se llama master en el proyecto lo pueden ver igual en github
pero no hay tiempo kreo yo pero si kieren por seguridad haganlo asi o como kieran...



también podemos trabajar sin crear ramas, usando solamente la rama principal master.
En este caso, cada avance se guarda como una nueva versión usando commit.
Un commit es como una foto del proyecto en un momento específico.

Ejemplo:

```text
commit 1: primer commit del proyecto
commit 2: agrego index.html
commit 3: modifico views.py
commit 4: agrego estilos CSS
commit 5: corrijo error en urls.py

Los commits anteriores no se borran.
Git guarda el historial completo del proyecto.

tips: 
-Siempre hacer git pull antes de trabajar. Para tener la última versión del proyecto.
-Hacer git push al terminar. Para que los demás puedan bajar el avance

-git log --oneline para ver commits tenemos
-git checkout e4f5g6h < -- para ver el commit anterior eso ke dice e4f5g6h es el codigo del commit va ser diferente obvio pero es un ejemplo

-git checkout main para volver a la rama actual

-git pull origin main para ver los nuevos cambios ke alguein hizo y tener la version nueva en tu visual

ahi buscan los comandos ke necesiten por internet igual