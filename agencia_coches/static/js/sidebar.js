// Script para alternar el sidebar en móviles
const btnToggle = document.getElementById('sidebarCollapse');
const btnClose = document.getElementById('closeSidebar');
const sidebar = document.getElementById('sidebar');

btnToggle.addEventListener('click', () => sidebar.classList.toggle('active'));
btnClose.addEventListener('click', () => sidebar.classList.remove('active'));