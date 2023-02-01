function formularioAdmin() {
  var usuario = document.getElementById("usuario")
  var password = document.getElementById("password") 
  console.log(password.value)

  document.getElementById("formularioAdmin").submit()

  /* SUBMIT A FORM DE HTML */
  
  $.ajax({ 
    url:"/ingreso", 
    type:"POST", 
    data: {"usuario": usuario,
          "password": password,
          }, 

    success: function(response){  
      datos = response
      //console.log(datos)
      console.log('Llega al java')
      location.href= '/opcionesAdmin'
      if(datos == true) {
        alert(`Se registró su respuesta`)
      }
    }, 
    error: function(error){ 
      console.log(error); 
  }, });
}

// MODAL PARA SECCIÓN PRODUCTOS
function mostrarModal(nombre) {
  dialog = document.getElementById("modal"+nombre);
  dialog.showModal();
}

function ocultarModal(nombre) {
  dialog = document.getElementById("modal"+nombre);
  dialog.close();
}

//
function seleccionar(productos) {
  productos = productos
  console.log(productos)
  $.ajax({ 
    url:"/seleccionarSeguridad", 
    type:"POST", 
    data: {"productos": productos,
          }, 

    success: function(response){  
      console.log(productos)
      location.href= '/seleccionarSeguridad'
      datos = (response); 
      console.log(datos)
      
    }, 
    error: function(error){ 
      console.log(error); 
  }, });
}




// FUNCIONES DE ADMINISTRADOR

// IMÁGENES
function detectarImagen() {
  let cargadorImagenes = document.getElementById("selecArchivo");
  if(cargadorImagenes.files.length > 0) {
    //Tengo imagenes subidas
    document.getElementById("selecArchivoLabel").innerHTML = "Imagen Adjunta";
  }
  else {
    document.getElementById("selecArchivoLabel").innerHTML = "Adjunte una imagen";
  }
}

function detectarImagenMod() {
  let cargadorImagenes = document.getElementById("imagen");
  if(cargadorImagenes.files.length > 0) {
    //Tengo imagenes subidas
    document.getElementById("selecArchivoLabel").innerHTML = "Imagen Adjunta";
  }
  else {
    document.getElementById("selecArchivoLabel").innerHTML = "Adjunte una imagen";
  }
}

// REDIRIGIR A LAS OPCIONES
function redirigirAdminAgregar() {
  alert('Usted será redirigido a la sección de Agregar Productos')
  location.href = '/agregarProductos';
}

function redirigirAdminBorrar() {
  alert('Usted será redirigido a la sección de Borrar Productos')
  location.href = '/borrarProductosGeneral';
}

function redirigirAdminModificar() {
  alert('Usted será redirigido a la sección de Modificar Productos')
  location.href = '/modificarProductos';
}

// BORRAR PRODUCTOS
function eliminar(producto) {
  producto = producto
  console.log(producto)
  $.ajax({ 
    url:"/eliminar", 
    type:"POST", 
    data: {"producto": producto,
          }, 

    success: function(response){
      console.log(producto)
      datos = (response); 
      console.log(datos)
      console.log(producto)
      document.getElementById(producto).remove()
      alert("Se eliminó el producto: " + datos)
      
    }, 
    error: function(error){ 
      console.log(error); 
  }, });
}

function borrarProducto() {
  nombreProducto = document.getElementById("nombreProducto")
  
  $.ajax({ 
    url:"/opcionesBorrarProducto", 
    type:"POST", 
    data: {"nombreProducto": nombreProducto,
          }, 

    success: function(response){  
      datos = response
    }, 
    error: function(error){ 
      console.log(error); 
  }, });

}

// MODIFICAR PRODUCTOS
function modificar(producto) {
  producto = producto
  info = document.getElementById("info").value;
  console.log(producto)
  console.log(info)
  $.ajax({ 
    url:"/modificar", 
    type:"POST", 
    data: {"producto": producto,
           "info": info,
          }, 

    success: function(response){ 
      console.log(producto)
      datos = (response); 
      console.log(datos)
      console.log(producto)
      alert("Se modificó el producto: "+ datos)
      
    }, 
    error: function(error){ 
      console.log(error); 
  }, });
}

