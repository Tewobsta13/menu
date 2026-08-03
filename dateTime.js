const dateTimeContainer = document.getElementById("date-time");

function updateDateTime() {
  let dateTimeObject = new Date();
  const date = dateTimeObject.toLocaleDateString();
  const time = dateTimeObject.toLocaleTimeString();
  const dateTime = `${date} ${time}`;
  dateTimeContainer.textContent = dateTime;
}

setInterval(() => {
  updateDateTime();
}, 1000);
