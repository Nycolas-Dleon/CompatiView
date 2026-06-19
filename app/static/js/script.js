function abrirAlerta(event) {
    event.preventDefault(); // Impede o link de navegar
    const alerta = document.getElementById("alerta-embreve");
    alerta.classList.add("mostrar");

    setTimeout(() => {
            alerta.classList.remove("mostrar");
        }, 5000); 
}


function fecharAlerta(event) {
    const alerta = document.getElementById("alerta-embreve");
    alerta.classList.remove("mostrar");
}