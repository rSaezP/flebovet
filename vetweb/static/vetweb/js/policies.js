// Agregar este script al final de tu HTML o en un archivo separado
document.addEventListener('DOMContentLoaded', function() {
    // Manejo de Tabs
    const tabButtons = document.querySelectorAll('.tab-btn');
    const tabContents = document.querySelectorAll('.tab-content');

    tabButtons.forEach(button => {
        button.addEventListener('click', () => {
            // Remover clase active de todos los botones
            tabButtons.forEach(btn => btn.classList.remove('active'));
            // Remover clase active de todos los contenidos
            tabContents.forEach(content => content.classList.remove('active'));
            
            // Agregar clase active al botón clickeado
            button.classList.add('active');
            // Mostrar el contenido correspondiente
            const tabId = button.getAttribute('data-tab');
            document.getElementById(tabId).classList.add('active');
        });
    });

    // Manejo del Acordeón
    const accordionButtons = document.querySelectorAll('.accordion-btn');

    accordionButtons.forEach(button => {
        button.addEventListener('click', () => {
            const accordionItem = button.parentElement;
            const isOpen = accordionItem.classList.contains('open');
            
            // Cerrar todos los items abiertos
            document.querySelectorAll('.accordion-item').forEach(item => {
                item.classList.remove('open');
                const content = item.querySelector('.accordion-content');
                content.style.maxHeight = null;
            });

            // Si el item clickeado no estaba abierto, abrirlo
            if (!isOpen) {
                accordionItem.classList.add('open');
                const content = accordionItem.querySelector('.accordion-content');
                content.style.maxHeight = content.scrollHeight + 'px';
            }

            // Rotar el icono
            const icon = button.querySelector('i');
            accordionButtons.forEach(btn => {
                btn.querySelector('i').style.transform = 'rotate(0deg)';
            });
            if (!isOpen) {
                icon.style.transform = 'rotate(180deg)';
            }
        });
    });
});