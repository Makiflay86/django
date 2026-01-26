from django.shortcuts import render,redirect
from django.http import HttpResponse # Necesario para poder responder al cliente
from HolaMundo.models import Author,Book
from HolaMundo.forms import AutorForm, BookForm

# Create your views here.

# forma de responder al cliente cuando hace un http
def hola_mundo (request): # El request captura las peticiones de los clientes
    return HttpResponse ("<h1>hola mundo</h1>")
# Con esto hemos habilitado una vista, pero hay que además enlazar el proyecto con la aplicación

def home (request): # Pinta una página con render, también hay que darlo de alta en urls.py
    return render(request,'index.html') # La página index.html hay que crearla dentro del archivo de configuración de todo proyecto de django, settings.py



# Tabla de autores
def author (request):
    author = Author.objects.all()
    return render(request,'author.html',{'authors': author})

# Crear los autores
def author_create(request):
    if request.method == 'GET':
        return render(request, 'author_create.html', {'author_form': AutorForm}) 
        #Si tenemos las páginas
        #dentro de alguna carpeta dentro de template, entonces habría que especificar el nombre de la
        #carpeta return Ej:render(request, 'nombre_carpeta/create_autor.html')

    #Hemos añadido el contexto para pasarlo como parámetro a la página create_autor.html
    if request.method == 'POST':
    #Estaremos aqui en esta opción cuando le damos a guardar. Para obtener la información que
    #envía el formulario:
    # EN request.POST es dónde tenemos toda esa información. De hecho si imprimimos esa variable la
    #podemos ver.
        form = AutorForm(data = request.POST)
    
    #Hemos creado una instancia de un form de Django al que le estamos pasando los datos usando la
    #variable data, de esta manera entiende que se va a registrar una información (que va a ser un
    #diccionario)
    if form.is_valid: #Realizará de forma automática las validaciones que se han establecido en
    #el modelo
        form.save() #Guarda en la BD. En pocas lineas hemos validado y guardado.
        return redirect ('/author/') #Hay que importar el redirect en shortcuts. Debe redireccionar
        #al listado de autores.
    else:
    #Debo volver a crear una instancia del forma para dar la opción de poder escribir otra vez
    #los datos, con los mismos datos que ha introducido para que vea qué cual puede ser el error.
        form = AutorForm(data = request.POST)
        return render (request, 'author_create.html',{'author_form': AutorForm}) #Es como si fuera un
        #GET

# Editar los autores
def author_update (request, pk = None): #Recibe la clave del autor que queremos actualizar.
    author = Author.objects.get(pk = pk) #Nos buscará el registro que coincida con la clave que le
    #pongamos aquí.En el caso en el que no lo encuentre, va a generar un error, con lo que hay que
    #capturar excepción
    #Existe otra opción que es con el filter, pero para grandes cantidades de datos el get es más
    #óptimo
    # autor=Author.objects.filter(pk=pk).first Esta sería la otra forma

    if request.method == 'GET':
        author_form = AutorForm(instance = author) #todo form basado en un modelo tiene este atributo que
        #hace referencia a la instancia de un objeto de la BD. Al pasarle este objeto, Django toma los
        #atributos de éste y asociarlo a su campo html correspondiente que le estamos generando con el Form.
        return render (request,'author_update.html',{'author':author,'author_form':author_form}) #si la
        #página la tenemos dentro de template/core, hay que poner core/update_autor.html
        #Le pasamos también la variable author_form para obtener los valores que deseamos editar.

    if request.method == 'POST':
        author_form = AutorForm(data = request.POST, instance = author) #Combinamos obtene información así
        #como asociarla a una instancia. De esta forma Django entiende que es una actualización
        #El resto del proceso será igual que en la creación de autores.
        
    if author_form.is_valid():
        author_form.save()
        return redirect ('/author/') #Se realiza igual que en la creación
    else: #Creo nueva instancia con la misma información que tenía y además pinto la información
        #en el template
        author_form = AutorForm(data = request.POST, instance = author)
        return render (request,'author_update.html',{'author':author,'author_form':author_form})

# Eliminar los autores
def author_delete (request, pk = None):
    #Eliminación directa
    Author.objects.filter(pk = pk).delete()
    #Otra forma de hacerlo
    #autor=Author.objects.get(pk=pk)
    #autor.delete()
    return redirect ('/author/')



# Tabla de libros
def book (request):
    book = Book.objects.all()
    return render(request,'book.html',{'books': book})

# Crear los libros
def book_create(request):
    if request.method == 'GET':
        return render(request, 'book_create.html', {'book_form': BookForm})
    
    if request.method == 'POST':
        book_form = BookForm(data = request.POST) #data es lo que le enviamos para que inserte
    
    if book_form.is_valid(): #Valido la información que me envían para guardar el libro. Realmente
    #la información está en book_form.
        new_book = Book.objects.create(title = book_form.cleaned_data.get('title'),cod = book_form.cleaned_data.get('cod'))
        #Hasta aquí habrá registrado mi libro. Ahora pasamos al campo relaciona.
        #Ahora guardo la instancia que acabo de registrar, envíandole el id que quiero guardar
        #el atributo set, lo tiene el campo implicado en la relación manytomany
        new_book.author.set(book_form.cleaned_data.get('author'))
        return redirect('/book/')
    else:
        return render(request, 'book_create.html',{'book_form':BookForm}) #Le enviamos a la
        #página de creación con los datos incluidos para que pueda comprobar qué dato está mal.

