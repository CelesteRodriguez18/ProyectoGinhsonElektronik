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

function redirigirAdminAgregar() {
  location.href = "/agregarProductos";
}

function redirigirAdminBorrar() {
  location.href = "/borrarProductos";
}

function redirigirAdminModificar() {
  location.href = "/modificarProductos";
}

function pagAnterior() {
  location.href = "/opcionesAdmin";
}

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