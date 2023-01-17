<?php
if ($_POST[mensaje]!="" and $_POST[email]!="") {
	$asunto = "Contacto desde WebSite";
	$cuerpo = "Nombre: ".$_POST[nombre]." <BR>Empresa: ".$_POST[empresa]." <BR>Cargo: ".$_POST[cargo]." <BR>Teléfono: ".$_POST[telefono]." <BR>E-mail: ".$_POST[email]." <BR><BR>".nl2br($_POST[mensaje]);
	$myname= "info desde el website";
	$myreplyemail = $myemail = "info@ginhson.com.ar";
		//$myreplyemail = $myemail = "info@ginhson.com.ar";
	$headers = "MIME-Version: 1.0\r\n"; 
	$headers .= "Content-type: text/html; charset=iso-8859-1\r\n"; 
	$headers .= "From: ".$_POST[nombre]." <".$_POST[email].">\r\n"; 
	$headers .= "X-Priority: 3\r\n"; 
	$headers .= "X-MSMail-Priority: Normal\r\n"; 
	$headers .= "X-Mailer: Just My Server"; 
	mail($myemail,$asunto,$cuerpo,$headers);
	header('location:http://www.ginhson.com.ar/confirmacion.html');
	exit();
	
}
header('location:http://www.ginhson.com.ar/contactenos.html');
exit();

?>