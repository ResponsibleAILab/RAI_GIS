var countries = [
    "Afghanistan", "Albania", "Algeria", "Andorra", "Angola",
    "Antigua and Barbuda", "Argentina", "Armenia", "Australia", "Austria",
    "Azerbaijan", "Bahamas", "Bahrain", "Bangladesh", "Barbados",
    "Belarus", "Belgium", "Belize", "Benin", "Bhutan",
    "Bolivia", "Bosnia and Herzegovina", "Botswana", "Brazil", "Brunei",
    "Bulgaria", "Burkina Faso", "Burundi", "Cabo Verde", "Cambodia",
    "Cameroon", "Canada", "Central African Republic", "Chad", "Chile",
    "China", "Colombia", "Comoros", "Congo (Brazzaville)", "Congo (Kinshasa)",
    "Costa Rica", "Croatia", "Cuba", "Cyprus", "Czech Republic",
    "Denmark", "Djibouti", "Dominica", "Dominican Republic", "East Timor",
    "Ecuador", "Egypt", "El Salvador", "Equatorial Guinea", "Eritrea",
    "Estonia", "Eswatini", "Ethiopia", "Fiji", "Finland",
    "France", "Gabon", "Gambia", "Georgia", "Germany",
    "Ghana", "Greece", "Grenada", "Guatemala", "Guinea",
    "Guinea-Bissau", "Guyana", "Haiti", "Honduras", "Hungary",
    "Iceland", "India", "Indonesia", "Iran", "Iraq",
    "Ireland", "Israel", "Italy", "Ivory Coast", "Jamaica",
    "Japan", "Jordan", "Kazakhstan", "Kenya", "Kiribati",
    "Kosovo", "Kuwait", "Kyrgyzstan", "Laos", "Latvia",
    "Lebanon", "Lesotho", "Liberia", "Libya", "Liechtenstein",
    "Lithuania", "Luxembourg", "Macedonia", "Madagascar", "Malawi",
    "Malaysia", "Maldives", "Mali", "Malta", "Marshall Islands",
    "Mauritania", "Mauritius", "Mexico", "Micronesia", "Moldova",
    "Monaco", "Mongolia", "Montenegro", "Morocco", "Mozambique",
    "Myanmar (Burma)", "Namibia", "Nauru", "Nepal", "Netherlands",
    "New Zealand", "Nicaragua", "Niger", "Nigeria", "North Korea",
    "Norway", "Oman", "Pakistan", "Palau", "Palestine",
    "Panama", "Papua New Guinea", "Paraguay", "Peru", "Philippines",
    "Poland", "Portugal", "Qatar", "Romania", "Russia",
    "Rwanda", "Saint Kitts and Nevis", "Saint Lucia", "Saint Vincent and the Grenadines", "Samoa",
    "San Marino", "Sao Tome and Principe", "Saudi Arabia", "Senegal", "Serbia",
    "Seychelles", "Sierra Leone", "Singapore", "Slovakia", "Slovenia",
    "Solomon Islands", "Somalia", "South Africa", "South Korea", "South Sudan",
    "Spain", "Sri Lanka", "Sudan", "Suriname", "Sweden",
    "Switzerland", "Syria", "Taiwan", "Tajikistan", "Tanzania",
    "Thailand", "Togo", "Tonga", "Trinidad and Tobago", "Tunisia",
    "Turkey", "Turkmenistan", "Tuvalu", "Uganda", "Ukraine",
    "United Arab Emirates", "United Kingdom", "United States", "Uruguay", "Uzbekistan",
    "Vanuatu", "Vatican City", "Venezuela", "Vietnam", "Yemen",
    "Zambia", "Zimbabwe"
];
var countryList = document.getElementById("countryList");
var countriesText = countries.join("\n");

/* To have a count of the textbox */
var input_textbox_count = 2;

var inputContainer = document.getElementById('Rai_inputContainer');
var input = document.createElement('input');
input.type = 'text';
input.placeholder = 'Enter text';
inputContainer.appendChild(input);

function rai_search_btn() {
    if (input_textbox_count == 5) {
        alert("Maximum fields reached");
    }
    var inputContainer = document.getElementById('Rai_inputContainer');
    input_textbox_count += 1;
    inputContainer.innerHTML = inputContainer.innerHTML + '\n                <input type="text" class="rai_search" id ="rai_search_' + input_textbox_count + '" ></input>'
}



function sendData() {
    // Read the whole Input fields
    var Loader = document.getElementById('loader');
    if (Loader) {
        Loader.style.display = "block";
    }
    var inputContainer = document.getElementById('Rai_inputContainer');
    var startData = document.getElementById('StartYearInput').value;
    var endData = document.getElementById('EndYearInput').value;

    // define the Regular expression
    var regex = /id="rai_search_(\d+)"/g;
    var matchedIDs = [];
    var trends = [];
    matchedIDs = inputContainer.innerHTML.match(regex);

    // Dynamic values are stored in a list
    for (var i = 1; i <= matchedIDs.length; i++) {
        var inputValue = document.getElementById('rai_search_' + i).value;
        if (inputValue.trim() !== '') {
            trends.push(inputValue);
        } else {
            break; // Exit the loop if the value is empty
        }
    }

    console.log(trends);

    fetch('/api/receive_data', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ trends: trends, startDate: startData, endDate: endData }),
    })
    .then(response => response.json())
    .then(data => {
        console.log(data.message);
    });
    Loader.style.display = "none";
}




// function sendData() {
//     // Read the whole Input fields
//     var inputContainer = document.getElementById('Rai_inputContainer');
//     var startData = document.getElementById('StartYearInput').value;
//     var endData = document.getElementById('EndYearInput').value;

//     // define the Regular expression
//     var regex = /id="rai_search_(\d+)"/g;
//     var matchedIDs = [];
//     var trends = {};
//     matchedIDs = inputContainer.innerHTML.match(regex);

//     // Dynamic values are stored
//     for (var i = 1; i <= matchedIDs.length; i++) {
//         var inputValue = document.getElementById('rai_search_' + i).value;
//         if (inputValue.trim() !== '') {
//             trends['Trend' + i] = inputValue;
//         } else {
//             break; // Exit the loop if the value is empty
//         }
//     }

//     // Include start year and end year in trends object
//     trends['StartYear'] = startData;
//     trends['EndYear'] = endData;

//     console.log(trends);

//     fetch('/api/receive_data', {
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//         },
//         body: JSON.stringify(trends),
//     })
//         .then(response => response.json())
//         .then(data => {
//             console.log(data.message);
//         });
// }

window.addEventListener('load', function () {
    console.log('Hi');
});
