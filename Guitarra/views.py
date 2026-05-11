# Vista para la videollamada embebida de la clase privada
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import redirect

@login_required
def claseprivada_videollamada(request, pk):
    from .models import ClasePrivada
    from django.urls import reverse
    clase = get_object_or_404(ClasePrivada, pk=pk)
    user = request.user
    if not clase.puede_acceder(user):
        return HttpResponseForbidden("No tienes permiso para acceder a esta videollamada.")
    if clase.estado == 'cancelada':
        return render(request, 'clases/videollamada_cancelada.html', {'clase': clase})

    ahora = timezone.now()
    if clase.fecha_inicio > ahora:
        return render(request, 'clases/videollamada_espera.html', {'clase': clase})
    if clase.fecha_fin <= ahora:
        return render(
            request,
            'clases/videollamada_caducada.html',
            {'clase': clase},
            status=403,
        )

    if request.GET.get('redirigir') != '0':
        return redirect(clase.get_jitsi_join_url())

    from django.conf import settings

    profile = getattr(user, 'profile', None)
    display_name = (
        getattr(profile, 'display_name', None)
        or user.get_full_name().strip()
        or user.get_username()
    )
    jitsi_domain = getattr(settings, 'JITSI_MEET_DOMAIN', 'meet.jit.si')
    jitsi_api_url = getattr(settings, 'JITSI_MEET_EXTERNAL_API_URL', f'https://{jitsi_domain}/external_api.js')
    return_url = request.GET.get('return_url') or reverse('guitarra:claseprivada_detail', kwargs={'pk': clase.pk})

    context = {
        'clase': clase,
        'jitsi_room_name': clase.get_jitsi_room_name(),
        'jitsi_display_name': display_name,
        'jitsi_domain': jitsi_domain,
        'jitsi_api_url': jitsi_api_url,
        'return_url': return_url,
    }
    return render(request, 'clases/videollamada.html', context)
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AdminRequiredLoginMixin, OwnerOrAdminRequiredMixin
from django.views.generic import ListView
from .models import Notification
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from django.views import View
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.db import models
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

# List view for user notifications
class NotificationListView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_list.html'
    context_object_name = 'notifications'
    paginate_by = 20

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')

