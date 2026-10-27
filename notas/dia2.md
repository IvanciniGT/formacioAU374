
# Versionado de software

Usamos tradicionalmente en la industria del software lo que se llama el esquema de versionado semántico (Semantic Versioning: semVer).

vA.B.C
                 Cuándo suben?
A = MAYOR        Breaking changes! Cambio que rompe compatibilidad
                 Cuando quito algo de funcionalidad (con o sin reemplazo)
B = MINOR        Nueva funcionalidad
                 Se marca una funcionalidad como obsoleta (Deprecated)
                    (Opcionalmente puden venir arreglos de bugs)
C = PATCH        Arreglos de defectos (bugs) - Bugfixes

Oracle 11
Oracle 12
Oracle 19
       ^^
       MAYOR

       Puedo actualizar un servidor de BBDD con tranquilidad de Oracle 11 a Oracle 12? NO, ni de broma
       En cuanto instale la Oracle 12, hay cosas que ya no funcionan igual.
       Y Puede ser (caso que esas cosas se usasen por mi app) que mi aplicación deje de funcionar correctamente.
       Es necesario revisar profundamente la app, para ver si sigue funcionando o no sobre esa versión,
       y en su casohacer los cambios que sean necesarios para que siga funcionando correctamente.

Imaginad que tengo Oracle 11.7 y quiero pasar a Oracle 11.8. Puedo hacerlo con tranquilidad?
       Sin problema.. es compatible. Cómo lo se? Por el numerito.. es el mismo MAYOR!
       Quiero hacerlo? Depende. De qué depende?
       - Si necesito esa nueva funcionalidad... aunque si ya estaba trabajando con Oracle 11.7, es que mi sistema NO NECESITA NI USA esa nueva funcionalidad. Solo tendrá sentido si modifico el sistema para que ahora haga uso de esa nueva funcionaldiad.
         Sin modificar nada, esa nueva funcionalidad NO LA USARÉ. Y ojo... puede venir con nuevos BUGS! Que han tocado código!
       - Que se incluyan PARCHES (PATCH) que solucionen problemas gordos o críticos (seguridad...)
       - Acaba el soporte de esa versión! 
       - Por cojones! Hay un roadmap de actualización que tengo que seguir!

Lo que marca la funcionalidad de un sistema es la pareja MAJOR.MINOR
El PATCH me habla de la cantidad de bugs que se han ido resolviendo en esa versión MAJOR.MINOR.