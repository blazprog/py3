//todo example from adi osmani book

var app = app || {};
var ENTER_KEY = 13; 

$(document).ready(function() {
    new app.AppView();
});


app.Todo = Backbone.Model.extend({
    defaults: {
        title: '',
        completed: false
    },
    toggle: function(){
       this.save({
        completed: !this.get('completed')
       }); 
    }
              
});

var TodoList = Backbone.Collection.extend({
    model: app.Todo,
    localStorage: new Backbone.LocalStorage('todos-backbone'),
    //filter down the list of all todo items that are finished
    completed: function(){
        return this.filter(function(todo){
            return todo.get('completed');
        });
    },
    
    remaining: function(){
        return this.without.apply(this, this.completed());
    },

    nextOrder: function() {
        if (!this.length) {
            return 1;
        }
        return this.last().get('order') + 1;
    },

    comparator: function(todo) {
        return todo.get('order');
    }
});


app.Todos = new TodoList();


app.AppView = Backbone.View.extend({
    el: '#todoapp',
    statsTemplate: _.template($('#stats-template').html() ),
    events: {
        'keypress #new-todo' : 'createOnEnter',
        'click #clear-completed' : 'clearCompleted',
        'click #toggle-all' : 'toggleAllComplete'
    },

    initialize: function() {
        this.allCheckbox = this.$('#toggle-all')[0];
        this.$input = this.$('#new-todo');
        this.$footer = this.$('#footer');
        this.$main = this.$('#main');
        this.listenTo(app.Todos,'add',this.addOne);
        this.listenTo(app.Todos,'reset',this.addAll);
        this.listenTo(app.Todos,'change:completed',this.filterOne);
        this.listenTo(app.Todos,'filter',this.filterAll);
        this.listenTo(app.Todos,'all',this.render);
        app.Todos.fetch();
    },

    render: function(){
        var completed = app.Todos.completed().length;
        var remaining = app.Todos.remaining().length;
        if (app.Todos.length) {
            this.$main.show();
            this.$footer.show();
            this.$footer.html(this.statsTemplate({
                completed: completed,
                remaining: remaining
            }));
            this.$('#filters li a')
                .removeClass('selected')
                .filter('[href="#/' + (app.TodoFilter || '') + '"]')
                .addClass('selected');
        } else {
            this.$main.hide();
            this.$footer.hide();
        }
        this.allCheckbox.checked =!remaining;
    },

    addOne: function(todo) {
        var view = new app.TodoView({model: todo});
        $('#todo-list').append(view.render().el);
    },
    addAll: function(){
        this.$('#todo-list').html('');
        app.Todos.each(this.addOne,this);
    },

    filterOne: function(todo) {
        todo.trigger('visible');
    },
    filterAll: function() {
        app.Todos.each(this.filterOne, this);
    },

    //Generate attributes for new todo item
    newAttributes: function() {
        return {
            title: this.$input.val().trim(),
            order: app.Todos.nextOrder(),
            completed: false
        };
    },

    createOnEnter: function(event) {
        if (event.which !== ENTER_KEY || !this.$input.val().trim() ) {
            return;
        }

        app.Todos.create(this.newAttributes());
        this.$input.val('');
    },

    clearCompleted: function() {
        _.invoke(app.Todos.completed(),'destroy');
        return false;
    },

    toggleAllComplete: function() {
        var completed = this.allCheckbox.checked;
        app.Todos.each(function(todo){
            todo.save({'completed' : completed});
        });
    }

});


//individula todo item
//

app.TodoView = Backbone.View.extend({
    tagName: 'li',
    template: _.template($('#item-template').html() ),
    events: {
        'dblclick label' : 'edit',
        'keypress edit' : 'updateOnEnter',
        'blur .edit' : 'close'
    },


    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
    },
    render: function() {
        console.log('In render');
        this.$el.html(this.template(this.model.toJSON()));
        this.$input = this.$('.edit');
        return this;
    },

    edit: function() {
        this.$el.addClass('editing');
        this.$input.focus();
    },

    close: function() {
        var value = this.$input.val().trim();
        alert('Finish todo editing ' + value);
        if (value) {
            this.model.set({title:value});
            this.model.save({title: value});
        }
        this.$el.removeClass('editing');
    },
    
    updateOnEnter: function(e) {
        if(e.which === ENTER_KEY ) {
            this.close();
        }
    }

});
