// scripts.js

// Toggle Sidebar Functionality
// const sidebarToggle = document.getElementById('sidebar-toggle');
// const sidebar = document.getElementById('sidebar');

// sidebarToggle.addEventListener('click', () => {
//     sidebar.classList.toggle('active');
// });

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

var akkuSelected = false;
var kabelSelected = false;
var schnittstellenSelected = false;
var masseSelected = false;
var selected_akkuvariante_name = "";
var selected_kabel_name = "";
var selected_schnittstellen_name = "";
var selected_masse_name = "";

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

function selectAkkuvariante(productName) {
    console.log('Selected Akkuvariante:', productName);

    var productSelectors = document.querySelectorAll('.akkuvariante-selector');

    productSelectors.forEach(function(selector) {
        selector.classList.remove('selected');
        var label = selector.querySelector('label');
        if (label.textContent.trim() === productName) {
            selector.classList.add('selected');
        }
    });

    akkuSelected = true;
    selected_akkuvariante_name = productName;
    updateProgressBar();
}

function selectKabelvariante(productName) {
    var productSelectors = document.querySelectorAll('.kabelvariante-selector');

    productSelectors.forEach(function(selector) {
        selector.classList.remove('selected');
        var label = selector.querySelector('label');
        if (label.textContent.trim() === productName) {
            selector.classList.add('selected');
        }
    });

    masse(productName);
    schnittstelle(productName);
    kabelSelected = true;
    schnittstellenSelected = false;
    removeAllSelectedSchnittstellen()
    masseSelected = false;
    updateProgressBar();
}

function masse(productName){
    console.log('Selected Kabelvariante in masse:', productName);

    // Hide all sliders initially
    var sliders = document.querySelectorAll('.masse-slider-container-class');
    sliders.forEach(function(slider) {
        slider.classList.add('hidden');
    });

    // Show the selected slider based on cable type
    var selectedSliderId = productName.toLowerCase() + '-messe-slider';
    var selectedSlider = document.getElementById(selectedSliderId);
    if (selectedSlider) {
        selectedSlider.classList.remove('hidden');
    } else {
        console.log('No matching slider found for:', productName);
    }
}

function schnittstelle(productName){
    console.log('Selected Kabelvariante in Schnittstellen:', productName);
    selected_kabel_name = productName;

    // Hide all sliders initially
    var sliders = document.querySelectorAll('.schnittstelle-slider-container-class');
    sliders.forEach(function(slider) {
        slider.classList.add('hidden');
    });

    // Show the selected slider based on cable type
    var selectedSliderId = productName.toLowerCase() + '-schnittstelle-slider';
    var selectedSlider = document.getElementById(selectedSliderId);
    if (selectedSlider) {
        selectedSlider.classList.remove('hidden');
    } else {
        console.log('No matching slider found for:', productName);
    }

}

function selectschnittstellenvariante(productName, splitIndex) {
    console.log('Selected schnittstelle:', productName, splitIndex);

    var productSelectors = document.querySelectorAll('.schnittstelle-selector');

    productSelectors.forEach(function(selector) {
        if (splitIndex === 'S'){
            var label = selector.querySelector('label');
            var selectorSplitIndex = selector.getAttribute('data-split-index');
            if (label.textContent.trim() === productName && selectorSplitIndex === splitIndex) {
                selector.classList.add('selected');
            }
            if (label.textContent.trim() !== productName && selectorSplitIndex === splitIndex) {
                selector.classList.remove('selected');
            }
        }
        else{
            for (var i = 0; i <= splitIndex; i++) {
                var label = selector.querySelector('label');
                var selectorSplitIndex = selector.getAttribute('data-split-index');
                if (label.textContent.trim() === productName && selectorSplitIndex === splitIndex) {
                    selector.classList.add('selected');
                }
                if (label.textContent.trim() !== productName && selectorSplitIndex === splitIndex) {
                    selector.classList.remove('selected');
                }
            }
        }
    });

    schnittstellenSelected = true;
    updateProgressBar();
}

function removeAllSelectedSchnittstellen() {
    var selectors = document.querySelectorAll('.schnittstelle-selector');
    selectors.forEach(function (selector) {
        selector.classList.remove('selected');
    });
}

