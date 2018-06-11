/*promises*/
var Costumer = {
    getDetails: function(customer_id) {
        var promise = $.ajax('/dokumenti/stranka/details/',{
            data: {q: costumer_id}
        });
        return promise;
    }            
}


/*end promises*/

function onbllur_Stranka(event) {
    var sifra_stranke = $(this).val();
    if (sifra_stranke === '') {
        return (false);
    }    
    lookup_stranka(sifra_stranke);
}


function lookup_stranka(sifra_stranke) {
    $.get('/dokumenti/stranka_details/', {'q':sifra_stranke}, function(data) {
        $('#id_stranka').val(data.idStranke);
        $('#id_txtNazivStranke').val(data.nazivStranke);
    });
}


function onblur_Artikel(event) {
    var sifra_artikla = $(this).val();
    var control_id = $(this).attr('id');
    var search = /id_dokumenti_racun-(\d+)-txtSifraArtikla/;
    a = control_id.match(search);
    var row = RegExp.$1;
    if (sifra_artikla === '') {
        selector_prefix = '#' + 'id_dokumenti_racun-' +  row + '-'; 
        //nastavim nazaj na privyete vrednosti. Taksno novo vrstico pri shranjevanju ignoriram 
        $(selector_prefix + 'artikel').val('');
        $(selector_prefix + 'txtNazivArtikla').val('');
        $(selector_prefix + 'kolicina').val(1);
        $(selector_prefix + 'cena').val(0);
        $(selector_prefix + 'davek').val(0);
        $(selector_prefix + 'popust').val(0);
        return (false);
    }    
    lookup_artikel(sifra_artikla, row);
}

function lookup_artikel(sifra_artikla, row) {
    selector_prefix = '#' + 'id_dokumenti_racun-' +  row + '-'; 
    $.get('/dokumenti/artikel_details/', {'q':sifra_artikla}, function(data) {
        $(selector_prefix + 'artikel').val(data.idArtikla);
        $(selector_prefix + 'txtNazivArtikla').val(data.naziv);
        $(selector_prefix + 'cena').val(data.cena);
        $(selector_prefix + 'davek').val(data.davek);
    });
    update_price();
}

function open_ModalStranka(event) {
    if (event.keyCode == 114) {
        event.stopPropagation();
        $("#modalStranka").modal('toggle');
        /*V attribut modalnege okna napisem ime kontrole v katero se naj prenese izbrana sifra*/
        $('#modalStranka').data('id_txtResult',event.data.id_txtResult);
        $('#txt_lookupStranke').focus();
    }
}

function open_ModalArtikel(event,id_txtResult,row) {
    if (event.keyCode == 114) {
        event.stopPropagation();
        $("#modalArtikel").modal('toggle');
        /*V attribut modalnege okna napisem ime kontrole v katero se naj prenese izbrana sifra*/
        $('#modalArtikel').data('id_txtResult',id_txtResult);
        $('#modalArtikel').data('row',row);
    }
}

function insert_resultTemplate(ev) {
    var table_name = ev.data.table;
    q = $(".txt_lookup:visible").val();
    $.get('/dokumenti/search/' + table_name + '/', {"q": q}, function(data) {
        $(".searchResult_placeholder:visible").html(data);
    });
}


function confirm_ModalStranka() {
    $('#modalStranka').modal('toggle');
    selector = '#' +  $('#modalStranka').data('id_txtResult');
    /*$(this) je button v tabeli, na katerega sem kliknil*/
    var sifraStranke = $(this).data('stranka_sifra'); 
    $(selector).val(sifraStranke);
    $(selector).focus();
    lookup_stranka(sifraStranke);
}


function confirm_ModalArtikel() {
    $('#modalArtikel').modal('toggle');
    //Preberem podatke, ki sev jih zapisal ob odprtju modalnega okna
    var selector = '#' +  $('#modalArtikel').data('id_txtResult');
    var row = $('#modalArtikel').data('row');
    /*$(this) je button v tabeli, na katerega sem kliknil*/
    var sifraArtikla = $(this).data('artikel_sifra'); 
    $(selector).val(sifraArtikla);
    lookup_artikel(sifraArtikla, row);
    $(selector).focus();
}


 
function setIdName(el, prefix, sufix, index) {
    el.attr('id',  'id_' + prefix + '-' + index + '-' + sufix);
    el.attr('name', prefix + '-' + index + '-' + sufix);
}


function addLine() {
    var formsetname = 'racunpozicija_set';
    var tablename = 'nakup-pozicije-vnos';
    var editFields = ['artikel','txtSifraArtikla', 'txtNazivArtikla', 'kolicina','cena','davek','popust']; 

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
    col = $('<td class="skupaj">0.00</td>');
    myRow.append(col);
    //This line is no longer last, so it doesent need that event
    $('#nakup-pozicije-vnos>tbody>tr:last-child>td:nth-child(2)>input').off('focus', addLine);
    $("#" + tablename).append(idField);
    $("#" + tablename).append(myRow);
    $("#id_" + formsetname + "-TOTAL_FORMS").val(formCount + 1);
    //Attach events to added controls
    $('#nakup-pozicije-vnos>tbody>tr:last-child>td:nth-child(2)>input').on('focus', addLine);
    $('.input-sifraArtikla').on('blur',onblur_Artikel);
    $('.input-sifraArtikla').on('keydown', function(event) {
        var control_id = $(this).attr('id');
        var search = /id_racunpozicija_set-(\d+)-txtSifraArtikla/;
        a = control_id.match(search);
        var row = RegExp.$1;
        return open_ModalArtikel(event,control_id,row);
    });

}

 

/*
 * Funkcije za preracunavanje vrednosti znesek v vrstici in skupni znesek
 */

function update_price() {
  var row = $(this).parents('.line-item');
  var kolicina = parseFloat(row.find('.kolicina>input').val());
  var cena =  parseFloat(row.find('.cena>input').val());
  var popust =  parseFloat(row.find('.popust>input').val());
  var davek =  parseFloat(row.find('.davek>input').val());
  popust = (100-popust)/100;
  davek = (100 + davek)/100;
  skupaj = cena*kolicina*popust*davek;
  row.find('.skupaj').html(skupaj.toFixed(2));
  //update_total();
}


$(document).ready(function() {
    $('#id_txtSifraStranke').on('keydown', {id_txtResult:'id_txtSifraStranke'}, open_ModalStranka);
    $('#id_txtSifraStranke').on('blur',onbllur_Stranka);
    $('.input-sifraArtikla').on('blur',onblur_Artikel);
    $('.input-sifraArtikla').on('keydown', function(event) {
        var control_id = $(this).attr('id');
        var search = /id_racunpozicija_set-(\d+)-txtSifraArtikla/;
        a = control_id.match(search);
        var row = RegExp.$1;
        return open_ModalArtikel(event,control_id,row);
    });

    //funkcije za preracunavanje totalov
    $('.sifra-artikel>input, .kolicina>input, .cena>input, .davek>input, .popust>input').on('blur', update_price);

    //funkcije za management grida
    //$("#add_line_btn").click(addLine2);
    //first child is hidden field idArtikla
    $('#nakup-pozicije-vnos>tbody>tr:last-child>td:nth-child(2)>input').on('focus', addLine);


    //Da dobim takoj focus na pravo polje v modalni formi
    $('#modalStranka').on('shown.bs.modal', function () {
        $('#txt_lookupStranke').focus();
    });

    $('#modalArtikel').on('shown.bs.modal', function () {
        $('#txt_lookupArtikel').focus();
    });
});