function modificarCategoria(producto) {
  producto = producto
  categoria = document.getElementById("categoria").value;
  console.log(producto)
  console.log(categoria)
  $.ajax({ 
    url:"/modificarCategoria", 
    type:"POST", 
    data: {"producto": producto,
           "categoria": categoria,
          }, 

    success: function(response){ 
      console.log(producto)
      datos = (response); 
      console.log(datos)
      console.log(producto)
      alert("Se modificó el producto: "+ datos)
      
    }, 
    error: function(error){ 
      console.log(error); 
  }, });
}

function modificarLinea(producto) {
  producto = producto
  linea = document.getElementById("linea").value;
  console.log(producto)
  console.log(linea)
  $.ajax({ 
    url:"/modificarLinea", 
    type:"POST", 
    data: {"producto": producto,
           "linea": linea,
          }, 

    success: function(response){ 
      console.log(producto)
      datos = (response); 
      console.log(datos)
      console.log(producto)
      alert("Se modificó el producto: "+ datos)
      
    }, 
    error: function(error){ 
      console.log(error); 
  }, });
}

function modificarLinea(producto) {
  producto = producto
  linea = document.getElementById("linea").value;
  console.log(producto)
  console.log(linea)
  $.ajax({ 
    url:"/modificarLinea", 
    type:"POST", 
    data: {"producto": producto,
           "linea": linea,
          }, 

    success: function(response){ 
      console.log(producto)
      datos = (response); 
      console.log(datos)
      console.log(producto)
      alert("Se modificó el producto: "+ datos)
      
    }, 
    error: function(error){ 
      console.log(error); 
  }, });
}

function modificarNombre(producto) {
  producto = producto
  nuevoNombre = document.getElementById("nuevoNombre").value;
  console.log(producto)
  console.log(nuevoNombre)
  $.ajax({ 
    url:"/modificarNombre", 
    type:"POST", 
    data: {"producto": producto,
           "nuevoNombre": nuevoNombre,
          }, 

    success: function(response){ 
      console.log(producto)
      datos = (response); 
      console.log(datos)
      console.log(producto)
      alert("Se modificó el producto: "+ datos)
      
    }, 
    error: function(error){ 
      console.log(error); 
  }, });
}



function modificarImagen(producto) {
  producto = producto
  imagen = document.getElementById("imagen").files[0].name;
  console.log(producto)
  console.log(imagen)
  $.ajax({ 
    url:"/modificarImagen", 
    type:"POST", 
    data: {"producto": producto,
           "imagen": imagen,
          }, 

    success: function(response){ 
      console.log(producto)
      datos = (response); 
      console.log(datos)
      console.log(producto)
      alert("Se modificó el producto: "+ datos)
      
    }, 
    error: function(error){ 
      console.log(error); 
  }, });
}

function modificarProducto() {
  nombreProducto = document.getElementById("nombreProducto")
  console.log(nombreProducto)
  
  $.ajax({ 
    url:"/opcionesModificar", 
    type:"POST", 
    data: {"nombreProducto": nombreProducto,
          }, 

    success: function(response){  
      datos = response
    }, 
    error: function(error){ 
      console.log(error); 
  }, });

}

function modificaProducto() {
  nombreProducto = document.getElementById("nombreProducto")
  console.log(nombreProducto)
  
  $.ajax({ 
    url:"/modificacionImagenBuscador", 
    type:"POST", 
    data: {"nombreProducto": nombreProducto,
          }, 

    success: function(response){  
      datos = response
    }, 
    error: function(error){ 
      console.log(error); 
  }, });

}


/* FORMULARIO CONTACTO

function formulario() {
  var nombre = document.getElementById("nombre").value 
  var correo = document.getElementById("correo").value 
  var mensaje = document.getElementById("mensaje").value  

  console.log(nombre)
  console.log(correo)
  console.log(mensaje)

  var contieneArroba = false
  if (correo.includes('@')){
    contieneArroba = true
  }
  if (nombre.length == 0 || correo.length == 0 || mensaje.length == 0 || contieneArroba == false)  {
    alert("Faltan ingresar datos")
    return 0;
  }
  
  
  $.ajax({ 
    url:"/contacto", 
    type:"POST", 
    data: {"nombre": nombre,
          "correo": correo,
          "mensaje": mensaje,
          }, 

    success: function(response){  
      datos = response
      //if(datos == true) {
      alert(`Se registró su respuesta`)
      location.href= '/'
      //}
    }, 
    error: function(error){ 
      console.log(error); 
  }, });

}
*/