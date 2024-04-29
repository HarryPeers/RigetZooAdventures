const months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
const days = ["Mon.", "Tue.", "Wed.", "Thu.", "Fri.", "Sat.", "Sun."]

const calanders = document.getElementsByClassName("calander-card");
var calanderValues = {};
var today = new Date();

function registerCalander(element, singlePicker, callback) {
    calanderValues[element] = {start: null, end: null, picker: 1, month: today.getMonth(), year: today.getFullYear(), element: element, singlePicker:singlePicker}
    element.getElementsByClassName("calander-booking-button")[0].addEventListener("click", () => { callback(element) });

    fillCalander(element);
}

function fillCalander(element, skipPickers) {
    let datesInOrder = [];
    let selectedCalander = calanderValues[element]

    
    element.getElementsByClassName("calander-dates")[0].innerHTML = "";

    let datePointer = new Date(selectedCalander.year, selectedCalander.month, 1)

    while (datePointer.getMonth() == selectedCalander.month) {
        datesInOrder.push(new Date(selectedCalander.year, selectedCalander.month, datePointer.getDate()))
        datePointer.setDate(datePointer.getDate() + 1);
    }

    let firstRow = document.createElement("div");

    days.forEach((dayOfWeek) => {
        let ele = document.createElement("div");
        ele.innerText = dayOfWeek;

        firstRow.appendChild(ele)
    })

    element.getElementsByClassName("calander-dates")[0].appendChild(firstRow)

    let rows = []
    rows.push(document.createElement("div"))

    for (let i = 0; i < datesInOrder[0].getDay()-1; i++) {
        let date = document.createElement("div");
        rows[rows.length-1].appendChild(date)
    }

    let datesToElement = {}

    datesInOrder.forEach((date) => {
        if (rows[rows.length-1].children.length >= 7) {      
            element.getElementsByClassName("calander-dates")[0].appendChild(rows[rows.length-1])

            rows.push(document.createElement("div"))
        }

        let dateElement = document.createElement("div");
        dateElement.innerText = date.getDate();

        if (today > date) dateElement.className += "expired-date"

        dateElement.addEventListener("click", () => dateOnClick(element, datesToElement, date.getDate()));
        dateElement.addEventListener("mouseover", () => highlightDates(element, datesToElement, date.getDate()));

        datesToElement[date.getDate()] = dateElement;

        rows[rows.length-1].appendChild(dateElement)
    })

    element.getElementsByClassName("calander-dates")[0].appendChild(rows[rows.length-1]);


    if (skipPickers) return;

    let yearPicker = element.getElementsByTagName("select")[1];
    let monthPicker = element.getElementsByTagName("select")[0];



    monthPicker.addEventListener("change", () => {
        let index = months.findIndex((x) => x == monthPicker.value)

        selectedCalander.month = index;

        fillCalander(selectedCalander.element, true);
    })

    yearPicker.addEventListener("change", () => {
        selectedCalander.year = yearPicker.value;
        fillCalander(selectedCalander.element, true);
    })

    for(let i = selectedCalander.year; i < selectedCalander.year + 10; i++) {
        let element = document.createElement("option");
        element.innerText = i;

        if (i == selectedCalander.year) element.selected = true;

        yearPicker.appendChild(element)
    }

    months.forEach((m) => {
        let element = document.createElement("option");
        element.innerText = m;

        if (months.findIndex((x) => x == m) == selectedCalander.month) element.selected = true;

        monthPicker.appendChild(element)
    })
}

