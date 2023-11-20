"use strict";

class DropzoneElement extends HTMLElement {

    connectedCallback() {
        self = super();

        // allow receiving drop events
        self.addEventListener("dragover", function(event) {
            event.preventDefault();
        });

        // add class for dragenter
        self.addEventListener("dragenter", function(event) {
        });
    }

    attributeChangedCallback(name, oldValue, newValue) {
    }

    updateValue() {
    }

    // validate drop with attribute matching. original uses type.

    is_valid_drop(dragging) {
        console.log(dragging);
    }

}

customElements.define("dropzone-element", DropzoneElement);