class IABusquedaView(LoginRequiredMixin, View):
    template_name = 'IA/ia_busqueda.html'

    def get(self, request):
        return render(request, self.template_name, {'respuesta': None, 'pregunta': ''})

    def post(self, request):
        pregunta = request.POST.get('pregunta', '').strip()
        respuesta = None
        user = request.user
        nombre = user.first_name or user.username or 'usuario'
        if pregunta:
            saludos = ["hola", "buenas", "buenos días", "buenas tardes"]
            despedidas = ["adiós", "hasta luego", "nos vemos", "gracias"]
            pregunta_limpia = pregunta.lower().strip()
            # Saludo
            if any(pregunta_limpia.startswith(s) for s in saludos):
                respuesta = f"Hola {nombre}, dime qué necesitas."
            # Despedida
            elif any(pregunta_limpia.startswith(d) for d in despedidas):
                respuesta = f"¡Hasta pronto, {nombre}! Si tienes más dudas sobre flamenco, aquí estaré."
            # Guitarras específicas
            elif "guitarra" in pregunta_limpia or any(modelo in pregunta_limpia for modelo in [
                "alhambra 10fc", "alhambra 10fp", "alhambra 10 premier", "alhambra 11p", "alhambra 1c blacksatin", "alhambra 1c ht", "alhambra 2c", "alhambra 2f", "alhambra 3c", "alhambra 3f", "alhambra 4f", "alhambra 5f", "alhambra 7fc"
            ]):
                modelos_info = {
                    "alhambra 10fc": ("La Alhambra 10 Fc es una guitarra de alto nivel, muy flamenca, cómoda y con un sonido potente de calidad. Una guitarra elaborada con materiales de primera calidad y mediante un trabajo completamente artesanal. Un instrumento con un sonido potente, pero a la vez extremadamente cómoda. Tener entre las manos el modelo 10 Fc de Guitarras Alhambra, significa tocar con una guitarra que confiere al guitarrista mucha seguridad y capacidad para interpretar cualquier composición. El guitarrista que prueba el modelo 10 Fc percibe enseguida su excelente elaboración. El estudio y la investigación que Manufacturas Alhambra ha realizado durante muchos años, está reflejado en sus magníficos instrumentos y logran hacer disfrutar al intérprete más exigente. El modelo 10 Fc es un ejemplo, una guitarra flamenca blanca con altas prestaciones, totalmente equilibrada, consiguiendo un tono constante en todo el diapasón y una buena relación entre graves y agudos. Acabados de gran calidad. Para la construcción de la guitarra flamenca 10 Fc, se realiza una estricta selección de las maderas a utilizar. ciprés español macizo para los aros y el fondo y abeto alemán macizo para la tapa. Esta guitarra se elabora con ébano en el diapasón, clavijeros de lujo dorados y refuerzo de ébano en el mástil de cedro. El refuerzo de ébano se encuentra exactamente bajo del diapasón, en el interior del mástil. Para poder verlo se tiene que retirar la cejuela. Además, para contribuir a la comodidad del instrumento, se ha utilizado el mango desarrollado por Manufacturas Alhambra denominado Ergoneck. Un mástil ergonómico que favorece el agarre y el acceso al diapasón. En cuanto al acabado, en el modelo 10 Fc se utiliza un acabado brillo. En concreto para la tapa se utiliza un barniz mediante Laca nitrocelulosa. Un acabado que ofrece mayor flexibilidad y por lo tanto, mayor capacidad de vibración a la tapa. Incorpora dos silletas con diferente altura y golpeador. El modelo 10 Fc se sirve con dos silletas de hueso, pero con diferente altura. De esta manera cada guitarrista puede variar la acción de las cuerdas mediante el cambio de la silleta. La intención es conseguir una acción baja o algo más alta, aunque siempre estando totalmente adaptadas a las características de guitarra. Además esta guitarra viene provista de golpeador para proteger la tapa. En concreto se incorpora un golpeador estándar de una sola pieza. Respecto al tipo de cuerdas utilizadas, se instalan las cuerdas JG Flamenco Titanium de tensión fuerte, de la marca Royal Classics."),
                    "alhambra 10fp": ("Una flamenca oscura, completamente maciza y con tapa de cedro. Una guitarra muy bella y de gran calidad. Este modelo ha sido desarrollado en colaboración con el guitarrista flamenco Carlos Piñana, donde se han introducido unas especificaciones técnicas que definen un instrumento con las cualidades requeridas por los guitarristas flamencos de hoy en día, consiguiendo una guitarra flamenca muy bella y de gran calidad. Como elemento diferenciador de la 10 Fp Piñana, salta a la vista el diseño de la pala. Una silueta en la parte superior moldeada con forma de “cuernos”, con un acabado en brillo, que identifican fácilmente este instrumento y que le aporta mucha personalidad. El modelo 10 Fp Piñana es una guitarra de las denominadas como oscura, marcada por su característica principal, la utilización de Palosanto de India macizo para elaborar los aros y fondo. Aunque cabe destacar la elección del cedro macizo para la tapa. Una característica poco frecuente en las guitarras flamencas, pero que después de un proceso de desarrollo, mediante una configuración especial de barras armónicas, se consigue un sonido más redondo, se podría decir que más delicado, aunque siempre sin perder el carácter flamenco. Además en el caso de la 10 Fp Piñana el acabado es en mate, un acabado que requiere de menor cantidad de barniz y mediante el cual se consigue un sonido más potente. Una guitarra con un sonido muy flamenco pero con una calidez especial, un sonido adecuado para poder interpretar la música flamenca actual, pero sin perder la tradición de este arte. El modelo 10 Fp Piñana se construye con clavijeros de lujo dorados y un mástil muy cómodo con refuerzo de ébano. Un instrumento que por sus características estéticas aporta mucha elegancia y personalidad. Cualidades que se potencian cuando se unen al sonido de esta interesante guitarra."),
                    "alhambra 10 premier": ("Bajos, medios y agudos bien equilibrados y una proyección del sonido increíble, una guitarra moderna dirigida al guitarrista de hoy. Con el modelo 10 Premier, los artesanos de Guitarras Alhambra han aplicado la experiencia acumulada durante años en la elaboración de guitarras clásicas. Desde el modelo 8 P hasta el 11 P, los instrumentos están elaborados por un grupo reducido de artesanos donde, de manera progresiva, cada modelo adquiere mayor tiempo de elaboración, diseño y detalle. El modelo 10 Premier cuenta con un diseño de barras armónicas que favorece al máximo el volumen y la proyección de este. Un sonido que unido a una a altura de cuerdas perfecta, lo suficientemente alta para contribuir al sonido, pero al mismo tiempo con la altura justa para ser extremadamente cómoda, describen una guitarra con una proyección del sonido increíble y con bajos, medios y agudos bien equilibrados, una guitarra moderna diseñada para el guitarrista de hoy en día. Calidad y detalles. El modelo 10 Premier de Guitarras Alhambra está diseñado y elaborado con una serie de detalles que aumentan las prestaciones de este instrumento. Los acabados de este modelo denotan un importante trabajo artesanal y una imagen muy refinada. Doce orificios en el puente, hueso en la silleta y cejuela y un clavijero muy eficiente que proporcionan al modelo 10 Premier cualidades estéticas, pero a la vez comodidad y buen sonido. Un diseño donde se ha implementado el mango denominado “ergoneck”, que favorece la comodidad del guitarrista, y donde el diapasón se prolonga por la boca de la tapa armónica para introducir el traste número 20. Un diseño solicitado por los guitarristas y por las composiciones de hoy en día. Es difícil imaginar todas las posibilidades que ofrece este instrumento, donde especialmente cabe destacar la calidad sonora de la primera cuerda. En definitiva, una guitarra moderna para responder sobradamente a las exigencias del guitarrista de hoy en día."),
                    "alhambra 11p": ("Un sonido potente, pero a la vez delicado, que proporciona a esta guitarra de concierto unos atributos de alto nivel para la interpretación. El modelo 11 P es el de gama más alta antes de pasar a la serie denominada “signature models”, las guitarras más selectas de luthier. Los acabados de este modelo denotan un importante trabajo artesanal y una imagen muy refinada. Cabe destacar la línea verde adicional en los perfiles, así como la tipología de construcción. Al respecto, la pieza llamada tacón, del sistema constructivo tradicional denominado “tacón español”, en el modelo 11 P está compuesto por 5 piezas, mientras que en el resto de modelos sólo está compuesto por una única pieza. También se puede observar que el diapasón del modelo 11 P es más largo. El diapasón se prolonga por la boca de la tapa armónica para introducir un traste adicional. Un elemento que es solicitado por guitarristas calificados y que es necesario para tocar algunas piezas musicales. Además, este instrumento está construido con hueso en la silleta y cejuela, un material que se ha utilizado tradicionalmente y cuyas capacidades de vibración son excepcionales. Características que junto a una cuidada selección de maderas y una elaboración artesanal, producen un sonido fuerte, con cuerpo y de nivel de concierto. El sonido del modelo 11 P es un sonido potente, pero que a la vez puede producir las notas más delicadas y melodiosas con un sonido dulce y refinado. En definitiva, una guitarra que responde sobradamente a las exigencias del guitarrista y que cuando se tiene entre las manos se nota robusta, transmite energía y se disfruta haciéndola sonar. Unas características que proporciona a esta guitarra de concierto unos atributos de alto nivel para la interpretación."),
                    "alhambra 1c blacksatin": ("Un instrumento de estudio con un acabado que sorprende. Una guitarra de color oscuro mate, elegante y con estética moderna. Esta guitarra sorprende por su característico color oscuro mate, un diseño muy cuidado y elaborado con materiales de calidad. Cabe destacar que el acabado oscuro mate, al contrario de lo que se puede pensar, no deja marca de las huellas de las manos. Hecha a mano y con maderas seleccionadas, el modelo 1 C Black Satin está construido con tapa maciza de cedro y con aros y fondo de Sapelli, maderas que posibilitan un sonido con volumen y adecuado para interpretar diferentes estilos. El acabado está cuidado para ofrecer un instrumento elegante. Elementos como los clavijeros niquelados, el Palosanto del diapasón, el ribete en la tapa y su característico color oscuro mate, definen una guitarra bella y estilizada. Color oscuro mate, una imagen moderna. El modelo 1 C Black Satin es un instrumento muy cómodo, al igual que el modelo 1 C, la acción de las cuerdas está diseñada para conseguir un instrumento muy adecuado para el inicio en el estudio del arte de la guitarra. Las prestaciones sonoras y la comodidad, configuran un instrumento adecuado para la interpretación de diferentes estilos musicales. Es por ello que se ha optado por ofrecer la posibilidad de una guitarra oscura, de manera que este instrumento se aleja un poco de la tradicional imagen de una guitarra clásica. Sonido potente. Aunque el modelo 1 C Black Satin sea un instrumento de inicio, con una buena relación calidad-precio, nos encontramos con una guitarra con volumen y con alta capacidad para definir el sonido. Para la elaboración de los puentes, tanto para la silleta como para cejuela, se ha utilizado melamina, un material sintético altamente transmisor del sonido y que contribuye a conseguir un sonido redondo y definido. En definitiva, el modelo 1 C Black Satin es una guitarra elegante, con muy buenas prestaciones, que junto a su estética, la convierten en un instrumento muy versátil en su uso."),
                    "alhambra 1c ht": ("Este modelo 1 C HT (Hybrid Terra) es ideal para iniciarse en el estudio de la guitarra, con un peso un 10 % más ligero y un acabado que combina brillo y open pore. Este modelo sorprende principalmente por su acabado, una combinación de brillo y open pore que nunca se había visto en ningún otro modelo de guitarras Alhambra. Como todos los modelos, está hecha a mano y con maderas seleccionadas. Para la tapa se ha utilizado cedro macizo y Sapelli para aros y fondo. El acabado está cuidado para ofrecer un instrumento elegante y diferente. Además, viene con clavijeros niquelados, diapasón de palosanto y un virete de arce que definen una guitarra bella y estilizada. Se ha desarrollado un nuevo sistema de barnizado que respeta el medio ambiente, consiguiendo una mejora en la huella de carbono del 66 % y una reducción de emisiones de CO2 del 90%. Comodidad. La altura de las cuerdas y la elección de los trastes de alpaca ayudan a que el modelo 1 C HT (Hybrid Terra) sea muy cómodo, y sea un modelo perfecto para el inicio en el estudio del arte de la guitarra. Una comodidad que, unida a las prestaciones sonoras y estéticas, recompensan el esfuerzo del estudiante de este arte. Sonido Alhambra. Aunque el modelo 1 C HT (Hybrid Terra) sea un instrumento diseñado principalmente para estudiantes, nos encontramos con una guitarra con volumen y con alta capacidad para definir el sonido. Tanto para la silleta como para cejuela, son de melamina, un material sintético altamente transmisor del sonido y que contribuye a conseguir un sonido redondo y definido. En definitiva, el modelo 1 C HT (Hybryd Terra)es una guitarra de estudio con muy buenas prestaciones que ganará en sonido cuanto más la toques."),
                    "alhambra 2c": ("Un instrumento de estudio con potencia, calidad sonora y amplia gama de tonos, siempre con tapa maciza está disponible en Cedro o Abeto. Cuando tocas por primera vez el modelo 2 C de Guitarras Alhambra, disfrutas de una guitarra con gran volumen y claridad. Un instrumento que aporta un  amplia gama de tonos para crear diferentes clases de timbre y color en el sonido. Este instrumento, siendo adecuado para el inicio en el estudio, ofrece muchas posibilidades de interpretación, pudiendo ser utilizado para diferentes estilos. Estética y un acabado cuidado. Una preciosa guitarra, estilizada y con un cuidado acabado. Al igual que el modelo 1C, este instrumento de estudio, está construido con Sapelli para aros y fondo, Palosanto en el diapasón y clavijeros niquelados. En este caso, el acabado del modelo 2 C cuenta con un doble perfil, añadiendo uno en el fondo, y con la posibilidad de elección entre Cedro o Abeto para la tapa. Una tapa siempre maciza y que contribuye de manera directa a conseguir el gran sonido de esta guitarra. La elección entre Cedro o Abeto para la tapa es importante y depende del gusto del interprete. Existen diferencias en el color del sonido de la guitarra según el tipo de madera utilizada. Además, la estética también cambia de manera radical, siendo el color del Abeto mucho más claro que el del Cedro. También el modelo 2 C se elabora con melamina en la silleta y la cejuela. Un material sintético que es muy buen transmisor del sonido y que proporciona a este instrumento un color de sonido redondo, manteniendo la potencia y la diversidad de matices. El modelo 2 C, al igual que el modelo 1 C, es un instrumento de estudio aunque un paso más en prestaciones. Una guitarra muy cómoda y de gran calidad. Una elección segura para todo aquel que empieza en el mundo del arte de las seis cuerdas."),
                    "alhambra 2f": ("Una flamenca que hace volver a las raíces, a la tradición del arte flamenco. El modelo 2 F es una preciosidad y una maravilla de guitarra. Acabada con barniz de poro abierto y una tapa maciza de cedro, donde llama la atención la sonoridad. Muy potente y con un sonido fuertemente flamenco. En el modelo 2 F se ha cuidado especialmente el diseño, donde se ha buscado la sencillez junto a una excelente calidad. La 2 F es una opción segura para principiantes, con una relación calidad-precio excelente. En esta guitarra se ha utilizado la melamina para la silleta y la cejuela, un material que transmite mucho el sonido y que ofrece un sonido redondo, muy equilibrado. Además se ha utilizado el mástil ergoneck, un mango más estrecho, en este caso construido con Samanguila, y que la convierte en un instrumento muy cómodo."),
                    "alhambra 3c": ("Siendo una guitarra de estudio, con el modelo 3 C se observa un paso más en cuanto a prestaciones respecto a los modelos 1 C y 2 C. La guitarra Alhambra modelo 3C es una guitarra preciosa. Hecha a mano y cuidando todos los detalles, significa un paso más en la línea de estudio, un instrumento robusto, versátil y con un tono maravilloso. Con un sonido suave y un acabado de muy buena calidad, constituye una gran elección para trabajar la técnica, una elección segura para iniciarse en el estudio de la guitarra. El modelo 3 C está disponible con tapa de Cedro o de Abeto, siempre maciza y construida con maderas seleccionadas. En lo que respecta a la elaboración de los puentes, tanto para la silleta como para cejuela, se ha utilizado melamina, un material sintético altamente transmisor del sonido y que contribuye a conseguir un sonido redondo y definido. Disponible en Cutaway y cuerpo estrecho. El modelo 3 C de guitarras Alhambra también está disponible en versión cutaway (CW) para mejorar el acceso a la parte baja del diapasón, y en cutaway de cuerpo estrecho (CT). Esta variante reduce la profundidad de la guitarra (más estrecho en los lados), lo que permite una mayor accesibilidad si se toca en posición vertical y mediante un sistema de correa. En resumen, el modelo 3 C es una excelente compra dentro de un rango de precios adecuado para una guitarra de estudio."),
                    "alhambra 3f": ("Flamenca es la palabra más adecuada para definir a la guitarra Alhambra modelo 3 F. Un tono maravilloso, ligeramente más brillante en general que una guitarra clásica y con un sonido tremendo. El rasgueo con esta guitarra suena de una manera sorprendente, muy flamenco, “percusivo” y con buen volumen. Además es una guitarra que define muy bien la melodía y los bajos, aún siendo poderosos, están muy equilibrados. El modelo 3 F es un instrumento de la línea de estudio, cómodo, con muy buenas prestaciones y con una relación calidad-precio excepcional. Una buena elección para todo aquel que empieza en el mundo del flamenco. Con una tapa de Abeto Alemán macizo y un color claro por la utilización de Sicomoro en aros y fondos, la guitarra Alhambra modelo 3 F tiene una estética muy flamenca. Es un instrumento muy similar al modelo 4 F pero en este caso con clavijero plateado, diapasón de Palosanto de India y color claro en toda la caja de resonancia. Un modelo muy cómodo y que seguro satisface las exigencias de un intérprete flamenco. Incorpora dos silletas con diferente altura. El modelo 3 F incorpora dos silletas para poder elegir entre una acción de las cuerdas baja o algo más alta, la que más se adapte a los gustos del guitarrista. Ambas alturas están totalmente adaptadas a la guitarra, para que el ceceo sea el justo y además se asegure la comodidad en la interpretación. Diseñada para moverse rápidamente por el diapasón. Tanto la cejuela como la silleta son de melamina, un material altamente conductor del sonido y que ayuda a equilibrar el sonido en el instrumento."),
                    "alhambra 4f": ("El color de la guitarra Alhambra modelo 4 F no pasa desapercibido y lo convierte en un instrumento con mucha personalidad. Al igual que su homólogo clásico, el modelo 4 P, la flamenca 4 F es un instrumento muy equilibrado. Este modelo es la versión mejorada del modelo 3 F. En este caso con clavijero dorado y diapasón de ébano, además de su atractivo color anaranjado en toda la caja de resonancia. Una cualidad que confiere a este instrumento un valor añadido y lo convierte en una pieza que se diferencia del resto. Con una tapa de Abeto Alemán macizo, Sicomoro en aros y fondos,y el color anaranjado que la caracteriza, la guitarra Alhambra modelo 4 F tiene una estética muy flamenca. Al igual que el modelo 3 F, la 4 F es una guitarra con un sonido muy flamenco, se podría decir que es un sonido “percusivo” y con volumen. De hecho, con un simple rasgueo se puede apreciar el potente sonido flamenco y un tono que maravilla. Además es una guitarra que define muy bien la melodía y que cuenta con un buen equilibrio entre graves y agudos. El modelo 4 F es un instrumento de la línea de estudio, con la calidad que avala a Manufacturas Alhambra y con muy buenas prestaciones, donde cabe destacar la comodidad para el intérprete.. Una buena elección para todo aquel que empieza en el mundo del flamenco. Un modelo muy cómodo y que seguro satisface las exigencias de un intérprete flamenco. Incorpora dos silletas con diferente altura. El modelo 4 F incorpora dos silletas para poder adaptarlo a la acción de las cuerdas que prefiera el guitarrista. Una acción baja o algo más alta, pero siempre totalmente adaptadas a la guitarra. Un diseño adecuado para generar el ceceo justo y la mayor comodidad en la interpretación. Diseñada para moverse rápidamente por el diapasón. Tanto la cejuela como la silleta son de melamina, un material altamente conductor del sonido y que ayuda a equilibrar el sonido en el instrumento."),
                    "alhambra 5f": ("Una guitarra flamenca blanca elaborada con sicomoro en aros y fondo, abeto en la tapa y un mástil reforzado con ébano. El modelo 5 F es un instrumento con un sonido y tacto muy flamenco. Un sonido percusivo y potente pero a la vez limpio, donde los rasgueos suenan de manera extraordinaria. Además el modelo 5 F es una guitarra con la que se puede definir muy bien la melodía obteniendo un extraordinario equilibrio entre graves y agudos. Una guitarra elaborada con diapasón de ébano negro, cómoda y con un nivel de dureza bajo, una guitarra versátil con la que se pueden ejecutar todas las técnicas del flamenco. El modelo 5 F se construye con una tapa maciza de abeto, cuerpo de Sicomoro, clavijeros dorados y un cómodo mástil denominado ergoneck, en este caso elaborado con Samanguila y reforzado con ébano. Dos siletas con diferente altura. En el modelo 5 F se ha utilizado un varetaje tipo “classical 5”, que junto a una tapa solida de muy buena calidad, ofrece una dureza adecuada y mucha proyección. Además, el modelo 5 F de Guitarras Alhambra incorpora dos silletas. Una opción muy interesante para poder adaptar la acción de las cuerdas a las preferencias del guitarrista. Tanto la cejuela como la silleta son de melamina, un material altamente conductor de las vibraciones y que ayuda a equilibrar el sonido en el instrumento. Un gran instrumento. Una guitarra flamenca blanca, elegante, con acabado brillo e ideal para continuar con el estudio del difícil arte del flamenco."),
                    "alhambra 7fc": ("La Alhambra 7 Fc es una guitarra flamenca blanca con un hermoso ciprés macizo en aros y fondo. Tremendo, genuino, brillante y percutivo son algunas de los adjetivos que definen al modelo 7 Fc de Guitarras alhambra. Un instrumento con un impresionante sonido flamenco, tono constante y definición en la melodía. Además está totalmente equilibrada, tanto en potencia como en la relación entre graves y agudos. El modelo 7 Fc es un instrumento de la línea de conservatorio, con un bajo nivel de dureza y la calidad que avala a Manufacturas Alhambra. Una guitarra flamenca blanca muy cómoda y que seguro satisface las exigencias de un intérprete flamenco. Refuerzo de ébano en el mástil. Además del Ciprés macizo en aros y fondo y la tapa de Abeto Alemán macizo, esta guitarra incorpora ébano en el diapasón, clavijeros dorados y refuerzo de ébano en el mástil. En la elaboración de las guitarras Alhambra, el refuerzo de ébano se coloca en el interior del mástil, de forma que no se puede apreciar simple vista. Para poder ver la pieza de ébano se tiene que retirar la selleta. El refuerzo va colocado justo bajo del diapasón. Incorpora dos silletas con diferente altura. Cada guitarrista tiene una forma de tocar, lo que comporta que dentro de un mismo modelo tengan que haber variaciones. En este caso es posible variar la acción de las cuerdas mediante el cambio del “hueso” del puente, la cejuela. El modelo 7 Fc incorpora dos silletas con diferente altura, para conseguir una acción baja o algo más alta, pero siempre totalmente adaptadas a la guitarra. Una guitarra pensada para generar el ceceo justo cuando se requiera y posibilitar la mayor comodidad en la interpretación. Tanto la cejuela como la silleta son de melamina, un material altamente conductor del sonido y que ayuda a equilibrar el sonido en el instrumento.")
                }
                # Buscar el modelo en la base de datos
                from .models import Guitarra
                modelo_encontrado = None
                for modelo_key in modelos_info.keys():
                    if modelo_key in pregunta_limpia:
                        modelo_encontrado = modelo_key
                        break
                if modelo_encontrado:
                    guitarra = Guitarra.objects.filter(modelo__iexact=modelo_encontrado.replace("alhambra ", "").upper()).first()
                    precio = f"Precio: {guitarra.precio} €" if guitarra else "Precio no disponible."
                    respuesta = f"{modelos_info[modelo_encontrado]}\n\n{precio}"
                else:
                    respuesta = "¿Sobre qué modelo de guitarra Alhambra quieres información? Puedes preguntar por ejemplo: Alhambra 10FC, Alhambra 3F, etc."
            # Palos flamencos
            elif any(palo in pregunta_limpia for palo in ["bulería", "soleá", "tangos", "alegrías", "fandango", "rumba", "tanguillo"]):
                palo = next((p for p in ["bulería", "soleá", "tangos", "alegrías", "fandango", "rumba", "tanguillo"] if p in pregunta_limpia), None)
                historia = {
                    "bulería": "La bulería es uno de los palos más festivos y complejos del flamenco, originario de Jerez. Su compás es de 12 tiempos y es ideal para el baile improvisado.",
                    "soleá": "La soleá es uno de los palos más antiguos y profundos, con un compás de 12 tiempos y un carácter solemne y reflexivo.",
                    "tangos": "Los tangos flamencos son alegres y rítmicos, con compás de 4 tiempos, muy populares en fiestas y celebraciones.",
                    "alegrías": "Las alegrías son un palo luminoso y animado, típico de Cádiz, con compás de 12 tiempos y letras optimistas.",
                    "fandango": "El fandango es un palo de origen andaluz, muy variado, con versiones locales y gran riqueza melódica.",
                    "rumba": "La rumba flamenca es un palo influido por ritmos caribeños, muy bailable y popular en reuniones informales.",
                    "tanguillo": "El tanguillo es típico de Cádiz, con ritmo juguetón y letras humorísticas, usado en carnavales."
                }
                respuesta = historia.get(palo, "Ese palo flamenco tiene una historia fascinante. ¿Quieres saber más detalles?")
            # (apartado de vídeos eliminado, solo guitarras, historia y palos)
            # Artículos flamencos
            else:
                articulo = ArticuloFlamenco.objects.filter(titulo__icontains=pregunta).first()
                if articulo:
                    respuesta = articulo.contenido
                else:
                    respuesta = "No tengo información precisa sobre eso todavía, pero pronto podré ayudarte con más detalles sobre flamenco, guitarras y palos."
            # Evitar que la respuesta sea igual a la pregunta
            if respuesta and respuesta.strip().lower() == pregunta.strip().lower():
                respuesta = "He recibido tu pregunta, pero necesito más contexto para darte una respuesta útil sobre flamenco, guitarras o palos. ¿Puedes especificar más?"
            PreguntaIA.objects.create(
                usuario=request.user if request.user.is_authenticated else None,
                pregunta=pregunta,
                respuesta=respuesta,
                timestamp=timezone.now()
            )
        return render(request, self.template_name, {'respuesta': respuesta, 'pregunta': pregunta})

