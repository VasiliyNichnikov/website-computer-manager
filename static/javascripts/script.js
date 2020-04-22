$(document).ready(function () {
    $(".btn-more-details").click(function () {
        $(this).parents('.col').children('.more-details').animate({
            height: ["toggle", "swing"],
            opacity: "toggle"
        }, {
            duration: 200,
            easing: "linear",
            query: false
        });
    });
});


function sending_programs_scenario(condition, id) {
    var message = document.getElementById("message");

    var programs = [];
    var lines = document.querySelectorAll('.program_info');
    var name_scenario = document.getElementById('name_scenario').value;

    for(var i = 0; i < lines.length; i++){
        var line = lines[i].value;
        programs.push(line);
    }
    var request = new XMLHttpRequest();
    request.responseType = "json";
    var json_programs = '';
    if(condition === 'add'){
        json_programs = JSON.stringify({"programs": programs, "name_scenario": name_scenario});
        request.open("POST", "/create_new_scenario", true);
    }
    else {
        json_programs = JSON.stringify({"programs": programs, "name_scenario": name_scenario, "id": id});
        request.open("POST", "/edit_scenario", true);
    }
    request.setRequestHeader('Content-type', 'application/json; charset=utf-8');

    request.addEventListener("readystatechange", () => {
       if(request.readyState === 4 && request.status === 200){
           let obj = request.response;
           if(obj.success){
               document.location.replace("/scenarios")
           }else if(obj.error){
               message.innerHTML = obj.error;
           }
       }
    });
    request.send(json_programs);
}


function delete_program_scenario() {
    var elem = document.querySelector('.button-delete-block-program');
    var parents = document.querySelectorAll('.parent-block-scenario');

    let array_parents = [];

    for (var i = 0; i < parents.length; i++) {
        var parent = parents[i];
        if (parent.contains(elem)) {
            //array_parents.unshift(parent);
            parent.remove();
        }
    }
    //print(array_parents);
    //array_parents[0].remove();
}


function copy_clipboard(){
    var copyInformation = document.querySelector('.js-keycopybtn');
    copyInformation.addEventListener('click', function(event){
        var informationLink = document.querySelector('.js-keylink');
        var range = document.createRange();
        range.selectNode(informationLink);
        window.getSelection().addRange(range);
        
        try{
            var successful = document.execCommand('copy');
            var msg = successful ? 'successful' : 'unsuccessful';
            console.log('Copy information command was: ' + msg);
        }catch(err){
            print('sdds');
            console.log('Ooops, unable to copy');
        }
        window.getSelection().removeAllRanges();
    });
}


function add_program_scenario() {
    console.log("Hello!");
    // Работа с get запросами.
    var req = new XMLHttpRequest();
    // Нужно менять запрос
    req.open("GET", "/get_programs_for_scenarios", false);
    req.send(null);
    var array_json_programs  = JSON.parse(req.responseText);
    var array_programs = array_json_programs['programs'];

    // Создание блока
    var container = document.getElementById("add_program_scenario");

    var count_children = container.childNodes.length;

    var main_div = document.createElement("div");
    main_div.className = "row pt-3 parent-block-scenario";
    main_div.id = "block_program";

    var col_div = document.createElement("div");
    col_div.className = "col";

    var program_div = document.createElement("div");
    program_div.className = "block-add-program-scenario parent";

    var board_programs = document.createElement("div");
    board_programs.className = "button-right-program children-center-vertical";

    var button_delete = document.createElement("button");
    button_delete.type = "button";
    button_delete.className = "button-delete-block-program btn btn-danger";
    button_delete.setAttribute("onclick", "delete_program_scenario()");
    button_delete.textContent = "Удалить";

    var str = '<input type="search" class="program_info" list="character">';

    var datalist_programs = document.createElement("datalist");
    datalist_programs.id = "character";

    for(var i = 0; i < array_programs.length; i++){
        var option = document.createElement("option");
        option.value = array_programs[i];
        datalist_programs.appendChild(option);
    }

    var title_program = document.createElement("h6");
    title_program.className = "children-center-vertical";
    title_program.style = "padding-left: 20px;";
    title_program.innerHTML = "Добавление прогаммы";

    board_programs.innerHTML = str;
    board_programs.appendChild(datalist_programs);
    board_programs.appendChild(button_delete);

    program_div.appendChild(title_program);
    program_div.appendChild(board_programs);

    col_div.appendChild(program_div);
    main_div.appendChild(col_div);

    container.appendChild(main_div);
}
