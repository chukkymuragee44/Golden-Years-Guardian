const url = "http://localhost:5000";

function connectToServer(route, callbackResponse) {
  fetch(`${url}/${route}`, {
    method: "GET",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
  })
    .then((res) => res.json())
    .then((res) => callbackResponse(res));
}

function connectAndSendDataToServer(route, content, callbackResponse) {
  fetch(`${url}/${route}`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/json",
    },
    body: JSON.stringify(content),
  })
    .then((res) => res.json())
    .then((res) => callbackResponse(res));
}