from django.shortcuts import render
from .models import Profile, PaloFlamenco, Video, Like, Comentario, ChatRoom, ChatMessage, DisponibilidadProfesor, ClasePrivada, Guitarra, ArticuloFlamenco, PreguntaIA
from django.contrib.auth import get_user_model
User = get_user_model()
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .forms import RegistroUsuarioForm, ProfileForm, ClasePrivadaForm, VideoForm

# Create your views here.
class UserListView(LoginRequiredMixin, ListView):

    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return User.objects.all()
        return User.objects.filter(pk=user.pk)

class UserDetailView(OwnerOrAdminRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    context_object_name = 'user'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.object
        profile = getattr(user, 'profile', None)
        avatar_url = None
        avatar_is_svg = False
        if profile and profile.avatar:
            avatar_str = str(profile.avatar)
            if avatar_str.lower().endswith('.svg'):
                avatar_url = f"/media/avatars/{avatar_str}"
                avatar_is_svg = True
            else:
                try:
                    avatar_url = profile.avatar.url
                except Exception:
                    avatar_url = None
        context['avatar_url'] = avatar_url
        context['avatar_is_svg'] = avatar_is_svg
        return context


from django.contrib.auth.mixins import LoginRequiredMixin

class UserCreateView(CreateView):
    model = User
    form_class = RegistroUsuarioForm
    template_name = 'users/user_form.html'
    success_url = reverse_lazy('guitarra:user_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        user = self.object
        Profile.objects.create(
            user=user,
            display_name=form.cleaned_data['display_name'],
            pais=form.cleaned_data['pais'],
        )
        return response

class UserUpdateView(OwnerOrAdminRequiredMixin, UpdateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'email']
    success_url = reverse_lazy('guitarra:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Asegura que el usuario tenga profile
        user = self.object
        profile = getattr(user, 'profile', None)
        if not profile:
            from .models import Profile
            profile = Profile.objects.create(user=user, display_name=user.username)
        if self.request.POST:
            context['profile_form'] = ProfileForm(self.request.POST, self.request.FILES, instance=profile)
        else:
            context['profile_form'] = ProfileForm(instance=profile)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        if profile_form.is_valid():
            self.object = form.save()
            profile_form.save()
            messages.success(self.request, 'Usuario y perfil actualizados correctamente.')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class UserDeleteView(AdminRequiredLoginMixin, DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('guitarra:user_list')


# Vista para editar usuario y perfil asociado
from django.shortcuts import redirect
from django.contrib import messages

class UserUpdateView(UpdateView):
    model = User
    template_name = 'users/user_form.html'
    fields = ['username', 'email']
    success_url = reverse_lazy('guitarra:user_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Asegura que el usuario tenga profile
        user = self.object
        profile = getattr(user, 'profile', None)
        if not profile:
            from .models import Profile
            profile = Profile.objects.create(user=user, display_name=user.username)
        if self.request.POST:
            context['profile_form'] = ProfileForm(self.request.POST, self.request.FILES, instance=profile)
        else:
            context['profile_form'] = ProfileForm(instance=profile)
        context['avatar_choices'] = [
            'ava.svg','blair.svg','dean.svg','jack.svg','lilly.svg','lux.svg','mary.svg','sommer.svg'
        ]
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        profile_form = context['profile_form']
        if profile_form.is_valid():
            self.object = form.save()
            profile = profile_form.save(commit=False)
            avatar_predefinido = self.request.POST.get('avatar_predefinido')
            if avatar_predefinido:
                # Si el valor no empieza por 'avatars/', lo añadimos
                if not avatar_predefinido.startswith('avatars/'):
                    profile.avatar = f"avatars/{avatar_predefinido}"
                else:
                    profile.avatar = avatar_predefinido
            profile.save()
            messages.success(self.request, 'Usuario y perfil actualizados correctamente.')
            return redirect(self.success_url)
        else:
            return self.render_to_response(self.get_context_data(form=form))

class UserDeleteView(DeleteView):
    model = User
    template_name = 'users/user_confirm_delete.html'
    success_url = reverse_lazy('guitarra:user_list')


from django.contrib.auth.mixins import LoginRequiredMixin

class VideoListView(LoginRequiredMixin, ListView):
    model = Video
    template_name = 'videos/video_list.html'
    context_object_name = 'videos'
    # paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        palo = self.request.GET.get('palo', '').strip()
        duracion_max = self.request.GET.get('duracion_max', '').strip()
        if palo:
            queryset = queryset.filter(palo_flamenco=palo)
        if duracion_max:
            try:
                # Convertir minutos a timedelta
                from datetime import timedelta
                minutos = float(duracion_max)
                queryset = queryset.filter(duracion__lte=timedelta(minutes=minutos))
            except ValueError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Palos flamencos para el filtro
        from .models import PaloFlamenco
        context['palos'] = [ (k, v) for k, v in PaloFlamenco.NOMBRE_CHOICES ]
        return context

class VideoDetailView(LoginRequiredMixin, DetailView):
    model = Video
    template_name = 'videos/video_detail.html'
    context_object_name = 'video'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        from .forms import ComentarioForm
        obj = self.get_object()
        if 'comentario_form' not in context:
            context['comentario_form'] = ComentarioForm(initial={'usuario': self.request.user, 'video': obj})
        # Likes: número total y si el usuario actual ha dado like
        try:
            context['likes_count'] = obj.likes.count()
            context['user_liked'] = obj.likes.filter(usuario=self.request.user).exists() if self.request.user.is_authenticated else False
        except Exception:
            context['likes_count'] = 0
            context['user_liked'] = False
        return context

    def post(self, request, *args, **kwargs):
        from .forms import ComentarioForm
        self.object = self.get_object()
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            comentario = comentario_form.save(commit=False)
            comentario.usuario = request.user
            comentario.video = self.object
            comentario.save()
            # Redirige al ancla de comentarios para mantener el scroll
            return redirect(f"{request.path}#comentarios-lista")
        # Si hay error, mostrar el formulario con errores
        context = self.get_context_data(comentario_form=comentario_form)
        return self.render_to_response(context)

class VideoCreateView(AdminRequiredLoginMixin, CreateView):
    model = Video
    form_class = VideoForm
    template_name = 'videos/video_form.html'
    success_url = reverse_lazy('guitarra:video_list')

class VideoUpdateView(AdminRequiredLoginMixin, UpdateView):
    model = Video
    form_class = VideoForm
    template_name = 'videos/video_form.html'
    success_url = reverse_lazy('guitarra:video_list')

class VideoDeleteView(AdminRequiredLoginMixin, DeleteView):
    model = Video
    template_name = 'videos/video_confirm_delete.html'
    success_url = reverse_lazy('guitarra:video_list')


@login_required
@require_POST
def toggle_like(request, pk):
    """Toggle like/unlike for a video. Returns JSON with new state and count."""
    video = get_object_or_404(Video, pk=pk)
    user = request.user
    # Verifica existencia
    existing = Like.objects.filter(usuario=user, video=video).first()
    if existing:
        existing.delete()
        liked = False
    else:
        Like.objects.create(usuario=user, video=video)
        liked = True
    return JsonResponse({'liked': liked, 'likes_count': video.likes.count()})


class GuitarraListView(LoginRequiredMixin, ListView):
    model = Guitarra
    template_name = 'guitarras/guitarra_list.html'
    context_object_name = 'guitarras'
    # paginate_by = 5

    def get_queryset(self):
        queryset = super().get_queryset()
        modelo = self.request.GET.get('modelo', '').strip()
        color = self.request.GET.get('color', '').strip()
        precio_min = self.request.GET.get('precio_min', '').strip()
        precio_max = self.request.GET.get('precio_max', '').strip()
        if modelo:
            queryset = queryset.filter(modelo=modelo)
        if color:
            queryset = queryset.filter(color=color)
        if precio_min:
            try:
                precio_min_val = float(precio_min)
                queryset = queryset.filter(precio__gte=precio_min_val)
            except ValueError:
                pass
        if precio_max:
            try:
                precio_max_val = float(precio_max)
                queryset = queryset.filter(precio__lte=precio_max_val)
            except ValueError:
                pass
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Modelos únicos existentes
        context['modelos'] = self.model.objects.values_list('modelo', flat=True).distinct().order_by('modelo')
        # Colores del modelo
        context['colores'] = self.model.COLOR_CHOICES
        return context

class GuitarraDetailView(LoginRequiredMixin, DetailView):
    model = Guitarra
    template_name = 'guitarras/guitarra_detail.html'
    context_object_name = 'guitarra'

    def get(self, request, *args, **kwargs):
        response = super().get(request, *args, **kwargs)
        # HistorialItem eliminado
        return response

class GuitarraCreateView(AdminRequiredLoginMixin, CreateView):
    model = Guitarra
    fields = ['marca', 'modelo', 'color', 'precio', 'stock', 'descripcion', 'imagen']
    template_name = 'guitarras/guitarra_form.html'
    success_url = reverse_lazy('guitarra:guitarra_list')

class GuitarraUpdateView(AdminRequiredLoginMixin, UpdateView):
    model = Guitarra
    fields = ['marca', 'modelo', 'color', 'precio', 'stock', 'descripcion', 'imagen']
    template_name = 'guitarras/guitarra_form.html'
    success_url = reverse_lazy('guitarra:guitarra_list')

class GuitarraDeleteView(AdminRequiredLoginMixin, DeleteView):
    model = Guitarra
    template_name = 'guitarras/guitarra_confirm_delete.html'
    success_url = reverse_lazy('guitarra:guitarra_list')


class ClasePrivadaListView(LoginRequiredMixin, ListView):
    model = ClasePrivada
    template_name = 'clases/claseprivada_list.html'
    context_object_name = 'clases'

    def get_queryset(self):
        user = self.request.user
        # El admin ve todas las clases, el usuario solo las suyas
        if user.is_staff or user.is_superuser:
            return ClasePrivada.objects.all().order_by('fecha_inicio')
        return ClasePrivada.objects.filter(models.Q(alumno=user) | models.Q(profesor=user)).order_by('fecha_inicio')

class ClasePrivadaDetailView(LoginRequiredMixin, DetailView):
    model = ClasePrivada
    template_name = 'clases/claseprivada_detail.html'
    context_object_name = 'clase'

    def get_queryset(self):
        user = self.request.user
        # El admin ve todas las clases, el usuario solo las suyas
        if user.is_staff or user.is_superuser:
            return ClasePrivada.objects.all()
        return ClasePrivada.objects.filter(models.Q(alumno=user) | models.Q(profesor=user))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clase = self.object
        ahora = timezone.now()
        context['estado_videollamada'] = clase.proximo_estado_videollamada(ahora)
        context['puede_unirse_ahora'] = clase.esta_activa(ahora)
        context['jitsi_join_url'] = clase.get_jitsi_join_url()
        return context

from django.contrib.auth.mixins import UserPassesTestMixin

class ClasePrivadaCreateView(AdminRequiredLoginMixin, CreateView):
    model = ClasePrivada
    form_class = ClasePrivadaForm
    template_name = 'clases_privadas/claseprivada_form.html'
    success_url = reverse_lazy('guitarra:claseprivada_list')

    def form_valid(self, form):
        response = super().form_valid(form)
        clase = self.object
        from .models import Notification
        alumno_nombre = getattr(clase.alumno, 'username', None) or getattr(clase.alumno, 'get_username', lambda: None)() or getattr(getattr(clase.alumno, 'profile', None), 'display_name', None) or 'alumno'
        profesor_nombre = getattr(clase.profesor, 'username', None) or getattr(clase.profesor, 'get_username', lambda: None)() or getattr(getattr(clase.profesor, 'profile', None), 'display_name', None) or 'profesor'
        Notification.objects.create(
            user=clase.profesor,
            message=f'Se ha creado una nueva clase privada: "{clase.titulo}" con el alumno {alumno_nombre}.',
            url=f'/clases/{clase.pk}/'
        )
        if clase.profesor != clase.alumno:
            Notification.objects.create(
                user=clase.alumno,
                message=f'Se ha creado una nueva clase privada: "{clase.titulo}" con el profesor {profesor_nombre}.',
                url=f'/clases/{clase.pk}/'
            )
        return response


class ClasePrivadaUpdateView(AdminRequiredLoginMixin, UpdateView):
    model = ClasePrivada
    form_class = ClasePrivadaForm
    template_name = 'clases_privadas/claseprivada_form.html'
    success_url = reverse_lazy('guitarra:claseprivada_list')


class ClasePrivadaDeleteView(AdminRequiredLoginMixin, DeleteView):
    model = ClasePrivada
    template_name = 'clases_privadas/claseprivada_confirm_delete.html'
    success_url = reverse_lazy('guitarra:claseprivada_list')


@login_required
def cambiar_estado_clase(request, pk):
    """Cambiar el estado de una clase privada con validación de permisos."""
    from django.http import JsonResponse
    from django.shortcuts import get_object_or_404
    
    if request.method != 'POST':
        return JsonResponse({'error': 'Método no permitido'}, status=405)
    
    clase = get_object_or_404(ClasePrivada, pk=pk)
    user = request.user
    nuevo_estado = request.POST.get('estado')
    
    # Validar que el nuevo estado sea válido
    valid_estados = dict(ClasePrivada.ESTADO_CHOICES)
    if nuevo_estado not in valid_estados:
        return JsonResponse({'error': 'Estado no válido'}, status=400)
    
    # Validar permisos
    es_admin = user.is_staff or user.is_superuser
    es_usuario_clase = (user == clase.profesor or user == clase.alumno)
    
    if not (es_admin or es_usuario_clase):
        return JsonResponse({'error': 'No tienes permiso para cambiar este estado'}, status=403)
    
    # Validar transiciones permitidas
    estado_actual = clase.estado
    
    # Si la clase está en estado final (realizada o cancelada), no permitir cambios
    if estado_actual in ['realizada', 'cancelada']:
        return JsonResponse({'error': 'No se puede cambiar el estado de una clase finalizada'}, status=403)
    
    # Admins pueden hacer cualquier transición
    if es_admin:
        # Permiso verificado
        pass
    # Usuarios solo pueden confirmar (pendiente -> confirmada)
    elif es_usuario_clase:
        if not (estado_actual == 'pendiente' and nuevo_estado == 'confirmada'):
            return JsonResponse({'error': 'Transición no permitida para usuario'}, status=403)
    
    # Aplicar cambio
    clase.estado = nuevo_estado
    clase.save()
    
    # Crear notificación si el estado cambió
    if estado_actual != nuevo_estado:
        from .models import Notification
        
        estado_display = dict(ClasePrivada.ESTADO_CHOICES).get(nuevo_estado, nuevo_estado)
        
        # Notificar a ambas partes
        for notif_user in [clase.profesor, clase.alumno]:
            if notif_user != user:  # No notificar al que hizo el cambio
                mensaje = f'El estado de la clase "{clase.titulo}" ha sido actualizado a {estado_display}.'
                Notification.objects.create(
                    user=notif_user,
                    message=mensaje,
                    url=f'/clases/{clase.pk}/'
                )
    
    return JsonResponse({'success': True, 'estado': nuevo_estado})


class NotificationPopupView(LoginRequiredMixin, ListView):
    model = Notification
    template_name = 'notifications/notification_popup.html'
    context_object_name = 'notifications'

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by('-created_at')[:10]

    def get(self, request, *args, **kwargs):
        if request.GET.get('ajax') == '1':
            if request.GET.get('count') == '1':
                count = Notification.objects.filter(user=request.user, read=False).count()
                return JsonResponse({'count': count})
            # Renderizar HTML del popup
            notifications = self.get_queryset()
            html = render_to_string('notifications/notification_popup.html', {'notifications': notifications})
            return JsonResponse({'html': html})
        return super().get(request, *args, **kwargs)

@require_POST
def add_to_cart(request, guitarra_id):
    cart = request.session.get('cart', {})
    cart[str(guitarra_id)] = cart.get(str(guitarra_id), 0) + 1
    request.session['cart'] = cart
    return redirect('guitarra:guitarra_list')

def cart_view(request):
    cart = request.session.get('cart', {})
    guitarras = []
    total = 0
    for gid, qty in cart.items():
        guitarra = get_object_or_404(Guitarra, pk=gid)
        guitarras.append({'guitarra': guitarra, 'cantidad': qty, 'subtotal': guitarra.precio * qty})
        total += guitarra.precio * qty
    return render(request, 'cart/cart_detail.html', {'guitarras': guitarras, 'total': total})

@require_POST
def remove_from_cart(request, guitarra_id):
    cart = request.session.get('cart', {})
    if str(guitarra_id) in cart:
        del cart[str(guitarra_id)]
        request.session['cart'] = cart
    return redirect('guitarra:cart_view')


# ====== VISTAS DE CHECKOUT ======

@login_required
def checkout_view(request):
    """Vista de checkout - mostrar formulario de dirección de envío"""
    from .forms import CheckoutForm
    cart = request.session.get('cart', {})
    
    if not cart:
        return redirect('guitarra:cart_view')
    
    # Obtener guitarras del carrito
    guitarras = []
    total = 0
    for gid, qty in cart.items():
        guitarra = get_object_or_404(Guitarra, pk=gid)
        
        # Validar stock
        if guitarra.stock < qty:
            from django.contrib import messages
            messages.error(request, f'Stock insuficiente de {guitarra.marca} {guitarra.modelo}. Solo hay {guitarra.stock} disponibles.')
            return redirect('guitarra:cart_view')
        
        guitarras.append({'guitarra': guitarra, 'cantidad': qty, 'subtotal': guitarra.precio * qty})
        total += guitarra.precio * qty
    
    if request.method == 'POST':
        form = CheckoutForm(request.POST)
        if form.is_valid():
            # Guardar la orden temporalmente en la sesión
            request.session['checkout_data'] = {
                'nombre_completo': form.cleaned_data['nombre_completo'],
                'email': form.cleaned_data['email'],
                'telefono': form.cleaned_data['telefono'],
                'direccion': form.cleaned_data['direccion'],
                'ciudad': form.cleaned_data['ciudad'],
                'codigo_postal': form.cleaned_data['codigo_postal'],
                'pais': form.cleaned_data['pais'],
                'notas': form.cleaned_data['notas'],
            }
            return redirect('guitarra:checkout_confirm')
    else:
        # Pre-llenar con datos del usuario si existe
        initial_data = {
            'nombre_completo': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'pais': getattr(request.user.profile, 'pais', '') if hasattr(request.user, 'profile') else '',
        }
        form = CheckoutForm(initial=initial_data)
    
    context = {
        'form': form,
        'guitarras': guitarras,
        'total': total,
        'cart': cart,
    }
    return render(request, 'checkout/checkout.html', context)


@login_required
def checkout_confirm_view(request):
    """Vista de confirmación - resumen de la orden"""
    cart = request.session.get('cart', {})
    checkout_data = request.session.get('checkout_data')
    
    if not cart or not checkout_data:
        return redirect('guitarra:cart_view')
    
    # Obtener guitarras del carrito
    guitarras = []
    total = 0
    for gid, qty in cart.items():
        guitarra = get_object_or_404(Guitarra, pk=gid)
        guitarras.append({'guitarra': guitarra, 'cantidad': qty, 'subtotal': guitarra.precio * qty})
        total += guitarra.precio * qty
    
    if request.method == 'POST':
        request.session['checkout_payment_total'] = str(total)
        request.session.modified = True
        return redirect('guitarra:checkout_payment')
    
    context = {
        'guitarras': guitarras,
        'total': total,
        'checkout_data': checkout_data,
    }
    return render(request, 'checkout/checkout_confirm.html', context)


@login_required
def checkout_payment_view(request):
    """Vista de pago ficticio para simular una pasarela sin cobrar dinero real."""
    from .forms import FakePaymentForm

    cart = request.session.get('cart', {})
    checkout_data = request.session.get('checkout_data')

    if not cart or not checkout_data:
        return redirect('guitarra:cart_view')

    guitarras = []
    total = 0
    for gid, qty in cart.items():
        guitarra = get_object_or_404(Guitarra, pk=gid)
        guitarras.append({'guitarra': guitarra, 'cantidad': qty, 'subtotal': guitarra.precio * qty})
        total += guitarra.precio * qty

    if request.method == 'POST':
        form = FakePaymentForm(request.POST)
        if form.is_valid():
            request.session['fake_payment_data'] = {
                'card_holder': form.cleaned_data['card_holder'],
                'card_number': form.cleaned_data['card_number'][-4:],
                'expiry_date': form.cleaned_data['expiry_date'],
            }
            request.session.modified = True
            return process_checkout(request, guitarras, total, checkout_data)
    else:
        initial = {
            'card_holder': checkout_data['nombre_completo'],
        }
        form = FakePaymentForm(initial=initial)

    context = {
        'form': form,
        'guitarras': guitarras,
        'total': total,
        'checkout_data': checkout_data,
    }
    return render(request, 'checkout/checkout_payment.html', context)


def process_checkout(request, guitarras, total, checkout_data):
    """Procesar la orden y guardar en BD"""
    from .models import Order, OrderItem
    from django.contrib import messages
    
    cart = request.session.get('cart', {})
    
    try:
        # Crear la orden
        order = Order.objects.create(
            usuario=request.user,
            nombre_completo=checkout_data['nombre_completo'],
            email=checkout_data['email'],
            telefono=checkout_data['telefono'],
            direccion=checkout_data['direccion'],
            ciudad=checkout_data['ciudad'],
            codigo_postal=checkout_data['codigo_postal'],
            pais=checkout_data['pais'],
            notas=checkout_data['notas'],
            total=total,
            estado='confirmada',  # Cambiar a 'pendiente' si usas pasarela de pago real
        )
        
        # Crear items de la orden y descontar stock
        for guitarra_data in guitarras:
            guitarra = guitarra_data['guitarra']
            cantidad = guitarra_data['cantidad']
            
            # Validar stock una última vez
            if guitarra.stock < cantidad:
                order.delete()
                messages.error(request, f'Stock insuficiente. La guitarra {guitarra.marca} {guitarra.modelo} no tiene suficiente inventario.')
                return redirect('guitarra:cart_view')
            
            # Crear OrderItem
            OrderItem.objects.create(
                order=order,
                guitarra=guitarra,
                cantidad=cantidad,
                precio_unitario=guitarra.precio,
            )
            
            # Descontar stock
            guitarra.stock -= cantidad
            guitarra.save()
        
        # Limpiar carrito y datos de checkout de la sesión
        del request.session['cart']
        del request.session['checkout_data']
        request.session.pop('checkout_payment_total', None)
        request.session.pop('fake_payment_data', None)
        request.session.modified = True
        
        messages.success(request, f'¡Pago de prueba completado! Número de orden: #{order.pk}')
        return redirect('guitarra:checkout_success', order_id=order.pk)
    
    except Exception as e:
        from django.contrib import messages
        messages.error(request, f'Error al procesar la orden: {str(e)}')
        return redirect('guitarra:checkout_confirm')


@login_required
def checkout_success_view(request, order_id):
    """Vista de éxito - mostrar resumen de la orden"""
    from .models import Order
    order = get_object_or_404(Order, pk=order_id, usuario=request.user)
    
    context = {
        'order': order,
        'items': order.items.all(),
    }
    return render(request, 'checkout/checkout_success.html', context)


@login_required
def my_orders_view(request):
    """Vista de historial de pedidos del usuario"""
    from .models import Order
    orders = Order.objects.filter(usuario=request.user).order_by('-fecha_creacion')
    
    context = {
        'orders': orders,
    }
    return render(request, 'checkout/my_orders.html', context)


@login_required
def order_detail_view(request, order_id):
    """Vista de detalle de una orden"""
    from .models import Order
    order = get_object_or_404(Order, pk=order_id, usuario=request.user)
    
    context = {
        'order': order,
        'items': order.items.all(),
    }
    return render(request, 'checkout/order_detail.html', context)


def handler_404(request, exception=None):
    """Renderiza la plantilla 404 personalizada."""
    return render(request, '404.html', status=404)

