"use strict";

function update_tab_arg(value) {
    const url = new URL(document.URL)
    url.searchParams.set("tab", value)
    history.pushState({}, document.title, url);
}

function update_tabs(event) {
    const checkedTabInput = event.target;
    const tabGroup = checkedTabInput.name;

    // hide and deactivate same group unchecked's tabs
    const s = `input[type=radio][name=${name=tabGroup}].tab:not(:checked)`;
    for (const tabInput of document.querySelectorAll(s)) {
        const tab = document.getElementById(tabInput.value);
        tab.classList.add("hidden");
        for (const label of tabInput.labels) {
            label.classList.remove("current");
        }
    }

    // show checked's tab
    const tab = document.getElementById(checkedTabInput.value)
    tab.classList.remove("hidden");

    // make checked tab's label "current"
    for (const label of checkedTabInput.labels) {
        label.classList.add("current");
    }

    update_tab_arg(checkedTabInput.value);
}

document.addEventListener("DOMContentLoaded", function(event) {
    for (const input_element of document.querySelectorAll("input[type=radio].tab")) {
        input_element.addEventListener("change", update_tabs);
    }
});
