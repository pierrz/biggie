var pages = document.getElementsByClassName("level page"),
            page_buttons = document.getElementsByClassName("button page"),
            active_page = pages[0],
            active_button = page_buttons[0],
            previous = document.getElementsByClassName("pagination-previous")[0],
            next = document.getElementsByClassName("pagination-next")[0],
            total_pages = pages.length;

active_page.classList.toggle("active_page");
active_button.classList.toggle("active_button");

function activateButton(button_id_int) {
    active_button_id = "button-" + button_id_int.toString()
    active_button = document.getElementById(active_button_id);
    button.classList.toggle("active_button");
};

for (let i = 0; i < total_pages; i++) {
    button = page_buttons[i];
    button.onclick = function() {
        active_page = document.getElementsByClassName("active_page")[0];
        active_button = document.getElementsByClassName("active_button")[0];
        active_button.classList.toggle("active_button");
        active_page.classList.toggle("active_page");

        display_id = i + 1
        active_page = document.getElementById(display_id.toString());
        active_page.classList.toggle("active_page");
        // alert(display_id)
        activateButton(display_id)

        if (display_id == 1) {
          previous.classList.add("disabled");
        }
        else if (display_id == total_pages) {
          next.classList.add("disabled");
        }
        else {
          next.classList.remove("disabled");
          previous.classList.remove("disabled");
        };
    };
};

next.onclick = function() {

    active_id = Number(active_page.getAttribute("id"))

    if (active_id < total_pages) {
      active_page.classList.toggle("active_page");
      next_id = Number(active_page.getAttribute("id")) + 1;
      active_page = document.getElementById(next_id.toString());
      active_page.classList.toggle("active_page");
      next.classList.remove("disabled");
      activateButton(next_id)
    }
    else {
        next.style.cursor = "cursor";
        next.classList.add("disabled");
    };
};

previous.onclick = function() {

    active_id = Number(active_page.getAttribute("id"))

    if (active_id > 1) {
        active_page.classList.toggle("active_page");
        previous_id = Number(active_page.getAttribute("id")) - 1;
        active_page = document.getElementById(previous_id.toString());
        active_page.classList.toggle("active_page");
        previous.classList.remove("disabled");
        activateButton(previous_id)
    }
    else {
        previous.style.cursor = "cursor";
        previous.classList.add("disabled");
    };
};
