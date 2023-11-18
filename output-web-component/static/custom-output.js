"use strict";

class CustomOutput extends HTMLOutputElement {
    static get observedAttributes() {
        return ["for"];
    }

    constructor() {
        self = super();
        self.event_name = "change";
    }

    connectedCallback() {
    }

    attributeChangedCallback(name, oldValue, newValue) {
        if (name === "for") {
            const re = /\ +/
            const a = new Set(oldValue ? oldValue.split(re) : []);
            const b = new Set(newValue ? newValue.split(re) : []);
            // removed event listeners
            for (const a_id of a) {
                if (b.has(a_id))
                    continue
                let element = document.getElementById(a_id);
                element.removeEventListener(self.event_name, self.updateValue);
            }
            // new event listeners
            for (const b_id of b) {
                if (a.has(b_id))
                    continue
                let element = document.getElementById(b_id);
                element.addEventListener(self.event_name, self.updateValue);
            }
        }
    }

    updateValue() {
        const elements = [];
        for (const id of self.htmlFor) {
            let element = document.getElementById(id);
            elements.push(element);
        }
        const func = window[self.dataset.func];
        self.value = func(elements);
    }

}

customElements.define("custom-output", CustomOutput, {extends: "output"});
