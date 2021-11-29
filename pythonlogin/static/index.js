var i = 1;
function addNewFields() {
   
    let sdLabel = document.createElement("label");
    sdLabel.setAttribute("for", "startDate" + i);
    sdLabel.appendChild(document.createTextNode("Enter a start date here: "));
    document.getElementById("pricingform").appendChild(sdLabel);

    let startDate = document.createElement("INPUT");
    startDate.setAttribute("type", "date");
    startDate.setAttribute("name", "startDate" + i);
    document.getElementById("pricingform").appendChild(startDate);

    let edLabel = document.createElement("label");
    edLabel.setAttribute("for", "endDate" + i);
    edLabel.appendChild(document.createTextNode("Enter an end date here: "));
    document.getElementById("pricingform").appendChild(edLabel);

    let endDate = document.createElement("INPUT");
    endDate.setAttribute("type", "date");
    endDate.setAttribute("name", "endDate" + i);
    document.getElementById("pricingform").appendChild(endDate);

    let pricingLabel = document.createElement("label");
    pricingLabel.setAttribute("for", "pricing" + i);
    pricingLabel.appendChild(document.createTextNode("Enter the price here:        "));
    document.getElementById("pricingform").appendChild(pricingLabel);

    let pricing = document.createElement("INPUT");
    pricing.setAttribute("type", "number");
    pricing.setAttribute("name", "pricing" + i);
    document.getElementById("pricingform").appendChild(pricing);
    
    i++;
}