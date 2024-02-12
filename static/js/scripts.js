// scripts.js

var overlay_sidebar = document.getElementById('overlay-sidebar');
overlay_sidebar.onclick = closePopupMenu;

function openPopupMenu() {
    var popupMenu = document.getElementById("popup-menu-wrapper");
    overlay_sidebar.style.display = 'block';
    popupMenu.style.display = "block";
}

function closePopupMenu() {
    var popupMenu = document.getElementById("popup-menu-wrapper");
    overlay_sidebar.style.display = 'none';
    popupMenu.style.display = "none";
}

// Function to make a GET request to fetch colors from the server
async function fetchColors() {
    try {
        const response = await fetch('/colors_url/');
        if (!response.ok) {
            throw new Error('Failed to fetch colors');
        }

        const colors = await response.json();
        return colors;
    } catch (error) {
        console.error('Error fetching colors:', error);
        return null;
    }
}

// Function to update CSS variables based on the colors fetched from the server
async function updateColors() {
    // Fetch colors from the server
    const colors = await fetchColors();

    // If colors are fetched successfully, update CSS variables
    if (colors) {
        for (var key in colors) {
            if (colors.hasOwnProperty(key)) {
                var cssVariableName = '--color-' + key;
                var cssVariableValue = '#' + cleanColorValue(colors[key]);
                setCSSVariableValue(cssVariableName, cssVariableValue);
            }
        }
    }
}

function cleanColorValue(colorValue) {
    // Remove any leading '#' and return a clean color value
    return colorValue.replace(/^#/, '');
}

// Function to get the value of a CSS variable
function getCSSVariableValue(variableName) {
    return getComputedStyle(document.documentElement).getPropertyValue(variableName).trim();
}

// Function to set the value of a CSS variable
function setCSSVariableValue(variableName, variableValue) {
    document.documentElement.style.setProperty(variableName, variableValue);
}

// Call the updateColors function when the page loads
document.addEventListener('DOMContentLoaded', updateColors);

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

// Get the topmost div element
const topArea = document.getElementById('main-website-top-area');

// Store the last scroll position
let lastScrollPosition = window.scrollY || document.documentElement.scrollTop;

// Function to handle the scroll event
function handleScroll() {
    const currentScrollPosition = window.scrollY || document.documentElement.scrollTop;

    if (currentScrollPosition < lastScrollPosition) {
        // Scrolling up
        topArea.className = 'main-website-top-area headroom headroom--not-bottom headroom--pinned headroom--top';
    } else {
        // Scrolling down
        topArea.className = 'main-website-top-area headroom headroom--not-bottom headroom--not-top headroom--unpinned';
    }

    // Update the last scroll position
    lastScrollPosition = currentScrollPosition;

    // Reset the flag after handling the scroll
    isScrollByGoToSection = false;
}

// Add scroll event listener
window.addEventListener('scroll', handleScroll);
