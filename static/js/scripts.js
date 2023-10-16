// scripts.js

// Toggle Sidebar Functionality
// const sidebarToggle = document.getElementById('sidebar-toggle');
// const sidebar = document.getElementById('sidebar');

// sidebarToggle.addEventListener('click', () => {
//     sidebar.classList.toggle('active');
// });

// Toggle Dropdown Functionality
const dropdownToggle = document.querySelectorAll('.dropdown-toggle');

dropdownToggle.forEach((toggle) => {
    toggle.addEventListener('click', () => {
        const dropdownMenu = toggle.nextElementSibling;
        dropdownMenu.classList.toggle('show');
    });
});

window.addEventListener("load", function() {
    closePopupMenu();
});

function openPopupMenu() {
    var popupMenu = document.getElementById("popup-menu-wrapper");
    popupMenu.style.display = "flex";
}

function closePopupMenu() {
    var popupMenu = document.getElementById("popup-menu-wrapper");
    popupMenu.style.display = "none";
}


// Get the button element
var nachObenButton = document.getElementById('nach-oben-bt');

// Add a click event listener to the button
nachObenButton.addEventListener('click', function() {
    // Scroll to the top of the page smoothly
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
});

var lastScrollTop = 0;
var mainWebsiteTopArea = document.getElementById('main-website-top-area');

window.addEventListener('scroll', function() {
    var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
    if (scrollTop > lastScrollTop) {
        // Scrolling down
        mainWebsiteTopArea.classList.remove('headroom--pinned');
    } else {
        // Scrolling up
        mainWebsiteTopArea.classList.add('headroom--pinned');
    }
    
    lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
});

// Add more functionality as needed
