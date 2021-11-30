var i = 1;

function addNewFields() {
    var newFields = document.createElement("div");
    newFields.innerHTML = '<label for="date">Start Date: </label>' + ' ' +
                          '<input type="date" name="startDate">' + ' ' +
                          '<label for="endDate">End Date: </label>' + ' ' +
                          '<input type="date" name="endDate">' + ' ' +
                          '<label for="pricing">Price for this date range: </label>' + ' ' +
                          '<input type="number" name = "pricing">' + ' '; 

    document.getElementById("pricingform").appendChild(newFields);
}