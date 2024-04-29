const highlightedItemImage = document.getElementById("highlighted-grid-item-image");
const highlightedItemName = document.getElementById("highlighted-grid-item-name");
const highlightedItemDescription = document.getElementById("highlighted-grid-item-description");
const highlightedItemList = document.getElementById("highlighted-grid-item-list");

function populateGrid(id, set) {
    var currentRow;
    var iteration = 0;
    var grid = document.getElementById(id);

    Object.keys(set).forEach((name) => {
        if (iteration % 2 == 0) {
            if (currentRow != null) grid.appendChild(currentRow);

            currentRow = document.createElement("div");
            currentRow.className = "animal-cards fifty-fifty";
        }

        item = set[name];

        let card = document.createElement("div");
        card.className = "high-contrast-background";

        
        let imageElement = document.createElement("img");
        imageElement.src = item.image;

        card.appendChild(imageElement);

        let cardInner = document.createElement("div");

        let header = document.createElement("h");
        header.innerText = name;
        
        let subheader = document.createElement("h2");
        subheader.innerText = item.type

        cardInner.appendChild(header);
        cardInner.appendChild(subheader);

        card.appendChild(cardInner);

        currentRow.appendChild(card);

        card.addEventListener("click", () => { expandCard(name, set) } );

        iteration += 1;
    })

    if (currentRow != null && currentRow.childElementCount > 0) grid.appendChild(currentRow);

    expandCard(Object.keys(set)[Math.floor(Math.random() * Object.keys(set).length)], set)
}

function expandCard(name, set) {
    item = set[name]

    highlightedItemName.innerText = name;
    highlightedItemDescription.innerText = item.description;
    highlightedItemImage.src = item.image;
    
    highlightedItemList.innerHTML = "";

    Object.keys(item.details).forEach((header) => {
        content = item.details[header]
        
        let row = document.createElement("div");
        row.className = "row";

        let headerEle = document.createElement("div");
        headerEle.className = "row-header";
        headerEle.innerText = header.replace(header[0], header[0].toUpperCase());

        let contentEle = document.createElement("div");
        contentEle.className = "row-content";
        contentEle.innerText = content;

        row.appendChild(headerEle);
        row.appendChild(contentEle);

        highlightedItemList.appendChild(row);

        if (Object.keys(item.details)[Object.keys(item.details).length-1] == header) row.style.borderBottom = "none";
    })


}