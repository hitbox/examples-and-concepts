"use strict";

function update_tabs(event) {
    const checkedTabInput = event.target;
    const tabGroup = checkedTabInput.name;

    // hide same group unchecked's tabs
    const s = `input[type=radio][name=${name=tabGroup}]:not(:checked)`;
    for (const tabInput of document.querySelectorAll(s)) {
        const tab = document.getElementById(tabInput.value);
        tab.classList.add("hidden");
    }

    // unhide checked's tab
    document.getElementById(checkedTabInput.value).classList.remove("hidden");

}

document.addEventListener("DOMContentLoaded", function(event) {

    for (const input_element of document.querySelectorAll("input[type=radio].tab")) {
        input_element.addEventListener("change", update_tabs);
    }

});
