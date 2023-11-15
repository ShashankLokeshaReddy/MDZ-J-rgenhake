// scripts.js

// Toggle Sidebar Functionality
// const sidebarToggle = document.getElementById('sidebar-toggle');
// const sidebar = document.getElementById('sidebar');

// sidebarToggle.addEventListener('click', () => {
//     sidebar.classList.toggle('active');
// });

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

// var lastScrollTop = 0;

// var mainWebsiteTopArea = document.getElementById('main-website-top-area');

// window.addEventListener('scroll', function() {
//     var scrollTop = window.pageYOffset || document.documentElement.scrollTop;
    
//     if (scrollTop > lastScrollTop) {
//         // Scrolling down
//         mainWebsiteTopArea.classList.remove('headroom--pinned');
//     } else {
//         // Scrolling up
//         mainWebsiteTopArea.classList.add('headroom--pinned');
//     }
    
//     lastScrollTop = scrollTop <= 0 ? 0 : scrollTop;
// });

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

    masseSelected = true;
    updateProgressBar();
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

function openProfile(){

}

function openCart(){

}

// function getSelectedOption(category) {
//     var selectedOption = ''; // Replace with logic to get the selected option
//     return selectedOption;
// }

// Select the first cable variante by default
// selectKabelvariante(document.querySelector('.kabelvariante-selector:first-child label').textContent.trim());
updateProgressBar();

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
