let errores = []
let tokens = []
let cuerpoAst = "";
let cuerpoTable = [];


async function loadFile(file) {
    let text = await file.text();
    document.getElementById('output').value = text;
}

function guardarArchivos(contenido, nombre){
    const a = document.createElement("a");
    const archivo = new Blob([contenido], { type: 'text/plain' });
    const url = URL.createObjectURL(archivo);
    a.href = url;
    a.download = nombre;
    a.click();
    URL.revokeObjectURL(url);
}

//-----------------------------#MANEJO DE PESTAÑAS
let pestañas = [];
let contadorPestañas = 1;
let indice = 0;
if(pestañas.length==0){
  pestañas.push(document.getElementById('output').value);
}

function addPestaña(){
  if(pestañas.length >= 1){
    var code = "";
    for(var i = 0; i <= pestañas.length; i++){
        code +=`<button class="pes" onclick="irPestaña(${i})">${i+1}</button>\n`
    }
    pestañas.push(document.getElementById('output').value);
    indice = pestañas.length-1;
    document.getElementById('output').value = ""
    $('#div-pestañas').html(code)
  }

}

const irPestaña = (index) => {
  // Guardar cambios de la pestaña actual antes de cambiar
  indice = index;
  //pestañas[index] = document.getElementById("output").value;
  // Cambiar a la pestaña deseada
  document.getElementById("output").value = pestañas[index];
}

function loadPestaña(){
  pestañas[indice] = document.getElementById("output").value;
}

function delPestaña(){
  pestañas.splice(indice, 1);
  
  indice = indice-1;
  var code = "";
  for(var i = 0; i < pestañas.length; i++){
    code +=`<button class="pes" onclick="irPestaña(${i})">${i+1}</button>\n`
  }
  $('#div-pestañas').html(code);
  document.getElementById("output").value = pestañas[indice]
  //pestañas[indice] = document.getElementById("output").value;
}

//-----------------------------#MANEJO DE REPORTES
function actualizar(){
  const codigo = document.getElementById('output').value // Obtener el código del textarea
  fetch("http://localhost:5000/interpreter", {
    method: "POST",
    body: JSON.stringify({ code: codigo }),
    headers: {
      "Content-Type": "application/json",
    },
  }).then((res) => res.json())
  .then((data) => {
    const consola = document.getElementById("editor");
    consola.value = data.console; // Mostrar la respuesta en el textarea
    console.log(data.console);
    //this.showAst(data.ast)
    //cuerpoAst = data.ast;
    cuerpoTable = data.tabla_simbolos;
    //symTable = data.Tsimbol;
    //console.log(data.Tsimbol)
    //console.log(data.errores)
    //tokens = data.VToken;
    errores = data.errores
    console.log(errores)
    console.log(cuerpoTable)
    //localStorage.setItem("errores",JSON.stringify(data.errores));
    
  })
  .catch((error) => console.error(error));
}

//-----------------------------#MANEJO DE ARCHIVOS

function ErrorReporte(){
  this.ocultar("consola","ERRORES");
  let cuerpo = "";
  console.log(errores)
  if(errores != "ninguno"){
    console.log(errores.length)
  for(var i = 0; i < errores.length; i++){
    let cadena = errores[i].toString();
    let columnas = cadena.split(","); 
    cuerpo += `

    <tr>
      <td>${i}</td>
      <td>${columnas[0]}</td>
      <td>${columnas[1]}</td>
      <td>${columnas[2]}</td>
      <td>${columnas[3]}</td>
    </tr>
`;
  }
  $('#studentsTable tbody').html(cuerpo)
  }
  
}


function TablaReporte(){
  this.ocultar("consola","TablaS");
  console.log(cuerpoTable)
  let cuerpo = "";
  if(cuerpoTable != "ninguno"){
    console.log(cuerpoTable.length)
  for(var i = 0; i < cuerpoTable.length; i++){
    let cadena = cuerpoTable[i].toString();
    let columnas = cadena.split(","); 
    let tipo=""
    if (columnas[2] == 0){
      tipo = "number"
    }else if(columnas[2] == 1){
      tipo = "float"
    }else if(columnas[2] == 2){
      tipo = "string"
    }else if(columnas[2] == 3){
      tipo = "boolean"
    }else if(columnas[2] == 4){
      tipo = "array"
    }else if(columnas[2] == 5){
      tipo = "struct"
    }else if(columnas[2] == 6){
      tipo = "null"
    }else if(columnas[2] == 7){
      tipo = "char"
    }else if(columnas[2] == 8){
      tipo = "matrix"
    }
    cuerpo += `

    <tr>
      <td>${columnas[0]}</td>
      <td>${columnas[1]}</td>
      <td>${tipo}</td>
      <td>${columnas[3]}</td>
      <td>${columnas[4]}</td>
      <td>${columnas[5]}</td>
    </tr>
`;
  }
    $('#SymbolTable tbody').html(cuerpo)
  }
}

function hideErrores(){
  this.ocultar("ERRORES", "consola")
}

function hideTable(){
  this.ocultar("TablaS", "consola")
}

function ocultar(sec1, sec2){
  const secConsola = document.getElementById(sec1);
  secConsola.hidden = true;
  const secErrores = document.getElementById(sec2);
  secErrores.hidden = false;
}