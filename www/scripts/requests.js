const sleep = ms => new Promise(r => setTimeout(r, ms));

function requestAsText(method, path, body="", callback=null) {
    var request = new XMLHttpRequest()

    request.onreadystatechange = function() {
        if (request.readyState == XMLHttpRequest.DONE) {
            if (callback != null) callback(request)
        }
    }

    request.open(method, path, true)
    request.send(body)
}

function request(method, path, json, callback) {
    var request = new XMLHttpRequest()

    request.onreadystatechange = function() {
        if (request.readyState == XMLHttpRequest.DONE) {
            if (callback != null) callback(request)
        }
    }

    request.open(method, path, true)
    if (token != null) request.setRequestHeader("authorization", token)

    request.send(JSON.stringify(json))
}

function encodeUrlParams(string) { return string.replaceAll("&", "%26").replaceAll("=", "%3D").replaceAll("?", "%3F"); }