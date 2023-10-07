"use strict";

const DROPZONE_SELECTOR = '[data-dropzone="true"]';
const DRAGGABLE_SELECTOR = '[draggable="true"]';
const DROPZONE_DRAGGING_CLASS = "dragging";
const DROPZONE_DRAGOVER_CLASS = "dragover";

let dragging_element = null;

function move_element(element, target) {
    // appendChild moves element
    // a remove op is not needed
    // https://developer.mozilla.org/en-US/docs/Web/API/Node/appendChild
    target.appendChild(element);
}

function get_dropzones(root=document) {
    return root.querySelectorAll(DROPZONE_SELECTOR);
}

function get_draggables(root=document) {
    return root.querySelectorAll(DRAGGABLE_SELECTOR);
}

function get_draggable_data(element) {
    return JSON.parse(element.dataset.draggableData);
}

function is_dropzone(element) {
    // element is a place where draggables can be dropped
    return (
        "dropzone" in element.dataset
        && JSON.parse(element.dataset.dropzone)
        && "dropzoneType" in element.dataset
        && element.dataset.dropzoneType
    );
}

function is_draggable(element) {
    return JSON.parse(element.getAttribute("draggable"));
}

function is_list_collector(element) {
    return (
        "listName" in element.dataset
        && element.dataset.listName
    )
}

function get_dropzone_types(element) {
    // get array of strings of types permitted in dropzone
    return JSON.parse(element.dataset.dropzoneType);
}

function validate_dropzone(dropzone_element) {
    // init check required data attribute
    if (!("dropzoneType" in dropzone_element.dataset)) {
        // required data attribute is missing
        throw new Error(
            `${dropzone_element} dropzone element missing dropzone-type data attribute`
        );
    }

    // init check parsing data attribute
    const dropzone_types = get_dropzone_types(dropzone_element);
    if (dropzone_types.length === 0) {
        throw new Error(
            `${dropzone_element} failed parsing dropzone-type data attribute`
        );
    }
}

function init_dropzone(dropzone_element) {
    // initialize dropzone

    // preventDefault to enable receiving drop events
    dropzone_element.addEventListener("dragover", function(event) {
        event.preventDefault();
    });

    // on dragenter add a class for styling
    dropzone_element.addEventListener("dragenter", function(event) {
        if (is_valid_drop(dragging_element, event.currentTarget)) {
            event.currentTarget.classList.add(DROPZONE_DRAGOVER_CLASS);
        }
    });

    // remove class on dragleave
    dropzone_element.addEventListener("dragleave", function(event) {
        event.currentTarget.classList.remove(DROPZONE_DRAGOVER_CLASS);
    });

    // handle drop event
    dropzone_element.addEventListener("drop", function(event) {
        const dropzone_element = event.currentTarget;
        if (is_valid_drop(dragging_element, dropzone_element)) {
            event.preventDefault();
            // move dragged element
            move_element(dragging_element, dropzone_element);
            update_form();
        }
    });
}

function update_form() {
    const form = document.forms[0];
    form.dragdrop_json.value = JSON.stringify(dragdrop_data());
}

function validate_draggable(draggable_element) {
    if (!("draggableType" in draggable_element.dataset)) {
        // required data attribute is missing
        throw new Error(
            `${draggable_element} draggable element missing draggable-type data attribute`
        );
    }

    if (!("draggableData" in draggable_element.dataset)) {
        // required data attribute is missing
        throw new Error(
            `${draggable_element} draggable element missing draggable-data data attribute`
        );
    }
}

function init_draggable(draggable_element) {
    // initialize draggable element
    draggable_element.addEventListener("dragstart", function(event) {
        // begin dragging
        dragging_element = event.target;
        // add class indicating something is dragging to dropzones that can
        // accept it
        for (const dropzone_element of get_dropzones()) {
            if (is_valid_drop(dragging_element, dropzone_element)) {
                dropzone_element.classList.add(DROPZONE_DRAGGING_CLASS);
            }
        }
    });

    draggable_element.addEventListener("dragend", function(event) {
        // remove class indicating something is being dragged from dropzones
        for (const dropzone_element of get_dropzones()) {
            dropzone_element.classList.remove(DROPZONE_DRAGGING_CLASS);
            dropzone_element.classList.remove(DROPZONE_DRAGOVER_CLASS);
        }
        dragging_element = null;
    });
}

function has_draggable_type(element) {
    // element carries what draggable type it is
    return (
        "draggableType" in element.dataset
        && element.dataset.draggableType
    )
}

function has_dropzone_type(element) {
    return (
        // has the key
        "dropzoneType" in element.dataset
        // and value is truthy
        && element.dataset.dropzoneType
        // and value parses to truthy object
        && JSON.parse(element.dataset.dropzoneType)
    )
}

function is_valid_type(draggable_element, dropzone_element) {
    if (!(
        has_draggable_type(draggable_element)
        && has_dropzone_type(dropzone_element)
    )) {
        // either draggle or dropzone does not have required data attributes to
        // make type check
        return false
    }
    const draggable_type = draggable_element.dataset.draggableType;
    const dropzone_types = get_dropzone_types(dropzone_element);
    if (dropzone_types.indexOf(draggable_type) < 0) {
        // dropzone does not accept this type
        return false
    }
    return true
}