function updateProgressBar() {
    // Update the stepper based on selected sections
    var stepperItems = document.querySelectorAll('.stepper-item');

    stepperItems[0].classList.toggle('completed', akkuSelected);
    stepperItems[1].classList.toggle('completed', kabelSelected);
    stepperItems[2].classList.toggle('completed', schnittstellenSelected);
    stepperItems[3].classList.toggle('completed', masseSelected);
}

function updateSummary() {
    var akkuvariante = selected_akkuvariante_name;
    var kabelvariante = selected_kabel_name;
    var schnittstelle = selected_schnittstellen_name;
    var masse = selected_masse_name;

    document.getElementById('akkuvariante-summary').innerText = 'Akkuvariante: ' + akkuvariante;
    document.getElementById('kabelvariante-summary').innerText = 'Kabelvariante: ' + kabelvariante;
    document.getElementById('schnittstelle-summary').innerText = 'Schnittstelle: ' + schnittstelle;
    document.getElementById('masse-summary').innerText = 'Maße: ' + masse;
}

function masseChange(value) {
    masseSelected = true;
    updateProgressBar();
    console.log("Main Length changed to: " + value);
}

function openProfile(){

}

function openCart(){

}

// Function to handle the scroll for goToSection
function goToSection(selectedSectionId) {
    var sections = [
        'Akkuvariante-Section',
        'Kabelvariante-Section',
        'Schnittstellen-Section',
        'Masse-Section',
        'Zusammenfassung-Section'
    ];

    for (var i = 0; i < sections.length; i++) {
        var sectionId = sections[i];
        var section = document.getElementById(sectionId);
        var stepperItem = document.querySelector('.stepper-item[data-counter="' + (i + 1) + '"]');

        if (section) {
            if (i === 0) {
                // For the first section (Akkuvariante-Section), scroll to the top of the page
                if (i <= sections.indexOf(selectedSectionId)) {
                    section.classList.remove('hidden');
                    
                    if (stepperItem) {
                        stepperItem.classList.add('active');
                    }

                    // Auto-scroll to the top of the page
                    window.scrollTo({
                        top: 0,
                        behavior: 'smooth'
                    });
                } else {
                    section.classList.add('hidden');
                    if (stepperItem && stepperItem.classList.contains('active')) {
                        stepperItem.classList.remove('active');
                    }
                }
            } else {
                // For the rest of the sections, apply target position logic
                if (i <= sections.indexOf(selectedSectionId)) {
                    section.classList.remove('hidden');

                    if (stepperItem) {
                        stepperItem.classList.add('active');
                    }

                    // Calculate the target position as 30% of the screen height
                    var targetPosition = section.offsetTop;

                    // Set the flag to indicate that scroll is triggered by goToSection
                    isScrollByGoToSection = true;

                    // Auto-scroll to the target position
                    window.scrollTo({
                        top: targetPosition,
                        behavior: 'smooth'
                    });
                } else {
                    section.classList.add('hidden');
                    if (stepperItem && stepperItem.classList.contains('active')) {
                        stepperItem.classList.remove('active');
                    }
                }
            }
        } else {
            console.error("Element with ID '" + sectionId + "' not found.");
        }
    }

    console.log("Going to the section: " + selectedSectionId);
}

function addToCart() {
    // Add logic to navigate to the next section
    // You can use JavaScript or any client-side framework/library for this
    console.log("Adding to cart");
}

// function getSelectedOption(category) {
//     var selectedOption = ''; // Replace with logic to get the selected option
//     return selectedOption;
// }

// Select the first cable variante by default
// selectKabelvariante(document.querySelector('.kabelvariante-selector:first-child label').textContent.trim());
updateProgressBar();
// goToSection('Akkuvariante-Section')

// Event listeners for slider values (you can modify these according to your requirements)
// document.getElementById('straight-length').addEventListener('input', function() {
//     console.log('Straight Cable Length:', this.value);
// });

// document.getElementById('main-length').addEventListener('input', function() {
//     console.log('Main Cable Length:', this.value);
// });

// document.getElementById('branch1-length').addEventListener('input', function() {
//     console.log('Branch 1 Length:', this.value);
// });

// document.getElementById('branch2-length').addEventListener('input', function() {
//     console.log('Branch 2 Length:', this.value);
// });

// // Add more functionality as needed
