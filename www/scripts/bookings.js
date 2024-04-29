const bookingsList = document.getElementById("pending-bookings-list")

const loyaltyPoints = document.getElementById("loyalty-points");
const loyaltyPointsPounds = document.getElementById("loyalty-points-pounds");


const types = {
    "Snow": {
        "type": "Limited Spaces",
        "description": "",
        "details": {
            "sleeps": "6",
            "amenities": "Wifi, Hot tub, Kitchen",
            "cost/night": "Enquire for details",
            "Max stay": "24",
            "Min stay": "2",
            "Available": 5
        },
        "image": "images/accomodation/snow.png"
    },
    "Woodland": {
        "type": "",
        "description": "",
        "details": {
            "sleeps": "12",
            "amenities": "Wifi, Kitchen, Hammock sleeping",
            "cost/night": "Enquire for details",
            "Max stay": "24",
            "Min stay": "2",
            "Available": 24
        },
        "image": "images/accomodation/woodland.png"
    },
    "Aquarium": {
        "type": "Limited Spaces",
        "description": "",
        "details": {
            "sleeps": "4",
            "amenities": "Wifi, kitchen",
            "cost/night": "Enquire for details",
            "Max stay": "12",
            "Min stay": "2",
            "Available": 9
        },
        "image": "images/accomodation/aquarium.png"
    },
    "Camping": {
        "type": "",
        "description": "",
        "details": {
            "pitch size": "large",
            "amenities": "Electric plugin, showers",
            "cost/night": "Enquire for details",
            "Max stay": "12",
            "Min stay": "2",
            "Available": 120
        },
        "image": "images/accomodation/camping.png"
    },
    "Eco-pod": {
        "type": "Limited Spaces",
        "description": "",
        "details": {
            "sleeps": "2",
            "amenities": "Completely eco-friendly",
            "cost/night": "Enquire for details",
            "Max stay": "24",
            "Min stay": "3",
            "Available": 9
        },
        "image": "images/accomodation/eco-pod.png"
    },
    "Treehouse": {
        "type": "Limited Spaces",
        "description": "",
        "details": {
            "sleeps": "8",
            "amenities": "Kitchen, WiFi",
            "cost/night": "Enquire for details",
            "Max stay": "12",
            "Min stay": "4",
            "Available": 12
        },
        "image": "images/accomodation/treehouse.png"
    },
    "Campervan": {
        "type": "",
        "description": "",
        "details": {
            "Max height": "14 foot",
            "Max width": "9 foot",
            "amenities": "Electric plug in, shower blocks",
            "cost/night": "Enquire for details",
            "Max stay": "2",
            "Min stay": "31",
            "Available": 60
        },
        "image": "images/accomodation/campervan.png"
    },
    "Standard": {
        "type": "",
        "description": "",
        "details": {
            "sleeps": "4",
            "amenities": "Kitchen, WiFi",
            "cost/night": "Enquire for details",
            "Max stay": "3",
            "Min stay": "31",
            "Available": 32
        },
        "image": "images/accomodation/standard.png"
    },
    "Safari Adventure": {
        "type": "",
        "description": "",
        "details": {
            
        },
        "image": "images/safari.jpg"
    }
    
}


const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const today = new Date();

function getPrefix(date) {
    date = date.toString()

    if (date.length == 2 && date[0] == "1") return "th"

    switch (date[date.length-1]) {
        case ("1"):
            return "st"
        case ("2"):
            return "nd"
        case ("3"):
            return "rd"
        default:
            return "th"
    }
}

function getDateString(date, showYear) {
    let x = `${date.getDate()}${getPrefix(date.getDate())} ${months[date.getMonth()]}`

    if (showYear) x += ` ${date.getFullYear()}`

    return x;
}

window.addEventListener("load", () => {
    let path = window.location.pathname
    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);

    switch (path) {
        case ("/zooBookingsCreate"):
            if (token == null) window.location.replace(`/login?callback=/zooBookingsCreate${encodeUrlParams(queryString)}`) 
            else {
                request("POST", `/api/bookings/zoo/create${queryString}`, null, (x) => {
                    if (x.status == 401) window.location.replace(`/login?callback=/zooBookingsCreate${encodeUrlParams(queryString)}`)
                    else window.location.replace("/dashboard#bookings")
                })
            }
            break;
        case ("/accomodationBookingsCreate"): 
            if (token == null) window.location.replace(`/login?callback=/accomodationBookingsCreate${encodeUrlParams(queryString)}`) 
            else {
                request("POST", `/api/bookings/accomodation/create${queryString}`, null, (x) => {
                    if (x.status == 401) window.location.replace(`/login?callback=/accomodationBookingsCreate${encodeUrlParams(queryString)}`)
                    else window.location.replace("/dashboard#bookings")
                })
            }
            break;
        case ("/dashboard"):
            request("GET", `/api/bookings/`, null, (x) => {
                if (x.status == 401) window.location.replace(`/login?callback=/dashboard`)

                let iteration = 0;
                let response = JSON.parse(x.responseText);
                let currentRow = null;
                
                loyaltyPoints.innerText = response.length * 1500

                loyaltyPointsPounds.innerText = response.length * 3

                response.forEach((x) => {
                    if (iteration % 2 == 0) {
                        if (currentRow != null) bookingsList.appendChild(currentRow);

                        currentRow = document.createElement("div");
                        currentRow.className = "animal-cards fifty-fifty";
                    }

                    let card = document.createElement("div");
                    card.className = "high-contrast-background";

                    if (Object.keys(types).includes(x.type)) {
                        let image = document.createElement("img");
                        image.src = types[x.type].image

                        card.appendChild(image);
                    }

                    let cardInner = document.createElement("div");

                    let header = document.createElement("h");
                    header.innerText = x.type;
                    
                    let subheader = document.createElement("h2");
                    let startDate = new Date(x.time.start)

                    if (x.type.toString().toLowerCase() == "safari adventure") {
                        subheader.innerText = getDateString(startDate, startDate.getFullYear() != today.getFullYear())
                    } else {
                        let endDate = new Date(x.time.end)

                        subheader.innerText = `${getDateString(startDate, startDate.getFullYear() != today.getFullYear())} - ${getDateString(endDate, endDate.getFullYear() != today.getFullYear())}`
                    }

                    cardInner.appendChild(header);
                    cardInner.appendChild(subheader);

                    card.appendChild(cardInner);

                    currentRow.appendChild(card);

                    iteration += 1

                    card.addEventListener("click", () => expandCard(x.type, types));
                    expandCard(x.type, types)
                })

                if (currentRow != null && currentRow.childElementCount > 0) bookingsList.appendChild(currentRow);

            });
            break;
    }

})
