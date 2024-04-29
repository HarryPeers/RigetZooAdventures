var components;
var loadedComponents = {};

window.addEventListener("load", () => onLoad(), false )

async function onLoad() {
    components = document.getElementsByClassName("component");

    Array.from(components).forEach(async (element) => {
        let componentName = element.innerText.split(".")[0];
        let innerText = element.innerText

        if (componentName.length == 0) return;

        if (!Object.keys(loadedComponents).includes(componentName)) loadedComponents[componentName] = requestAsText("GET", `/components/${componentName}.html`, "", (x) => {cacheComponentResult(componentName, x); loadComponentToDOM(element, componentName)});
        else loadComponentToDOM(element, componentName);

        await loadJavascript(innerText)
    });

}

async function loadJavascript(elementInnerText) {
    await sleep(10)

    requestAsText("GET", `/scripts/components/${elementInnerText}`, "", (x) => {
        if (x.status == 200) eval(x.responseText);
    });
}

function cacheComponentResult(componentName, response) {
    if (response.status == 200) loadedComponents[componentName] = response.responseText;
}

function loadComponentToDOM(element, componentName) {
    if (Object.keys(loadedComponents).includes(componentName)) element.innerHTML = loadedComponents[componentName];
}
