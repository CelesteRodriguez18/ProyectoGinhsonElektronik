/*
const toggle = document.querySelector('.toggle')
const links = document.querySelector('.links')

toggle.addEventListener('click', () => {
    toggle.classList.toggle('rotate')
    links.classList.toggle('inactive')
})
*/


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

function detectarImagen() {
  let cargadorImagenes = document.getElementById("selecArchivo");
  if(cargadorImagenes.files.length > 0) {
    //Tengo imagenes subidas
    document.getElementById("selecArchivoLabel").innerHTML = "Imágen Adjunta";
  }
  else {
    document.getElementById("selecArchivoLabel").innerHTML = "Adjunte una imagen";
  }
}

function detectarImagenMod() {
  let cargadorImagenes = document.getElementById("selecArchivo");
  if(cargadorImagenes.files.length > 0) {
    //Tengo imagenes subidas
    document.getElementById("selecArchivoLabel").innerHTML = "Imágen Adjunta";
  }
  else {
    document.getElementById("selecArchivoLabel").innerHTML = "Adjunte una imagen";
  }
}


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
/*
function deseleccionar(check1, check2, check3) {
  if (document.getElementById(check1).checked == true) {
    document.getElementById(check1).checked = false
  }
  if (document.getElementById(check2).checked == true) {
    document.getElementById(chec2).checked = false
  }
  if (document.getElementById(check3).checked == true) {
    document.getElementById(check3).checked = false
  }
}
*/
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

function modificarImagen(producto) {
  producto = producto
  selecArchivo = document.getElementById("selecArchivo").value;
  console.log(producto)
  console.log(selecArchivo)
  $.ajax({ 
    url:"/modificarImagen", 
    type:"POST", 
    data: {"producto": producto,
           "selecArchivo": selecArchivo,
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

/*
function borrarProductoSeguridad() {
  nombreProductoSeguridad = document.getElementById("nombreProductoSeguridad")
  
  $.ajax({ 
    url:"/opcionesBorrarProductoSeguridad", 
    type:"POST", 
    data: {"nombreProductoSeguridad": nombreProductoSeguridad,
          }, 

    success: function(response){  
      datos = response
    }, 
    error: function(error){ 
      console.log(error); 
  }, });

}

function borrarProductoNautica() {
  nombreProductoNautica = document.getElementById("nombreProductoNautica")
  
  $.ajax({ 
    url:"/opcionesBorrarProductoNautica", 
    type:"POST", 
    data: {"nombreProductoNautica": nombreProductoNautica,
          }, 

    success: function(response){  
      datos = response
    }, 
    error: function(error){ 
      console.log(error); 
  }, });

}

function borrarProductoIndustria() {
  nombreProductoIndustria = document.getElementById("nombreProductoIndustria")
  
  $.ajax({ 
    url:"/opcionesBorrarProductoIndustria", 
    type:"POST", 
    data: {"nombreProductoIndustria": nombreProductoIndustria,
          }, 

    success: function(response){  
      datos = response
    }, 
    error: function(error){ 
      console.log(error); 
  }, });

}

function borrarProductoDispositivos() {
  nombreProductoDispositivos = document.getElementById("nombreProductoDispositivos")
  
  $.ajax({ 
    url:"/opcionesBorrarProductoDispositivos", 
    type:"POST", 
    data: {"nombreProductoDispositivos": nombreProductoDispositivos,
          }, 

    success: function(response){  
      datos = response
    }, 
    error: function(error){ 
      console.log(error); 
  }, });

}
*/

// FUNCION GENERAL
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