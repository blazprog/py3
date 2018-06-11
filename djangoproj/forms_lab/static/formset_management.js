/**
 * Created by blazko on 7.6.2015.
 * Funkcije za upravljanje s formsetom.
 * Tabela mora imeti nastavljeno data na formsetname iz django, ker imena
 * vseh kontrol izhajajo iz njega.
 */


function setIdName(el, prefix, sufix, index) {
    el.attr('id',  'id_' + prefix + '-' + index + '-' + sufix);
    el.attr('name', prefix + '-' + index + '-' + sufix);
}



function move(control_id, step,table_id) {
    formset_name = $('#' + table_id).data('formsetname');
    elid_before = '(id_' + formset_name + '_set-)';
    after = '(-\\w+)';
    var id_regex = new RegExp(elid_before + '(\\d+)' + after) ;
    var new_control_id = control_id.replace(id_regex,function($0,$1,$2,$3) {
        var new_index =  parseInt($2) + step;
        return $1 + new_index + $3;      
    });
    $('#' + new_control_id).focus();
}

function inc_function($0,$1,$2,$3) {
    var new_index =  parseInt($2) + 1;
    return $1 + new_index + $3;      

} 

function incrementIndex($table_row, formset_name) {
    elid_before = '(id_' + formset_name + '_set-)';
    elname_before = '(' + formset_name + '_set-)';
    after = '(-\\w+)';
    var id_regex = new RegExp(elid_before + '(\\d+)' + after) ;
    var name_regex = new RegExp(elname_before + '(\\d+)' + after) ;
    $table_row.find('input').each(function() {
        input_id = $(this).attr('id');
        input_name = $(this).attr('name');
        new_input_id = input_id.replace(id_regex,inc_function);
        new_input_name = input_name.replace(name_regex,inc_function);
        $(this).attr('id',new_input_id);
        $(this).attr('name',new_input_name);
    });
}

function addLine(event) {
    //zadnja vrstica v tabeli je vedno nevidna.
    //Uporabim jo kot vzorec (klon) za dodajanje.
    //Ko dodam novo, klonirano vrstico na predzadnje mesto v tabeli,
    //moram spremeniti indekse v zadnji, nevidni vrstici
    //Tabela mora imeti data atribut ime formseta
    var formset_name = event.data.formset_name;
    var table_id = event.data.table_id;
    $table = $('#' + table_id);
    $lastRow = $table.find('tr:last');
    $newRow = $lastRow.clone();
    incrementIndex($lastRow,formset_name);
    $('#' + table_id + '>tbody>tr').eq(-2).find('td input').off('focus',addLine);
    $newRow.insertBefore($table.find('tr:last'));
    //increment hidden field that holds number of forms
    hidden_input_id = '#id_' + formset_name + '_set-TOTAL_FORMS';
    var formCount = parseInt($(hidden_input_id).val());
    $(hidden_input_id).val(formCount + 1);
    //focus on last line should add a new one
    //tu je strasno glupo napisano, moram cimprej popravit z event delegation
    $('#' + table_id + '>tbody>tr').eq(-2).find('td input').on('focus',
            {formset_name:formset_name,
             table_id: table_id},
            addLine);
}




function handle_keys(event) {
    var moveDirection = 0;

    switch(event.keyCode) {
        case 38:
            moveDirection = -1;
            break;
        case 40:
            moveDirection = 1;
            break;
    }
    if (moveDirection){
        move($(this).attr('id'),moveDirection,event.data.table_id); 
    }
}


$(document).ready(function () {
    $("#add_line_btn").click(addLine);
    $('#nakup-pozicije>tbody>tr').eq(-2).find('td input').on('focus',
            {formset_name:'nakupizdelki',
             table_id : 'nakup-pozicije'},
            addLine);
    //$('.izdelek input').on('keydown', lookup);
    $('#nakup-pozicije').on('keydown','input',{table_id:'nakup-pozicije'},handle_keys);
});


