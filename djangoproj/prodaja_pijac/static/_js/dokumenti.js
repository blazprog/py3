var skupineArtiklovData = [
    {id:1,naziv:'Vina'},
    {id:2,naziv:'Piva'},
    {id:3,naziv:'Zgane pijace'},
    {id:4,naziv:'Topli napitki'},
    {id:5,naziv:'Slani in sladki prigrizki'}
];


Stranka = Backbone.Model.extend({
    urlRoot:'/dokumenti/api/stranke/',
    defaults: {
        id: null,
        sifra:'',
        naziv: '',
        ulica: '',
        posta: '',
        kraj: ''
    }
});

strankaTemplate = _.template($("#tmplStranka").html());
StrankaView = Backbone.View.extend({
    template: strankaTemplate,
    el : $('#searchResultStranka'),
    events: {
        'change input' : 'changed',
        'click button#butSaveStranka' : 'saveModel'
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
        //console.log(evt.currentTarget.id + ' ' + 'changed');
        this.model.set(evt.currentTarget.id, $(evt.currentTarget).val());
    },
    saveModel: function(evt) {
        console.log("Saving model");
        console.log(this.model.get('naziv'));
        this.model.save();
    }
});   


Artikel = Backbone.Model.extend({
    urlRoot:'/dokumenti/api/artikli/', 
    defaults: {
        sifra: '',
        naziv: '',
        skupina: '',
        cena: 0,
        davek: 0,
        em: ''
    }
});

artikelTemplate = _.template($('#tmplArtikel').html());
ArtikelView = Backbone.View.extend({
    initialize: function() {
        this.model.on('change', this.render, this);
    },
    events: {
        'change input' : 'changed',
        'click #butSaveArtikel' : 'saveModel'
    },        
    el : $('#searchResultArtikel'),
    template: artikelTemplate,
    render : function(){
       $(this.el).html(this.template(this.model.toJSON()));
       return this;
    },
    changed: function(evt) {
        //console.log(evt.currentTarget.id + ' ' + 'changed');
        this.model.set(evt.currentTarget.id, $(evt.currentTarget).val());
    },
    saveModel: function(e) {
        console.log("Saving model");
        console.log(this.model.get('naziv'));
        this.model.save();
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

    skupineArtiklov.fetch(); //ko bodo fetchani, jih bo prikazal view

    var s=new Stranka();
    var sw = new StrankaView({model:s});
    $('#butSearchStranka').on('click',function(){
        var sifra_stranke = $('#searchStranka').val();
        s.set({id: sifra_stranke});
        s.fetch();
        sw.render();
    }); //butSearchClick
    $('#butAddStranka').on('click', function() {
        s.set({
            id: null,
            sifra:'',
            naziv: '',
            ulica: '',
            posta: '',
            kraj: ''
        });
        sw.render();
    })

    var artikel = new Artikel();
    var artikelView = new ArtikelView({model: artikel});
    $('#butSearchArtikel').on('click',function() {
        var sifra_artikla = $('#searchArtikel').val();
        artikel.set({id: sifra_artikla});
        artikel.fetch();
        artikelView.render();
    }); //butSearchArtikel click
    $('#butAddArtikel').on('click', function() {
        artikel.set({
            id: null,
            sifra: '',
            naziv: '',
            skupina: '',
            cena: 0,
            davek: 0,
            em: '',
        })
        artikelView.render();
    })

    
}); //document ready function
