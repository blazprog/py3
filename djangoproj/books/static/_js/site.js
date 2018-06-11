//model for our book class
//
 /* alias away the sync method 
/spodnjo kodo rabim, da mi poslje csfr cookie nazaj na server
pri update operacijah
*/
Backbone._sync = Backbone.sync;

/* define a new sync method */
Backbone.sync = function(method, model, options) {

    /* only need a token for non-get requests */
    if (method == 'create' || method == 'update' || method == 'delete') {
        // CSRF token value is in an embedded meta tag 
        var csrfToken = $("meta[name='csrf_token']").attr('content');

        options.beforeSend = function(xhr){
            xhr.setRequestHeader('X-CSRFToken', csrfToken);
        };
    }

    /* proxy the call to the old sync method */
    return Backbone._sync(method, model, options);
};

var app = app || {};
app.Book = Backbone.Model.extend({
    defaults: {
        title: 'No title',
        author: 'Unknown',
        releaseDate: 'Unknown',
        keywords: 'None'
    }
});


app.Library = Backbone.Collection.extend({
    model: app.Book,
    url: '/api/books/'  //zadnji slash je pomemben
});


app.BookView = Backbone.View.extend({
    tagName: 'div',
    className: 'bookContainer',
    template: _.template($('#bookTemplate').html() ),
    events: {
        'click .delete' : 'deleteBook',
        'click .edit' : 'editBook',
        'click .save' : 'saveBook'
    },

    deleteBook: function() {
        //Delete model
        this.model.destroy();
        //Delete view
        this.remove();

    },
    
    editBook: function() {
        this.$el.find('li').addClass('editing');
        this.$el.find('div.button-container').addClass('editing');
    },

    saveBook: function() {
        this.$el.find('li').removeClass('editing');
        this.$el.find('div.button-container').removeClass('editing');
        var formData={};
        //id controle mora biti enak imenu property v modelu
        this.$el.find('input').each(function(i,el) {
            if ( $(el).val() !== '' ) {
                formData[el.id] = $(el).val();
            }
        });
        //this.model.set(formData);
        this.model.save(formData);
        this.render();
    },

    render: function() {
        this.$el.html(this.template(this.model.toJSON() ));
        return this;
    }

});


app.LibraryView = Backbone.View.extend({
    el: '#books',
    events: {
        'click #add_book': 'addBook'
    },

    initialize: function(initialBooks) {
        this.collection = new app.Library();
        this.collection.fetch({reset:true});
        this.listenTo( this.collection, 'add', this.renderBook );
        this.listenTo( this.collection, 'reset', this.render ); //izvede, ko se konca fetch
    },


    render: function() {
        this.collection.each(function(item) {
            this.renderBook(item);
        }, this);
    },

    renderBook: function(item) {
        var bookView = new app.BookView({
            model: item
        });
        this.$el.append(bookView.render().el);
    },

    addBook: function(e) {
        e.preventDefault();
        var formData={};
        $('#addBook').find('input').each(function(i,el) {
            if ( $(el).val() !== '' ) {
                formData[el.id] = $(el).val();
            }
        });
        //this.collection.add(new app.Book(formData));
        this.collection.create(formData);
    }
});


$(document).ready(function() {
    /* knjige bom prebral s serverja s pomocjo REST api 
    var books = [
        { title: 'JavaScript: The Good Parts', author: 'Douglas Crockford',
        releaseDate: '2008', keywords: 'JavaScript Programming' },
        { title: 'The Little Book on CoffeeScript', author: 'Alex MacCaw',
        releaseDate: '2012', keywords: 'CoffeeScript Programming' },
        { title: 'Scala for the Impatient', author: 'Cay S. Horstmann',
        releaseDate: '2012', keywords: 'Scala Programming' },
        { title: 'American Psycho', author: 'Bret Easton Ellis',
        releaseDate: '1991', keywords: 'Novel Splatter' },
        { title: 'Eloquent JavaScript', author: 'Marijn Haverbeke',
        releaseDate: '2011', keywords: 'JavaScript Programming' }
    ];
    */
    new app.LibraryView();    
});


