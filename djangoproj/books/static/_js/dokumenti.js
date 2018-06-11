var skupineArtiklovData = [
    {id:1,naziv:'Vina'},
    {id:2,naziv:'Piva'},
    {id:3,naziv:'Zgane pijace'},
    {id:4,naziv:'Topli napitki'},
    {id:5,naziv:'Slani in sladki prigrizki'}
];


Stranka = Backbone.Model.extend({});

strankaTemplate = _.template($("#tmplStranka").html());
StrankaView = Backbone.View.extend({
    template: strankaTemplate,
    el : $('#searchResultStranka'),
    events: {
        'change input' : 'changed'
    },        
    initialize: function () {
        this.model.on('change', this.render, this);
    },
    render: function () {
        //return $(this.el).append(this.template(this.model.toJSON())) ;
        $(this.el).html(this.template(this.model.toJSON())) ;
        return this;
    },
    changed: function(evt) {
        console.log(evt.currentTarget.id + ' ' + 'changed');
        this.model.set(evt.currentTarget.id, $(evt.currentTarget).val());
    }
});   


Artikel = Backbone.Model.extend({});
artikelTemplate = _.template($('#tmplArtikel').html());
ArtikelView = Backbone.View.extend({
    initialize: function() {
        this.model.on('change', this.render, this);
    },
    events: {
        'change input' : 'changed'
    },        
    el : $('#searchResultArtikel'),
    template: artikelTemplate,
    render : function(){
       $(this.el).html(this.template(this.model.toJSON()));
       return this;
    },
    changed: function(evt) {
        console.log(evt.currentTarget.id + ' ' + 'changed');
        this.model.set(evt.currentTarget.id, $(evt.currentTarget).val());
    }
});


var SkupinaArtikla = Backbone.Model.extend({ });
var SkupinaArtiklaView = Backbone.View.extend({
    template : _.template($('#tmplSkupinaArtikla').html()),
    tagName: 'tr',
    events: {
        'change input' : 'changed'
    },        
    render: function() {
        this.$el.html(this.template(this.model.toJSON()));
        return this;
    },
    changed: function(evt) {
        console.log(evt.currentTarget.id + ' ' + 'changed');
        this.model.set(evt.currentTarget.id, $(evt.currentTarget).val());
    }
});

var SkupineArtiklov = Backbone.Collection.extend({
    model: SkupinaArtikla,
    url: '/dokumenti/get_skupina_artiklov/' 
});

var SkupineArtiklovView = Backbone.View.extend({
    el:'.skupinePlaceholder',
    tagName : 'table',
    className : 'table table-stripped table-bordered',
    events: {
        change: function() {
            console.log("Element in collection changed");
        }
    },
    initialize: function () {
         this.collection.on("reset", this.render,this);
         this.collection.on("add", this.renderOne,this);
    },

    render: function(){
        this.collection.forEach(this.renderOne,this);
        return this;
    },
    renderOne: function(skupinaArtikla) {
        var skupinaArtiklaView = new SkupinaArtiklaView({
            model: skupinaArtikla});
        this.$el.append(skupinaArtiklaView.render().el);
    }
});



var skupineArtiklov = new SkupineArtiklov();
var skupineArtiklovView = new SkupineArtiklovView({
    collection: skupineArtiklov });


$(document).ready(function() {
    alert('Ready master Teddy');
    /* 
    $.get('/dokumenti/get_skupina_artiklov/',function(data){
        skupineArtiklov.reset(data);
        $('.skupinePlaceholder').html(skupineArtiklovView.render().el);
    });*/

    skupineArtiklov.fetch();

    $('#butSearchStranka').on('click',function(){
        var sifra_stranke = $('#searchStranka').val();
        $.get('/dokumenti/stranka_details/', {'q':sifra_stranke}, function(data) {
            s = new Stranka();
            var sw = new StrankaView({model:s});
            s.attributes = data;
            sw.render();
        });
    }); //butSearchClick


    $('#butSearchArtikel').on('click',function() {
        var sifra_artikla = $('#searchArtikel').val();
        $.get('/dokumenti/artikel_details/', {'q':sifra_artikla}, function(data) {
            artikel = new Artikel();
            artikelView = new ArtikelView({model: artikel});
            artikel.attributes = data;
            artikelView.render();
        });
    }); //butSearchArtikel click


    $('#butSearchArtikelId').on('click',function() {
        var sifra_artikla = $('#searchArtikel').val();
        $.get('/dokumenti/get_artikel_by_id/', {'q':sifra_artikla}, function(data) {
            artikel = new Artikel();
            artikelView = new ArtikelView({model: artikel});
            artikel.attributes = data;
            artikelView.render();
        });
    }); //butSearchArtikelId click

    $('#searchResultArtikel').on('click','#butSaveArtikel',function(){
        alert('Saving artikel');
        $.ajax({
            url: '/dokumenti/artikel_details/',
            type: 'POST',
            //data: {jsondata: artikel.toJSON()}
            data: artikel.toJSON()
        });
    }); //butSaveArtikel click

}); //document ready function