function is_valid_limit(element) {
    // TODO
    // -- number of dropped needs to account for *only* the direct dropzone
    //    dropped draggables.
    // -- maybe construct the dump object with reference to the element? and
    //    use that? would be simple array length check.
    console.warn("dropped limit check not implemented");
    return true
}

function trash_is_valid_limit(element) {
    const dropzone_limit = JSON.parse(dropzone_element.dataset.dropzoneLimit);
    const dropped = dropzone_element.querySelectorAll(DRAGGABLE_SELECTOR);
    if (dropped.length == dropzone_limit) {
        // dropped limit reached
        return false
    }
    return true
}

function is_valid_drop(draggable_element, dropzone_element) {
    return (
        // check element is dropzone
        is_dropzone(dropzone_element)
        // draggable is permitted to drop into dropzone
        && is_valid_type(draggable_element, dropzone_element)
        // check limit
        && is_valid_limit(dropzone_element)
    );
}

function update_inputs() {
    // update the inputs that dropzones reference from the draggables inside
    // them, that carry a data attribute for the input value
    for (const dropzone_element of get_dropzones()) {
        if (!('dropzoneInputId' in dropzone_element.dataset)) {
            continue
        }
        const input_id = dropzone_element.dataset.dropzoneInputId;
        const input_element = document.getElementById(input_id);
        const draggables_inside = get_draggables(dropzone_element);
        if (draggables_inside.length === 0) {
            // clear value for no draggable children
            // assumes invalid draggables have not gotten in
            input_element.value = "";
        } else {
            for (const draggable_element of draggables_inside) {
                if (!('draggableInputValue' in draggable_element.dataset)) {
                    // ignore missing input value
                    continue
                }
                const input_value = draggable_element.dataset.draggableInputValue;
                input_element.value = input_value;
            }
        }
    }
}

function draggable_object(draggable_element) {
    const draggable_data_string = draggable_element.dataset.draggableData;
    const draggable_data = JSON.parse(draggable_data_string);
    return draggable_data
}

function is_keep(element) {
    return (is_dropzone(element) || is_draggable(element));
}

function all(iterable) {
    for (const item of iterable) {
        if (!(item)) {
            return false
        }
    }
    return true
}

function any(iterable) {
    for (const item of iterable) {
        if (item) {
            return true
        }
    }
    return false
}

function* walk_filter(element, predicate) {
    if (predicate(element)) {
        yield element;
    }
    for (const child of element.children) {
        yield* walk_filter(child, predicate);
    }
}

function drag_or_drop(element) {
    return (is_dropzone(element) || is_draggable(element));
}

function* walk_draggable(element) {
    const result = JSON.parse(element.dataset.draggableData);
    for (const child of element.children) {
        for (const data of walk_dropzone(child)) {
            if (data) {
                Object.assign(result, data);
            }
        }
    }
    yield result;
}

function* walk_dropzone(element) {
    const result = {};
    if (element.dataset.dropzoneData) {
        Object.assign(result, JSON.parse(element.dataset.dropzoneData));
    }
    let key = null;
    if (is_list_collector(element)) {
        key = element.dataset.listName;
        result[key] = [];
    }
    for (const child of element.children) {
        for (const data of walk_dragdrop(child)) {
            if (data) {
                if (key) {
                    result[key].push(data);
                } else {
                    Object.assign(result, data);
                }
            }
        }
    }
    yield result;
}

function* walk_list_collector(element) {
    const key = element.dataset.listName;
    const result = {[key]: []};
    if (element.dataset.dropzoneData) {
        Object.assign(result, JSON.parse(element.dataset.dropzoneData));
    }
    for (const child of element.children) {
        for (const data of walk_dragdrop(child)) {
            if (data) {
                result[key].push(data);
            }
        }
    }
    yield result;
}

function* walk_dragdrop(element) {
    if (is_draggable(element)) {
        yield* walk_draggable(element);
    } else if (is_dropzone(element)) {
        yield* walk_dropzone(element);
    } else if (is_list_collector(element)) {
        yield* walk_list_collector(element);
    } else {
        for (const child of element.children) {
            yield* walk_dragdrop(child);
        }
    }
}

function dragdrop_data() {
    let result = {}
    for (const data of walk_dragdrop(document.body)) {
        Object.assign(result, data);
    }
    return result;
}

function dump_dragdrop_data() {
    const data = dragdrop_data();
    console.log(data);
}

function init_dragdrop() {
    // initialize dropzones
    for (const dropzone_element of get_dropzones()) {
        validate_dropzone(dropzone_element);
        init_dropzone(dropzone_element);
    }

    // initialize draggables
    for (const draggable_element of get_draggables()) {
        validate_draggable(draggable_element);
        init_draggable(draggable_element);
    }

    // dump data button
    let dump_button = document.getElementById("dump-drag-drop");
    if (dump_button) {
        dump_button.addEventListener("click", dump_dragdrop_data);
    }

    // initialize form data from html state
    update_form();
}

document.addEventListener("DOMContentLoaded", init_dragdrop);
