/**
 * Created by blazko on 7.6.2015.
 */

$(document).ready(function () {

    function setIdName(el, prefix, sufix, index) {
        el.attr('id',  'id_' + prefix + '-' + index + '-' + sufix);
        el.attr('name', prefix + '-' + index + '-' + sufix);
    }


    function addLine2() {
        var formsetname = 'nakupizdelki_set';
        var tablename = 'nakup-pozicije';
        var editFields = ['izdelek', 'kolicina', 'cena']; 

        var formCount = parseInt($('#id_' + formsetname + '-TOTAL_FORMS').val());
        var idField = $('#id_' + formsetname + '-__prefix__-id').clone();
        setIdName(idField, formsetname,'id', formCount); 

        var myRow = $('<tr/>');
        var field;
        var col;
        for (i=0; i < editFields.length; i++) {
            field = $('#id_' + formsetname + '-__prefix__-' + editFields[i]).clone();
            setIdName(field, formsetname, editFields[i], formCount); 
            col = $('<td class=' + editFields[i] + '/>');
            col.append(field);
            myRow.append(col);
        } 
        //This line is no longer last, so it doesent need that event
        $("#" + tablename + ">tbody>tr:last-child>td:first-child>input").off('focus', addLine); 
        $("#" + tablename).append(idField);
        $("#" + tablename).append(myRow);
        $("#id_" + formsetname + "-TOTAL_FORMS").val(formCount + 1);
        //Attach add event to new last line
        $('#nakup-pozicije>tbody>tr:last-child>td:first-child>input').on('focus', addLine);
        $('.izdelek').on('keydown', {akcija:'isci'}, lookup);

    }

    function addLine() {
        var formsetname = 'nakupizdelki_set';
        var formCount = parseInt($('#id_' + formsetname + '-TOTAL_FORMS').val());
        var idField = $('#id_nakupizdelki_set-__prefix__-id').clone();
        setIdName(idField, formsetname,'id', formCount); 
        var izdelekField = $('#id_nakupizdelki_set-__prefix__-izdelek').clone();
        setIdName(izdelekField, formsetname,'izdelek', formCount); 
        var cenaField = $('#id_nakupizdelki_set-__prefix__-cena').clone();
        setIdName(cenaField, formsetname,'cena', formCount); 
        var kolicinaField = $('#id_nakupizdelki_set-__prefix__-kolicina').clone();
        setIdName(kolicinaField, formsetname ,'kolicina',formCount); 
        myRow = $('<tr/>');
        col1 = $('<td class="izdelek"/>');
        col2 = $('<td class="kolicina" />');
        col3 = $('<td class="cena"/>');
        col1.append(izdelekField);
        col2.append(kolicinaField);
        col3.append(cenaField);
        myRow.append(col1);
        myRow.append(col2);
        myRow.append(col3);

        //This line is no longer last, so it doesent need that event
        $('#nakup-pozicije>tbody>tr:last-child>td:first-child>input').off('focus', addLine); 
        $("#nakup-pozicije").append(idField);
        $("#nakup-pozicije").append(myRow);
        $("#id_" + formsetname + "-TOTAL_FORMS").val(formCount + 1);
        //Attach add event to new last line
        $('#nakup-pozicije>tbody>tr:last-child>td:first-child>input').on('focus', addLine);
    }
   
    function lookup(event) {
        if (event.keyCode == 114) {
            $("#myModal").data('target_id', event.target.id);
            $("#myModal").modal();
        }
    }

    $("#add_line_btn").click(addLine2);
    $('#nakup-pozicije>tbody>tr:last-child>td:first-child>input').on('focus', addLine2);
    $('.izdelek').on('keydown', {akcija:'isci'}, lookup);
    $('#btnOkModal').on('click',function() {
        var tid = $('#myModal').data('target_id');
        var selectedText = $( "#modal_chooser option:selected" ).text();
        $('#'+ tid).val(selectedText);
        $("#myModal").modal('toggle');
    });
    
});