function dateOnClick(calander, datesToElement, date) {
    let selectedCalander = calanderValues[calander];

    if (new Date(selectedCalander.year, selectedCalander.month, date) < today) return;

    if (selectedCalander.singlePicker) {
        selectedCalander.start = date
        selectedCalander.end = date
    } else {
        if (selectedCalander.start != null && selectedCalander.end != null && selectedCalander.start < date < selectedCalander.end) {
            let distanceFromStart = date - selectedCalander.start;
            let distanceFromEnd = selectedCalander.end - date;
    
            if (distanceFromStart < distanceFromEnd) selectedCalander.start = date;
            else selectedCalander.end = date;
    
        } else {
            if (selectedCalander.start == null || date < selectedCalander.end) selectedCalander.start = date;
            else if (selectedCalander.end == null || date > selectedCalander.end) selectedCalander.end = date;     
        }
    }

    highlightDates(calander, datesToElement, date, true)
}

function highlightDates(calander, datesToElement, date, bypass=false) {

    let selectedCalander = calanderValues[calander];

    if (new Date(selectedCalander.year, selectedCalander.month, date) < today) return;


    let mimmickStart = selectedCalander.start;
    let mimmickEnd = selectedCalander.end;

    if (date < mimmickStart) {
        mimmickEnd = mimmickStart
        mimmickStart = null;
    }

    if (!bypass && selectedCalander.start != null && selectedCalander.end != null) return; 

    Object.values(datesToElement).forEach((el) => {
        if (!el.className.includes("expired-date")) el.className = ""
    });

    if (mimmickStart == mimmickEnd || (mimmickStart == date && mimmickEnd == null)) {
        datesToElement[date].className = "calander-whole";
        return;
    }

    if (mimmickStart != null) datesToElement[mimmickStart].className = "calander-start";
    else if (mimmickEnd != null) datesToElement[date].className = "calander-start";

    if (mimmickEnd != null) datesToElement[mimmickEnd].className = "calander-end";
    else if (mimmickStart != null) datesToElement[date].className = "calander-end";

    if (mimmickStart == null && mimmickEnd == null) return;

    let range = [mimmickStart + 1, date]

    if (mimmickEnd != null) range = [mimmickStart + 1, mimmickEnd]
    else if (date < selectedCalander.start) range = [date+1, mimmickEnd]


    for (let i = range[0]; i < range[1]; i++) {

        datesToElement[i].className = "calander-during";
    }

}

function bookAccomodation(calander) {
    let selectedCalander = calanderValues[calander]

    let accomodationType = document.getElementById("accomodation-type").value;

    if (selectedCalander.start == null) return;
    else if (selectedCalander.end == null) return;


    var token = localStorage.getItem("token");
    var redirect = `/accomodationBookingsCreate?start=${(new Date(selectedCalander.year, selectedCalander.month, selectedCalander.start, null, null)).toISOString()}&end=${(new Date(selectedCalander.year, selectedCalander.month, selectedCalander.end)).toISOString()}&type=${accomodationType}`
    var redirectParsed = redirect.replaceAll("&", "%26").replaceAll("=", "%3D").replaceAll("?", "%3F");

    if (token != null) {
        window.location.replace(redirect);
    } else {
        window.location.replace(`/login/?callback=${redirectParsed}`);
    }

}

function bookSafari(calander) {
    let selectedCalander = calanderValues[calander]

    let startHour = calander.getElementsByTagName("select")[2].value;
    let startMinute = calander.getElementsByTagName("select")[3].value;
    let vehRegistration = document.getElementById("vehicle-registration").value;

    if (selectedCalander.start == null) return;
    else if (selectedCalander.end == null) return;
    else if (startHour == null) return;
    else if (startMinute == null) return;
    else if (vehRegistration == null) return;

    var token = localStorage.getItem("token");
    var redirect = `/zooBookingsCreate?start=${(new Date(selectedCalander.year, selectedCalander.month, selectedCalander.start, startHour, startMinute)).toISOString()}&end=${(new Date(selectedCalander.year, selectedCalander.month, selectedCalander.end)).toISOString()}&registration=${vehRegistration}`
    var redirectParsed = redirect.replaceAll("&", "%26").replaceAll("=", "%3D").replaceAll("?", "%3F");

    if (token != null) {
        window.location.replace(redirect);
    } else {
        window.location.replace(`/login/?callback=${redirectParsed}`);
    }
}