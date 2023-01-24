console.log("JS loaded")

// mobileBurgerMenu
const mobileBurgerMenu = document.querySelector('.mobile-burger-menu');
const navLink = document.querySelector('.nav-links');

mobileBurgerMenu.addEventListener('click', () => {
  navLink.classList.toggle('hidden');
});