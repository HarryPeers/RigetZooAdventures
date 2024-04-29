var accesibilityOptions = {
    "contrastMode": false,
    "fontSize": false
}

function toggleAccesibilityOption(option) {
    let ele = document.getElementById(option)
    let optionParsed = option.split("-")[0]

    accesibilityOptions[optionParsed] = !accesibilityOptions[optionParsed] 
    ele.checked = accesibilityOptions[optionParsed] 
}

function changeAccesibility(option) {
    let ele = document.getElementById(option)
    let optionParsed = option.split("-")[0]
    accesibilityOptions[optionParsed] = ele.checked;

    updateContrast()
}

function openDropdown(event) {
    let content = event.target.parentElement.getElementsByClassName("dropdown-content")[0];
    content.style.display = "block";
}

function closeDropdown(event) {
    let content = event.target.getElementsByClassName("dropdown-content")[0];
    content.style.display = "none";
}

function updateContrast() {
    var backgroundColor, background;

    if (accesibilityOptions.contrastMode) backgroundColor = "white";
    else backgroundColor = "";



    Array.from(document.getElementsByClassName("high-contrast-background")).forEach((el) => {
        el.style.background = backgroundColor;
    })
}
