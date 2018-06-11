//project variables

var app = (function($){
    var config = $('#config');
    var app = JSON.parse(config.text());
    //ko je vse gotovo ustvarim router, ki v 
    //home funkciji, ki se sprozi ob routi '',
    //rendera HomePageView



    $(document).ready(function(){
        var router = new app.router();
    });

    return app;
})(jQuery);



//models
//Telovadba s csrf tokeni, je potrebna v modulu models,
//saj on komunicira z serverjem

(function ($, Backbone, _, app) {

    // CSRF helper functions taken directly from Django docs
    function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/i.test(method));
    }

    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = $.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(
                        cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    // Setup jQuery ajax calls to handle CSRF
    $.ajaxPrefilter(function (settings, originalOptions, xhr) {
        var csrftoken;
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            csrftoken = getCookie('csrftoken');
            xhr.setRequestHeader('X-CSRFToken', csrftoken);
        }
    });

    var BaseModel = Backbone.Model.extend({
        url: function()  {
            var links = this.get('links'), //links je slovar url naslovov, self je na samega sebe
             url = links && links.self;
            if (!url) {
                url = Backbone.Model.prototype.url.call(this); //klic parent methode, ce nimam svojega url
            }
            return url;
        } 
    }); //var BaseModel

    var BaseCollection = Backbone.Collection.extend({
        parse: function(response) {
            this._next = response.next;
            this._previous = response.previous;
            this._count = response.count;
            return response.results || [];
        },

        getOrFetch: function(id) {
            var result = new $.Deferred(),
                model = this.get(id);

            if (!model) {
                model = this.push({id:id});
                model.fetch({
                    success: function(model, response, options) {
                        result.resolve(model);
                    },
                    error: function(model, response, options) {
                        result.reject(model, response);
                    }
                });
            } else {
                result.resolve(model);
            }
            return result;
        }
    });

    app.models.Sprint = BaseModel.extend({
        fetchTasks: function() {
            var links = this.get('links');
            if (links && links.tasks) {
                app.tasks.fetch({url: links.tasks, remove: false});
            }
        }
        
    });
    app.models.Task = BaseModel.extend({
        statusClass: function() {
            var sprint = this.get('sprint'),
                status;
            if (!sprint) {
                status = 'unasigned';
            } else {
                status = ['todo', 'active', 'testing', 'done'][this.get('status') - 1];
            }
            return status;
        },
        inBacklog: function() {
            return !this.get('sprint');
        },
        inSprint: function(sprint) {
            return sprint.get('id') == this.get('sprint');
        }
    });

    app.models.User = BaseModel.extend({
        idAttributemodel: 'username'
    });

    app.collections.ready = $.getJSON(app.apiRoot);

    app.collections.ready.done(function(data){
        app.collections.Sprints = BaseCollection.extend({
            model: app.models.Sprint,
            url: data.sprints
        });

        app.sprints = new app.collections.Sprints();

        app.collections.Tasks = BaseCollection.extend({
            model: app.models.Task,
            url: data.tasks,
            getBacklog: function() {
                this.fetch({remove: false, data: {backlog: 'True'}});
            }
        });
        app.tasks = new app.collections.Tasks();

        app.collections.Users = BaseCollection.extend({
            model: app.models.User,
            url: data.users
        });
        app.users = new app.collections.Users();
    
    }); //ready.done


    var Session = Backbone.Model.extend({
        defaults: {
            token: null
        },
        initialize: function (options) {
            this.options = options;
            $.ajaxPrefilter($.proxy(this._setupAuth, this));
            this.load();
        },

        load: function () {
            var token = localStorage.apiToken;
            if (token) {
                this.set('token', token);
            }
        },

        save: function (token) {
            this.set('token', token);
            if (token === null) {
                localStorage.removeItem('apiToken');
            } else {
                localStorage.apiToken = token;
            }
        },
        delete: function () {
            this.save(null);
        },
        authenticated: function () {
            return this.get('token') !== null;
        },

        _setupAuth: function (settings, originalOptions, xhr) {
            if (this.authenticated()) {
                xhr.setRequestHeader(
                    'Authorization',
                    'Token ' + this.get('token')
                );
            }
        }
    });
    app.session = new Session();
})(jQuery, Backbone, _, app);


//views
(function ($, Backbone, _, app) {

    var TemplateView = Backbone.View.extend({
        templateName: '',
        initialize: function () {
            this.template = _.template($(this.templateName).html());
        },
        render: function () {
            var context = this.getContext(),
            html = this.template(context);
            this.$el.html(html);
        },
        getContext: function () {
            return {};
        }
    });


    var FormView = TemplateView.extend({
        events: {
            'submit form': 'submit',
            'click button.cancel': 'done'
        },
        errorTemplate: _.template('<span class="error"><%= msg %></span>'),

        modelFailure: function(model, xhr, options) {
            var errors = xhr.responseJSON;
            this.showErrors(errors);
        },

        showErrors: function(errors){
            _.map(errors, function(fieldErrors,name){
                var field = $('input[name=' + name + ']', this.form);
                var label = $('label[for=' + field.attr('id') + ']');
                if (label.length===0) {
                    label = $('label',this.form).first();
                }

                function appendError(msg) {
                    label.before(this.errorTemplate({msg:msg}));
                }

                _.map(fieldErrors, appendError, this);
            }, this);
        },
        
        clearErrors: function() {
            $('.error', this.form).remove();
        },

        serializeForm: function(form) {
            return _.object( _.map(form.serializeArray(), function(item) {
                return [item.name, item.value];
            }));
        },

        submit: function(event) {
            event.preventDefault();
            this.form = $(event.currentTarget);
            this.clearErrors();
            //naprej se realizira v subclassu
        },

        failure: function(xhr, status, error) {
            var errors = xhr.response.JSON;
            this.showErrors(errors);
        },

        done: function(event) {
            if (event) {
                event.preventDefault();
            }
            this.trigger('done');
            this.remove();
        }
    });


    var HeaderView = TemplateView.extend({
        tagName: 'header',
        templateName:'#header-template',
        events: {
            'click a.logout': 'logout'
        },
        getContext: function() {
            return {authenticated: app.session.authenticated()};
        },

        logout: function(event) {
            event.preventDefault();
            app.session.delete();
            window.location = '/';
        }
    });
    app.views.HeaderView = HeaderView;

    
    var NewSprintView = FormView.extend({
        templateName: '#new-sprint-template',
        className: 'new-sprint',
        /*events: _.extend({
            'click button.cance': 'done'
        },FormView.prototype.events),*/
        submit: function(event) {
            var self = this,
                attributes = {};
            FormView.prototype.submit.apply(this,arguments);
            attributes = this.serializeForm(this.form);
            app.collections.ready.done(function() {
                app.sprints.create(attributes, {
                    wait: true,
                    success: $.proxy(self.success,self),
                    fail: $.proxy(self.modelFailure,self)
                });
            });
                
        },
        success: function(model) {
            this.done();
            window.location.hash = '#sprint/' + model.get(id);
        }
    });

    
    var SprintView = TemplateView.extend({
        templateName: '#sprint-template',
        initialize: function(options) {
            var self = this;
            TemplateView.prototype.initialize.apply(this, arguments);
            this.sprintId = options.sprintId;
            this.sprint = null;
            this.tasks = [];
            this.statuses = {
                unassigned: new StatusView({ sprint: null, status: 1, title: 'Backlog'}), 
                todo: new StatusView({ sprint: this.sprintId, status: 1, title: 'Not Started' }),
                active: new StatusView({sprint: this.sprintId, status:2, title: 'In Development'}),
                testing: new StatusView({sprint: this.sprintId, status:3, title: 'In Testing'}),
                done: new StatusView({sprint: this.sprintId, status:4, title: 'Completed'}),
            };

            app.collections.ready.done(function() {
                app.tasks.on('add', self.addTask, self);
                app.sprints.getOrFetch(self.sprintId).done(function(sprint) { //get or fetch vrnt deferred
                    self.sprint = sprint;
                    self.render();
                    app.tasks.each(self.addTask, self);
                    sprint.fetchTasks();
                }).fail(function(sprint) {
                    self.sprint = sprint;
                    self.sprint.invalid = true;
                    self.render();
                });
                app.tasks.getBacklog();
            });
        },
        getContext: function() {
            return {sprint: this.sprint};
        },

        render: function() {
            TemplateView.prototype.render.apply(this, arguments);
             _.each(this.statuses, function(view, name) { 
                $('.tasks', this.$el).append(view.el);
                view.delegateEvents();
                view.render();
             }, this); 
            _.each(this.tasks, function(task) {
                this.renderTask(task);
            }, this); 
        },
        addTask: function(task) {
            //TODO: Handle the task
            if (task.inBacklog || task.inSprint(this.sprint)) {
                this.tasks[task.get('id')] = task;
                this.renderTask(task);
            }
        },

        renderTask: function(task) {
            var column = task.statusClass(),
                container = this.statuses[column],
                html = _.template('<div><%= task.get("name") %></div>', {task: task});
                $('.list', container.$el).append(html);
        }
        
    });
    app.views.SprintView = SprintView; //dodam v namespace, da vidim drugje v aplikaciji


    var AddTaskView = FormView.extend({
        templateName: '#new-task-template',
        /*Cancel button sem dodal v FormView base class
         * events: _.extend({
            'click button.cancel': 'done'
        }.FormView.prototype.events),*/ 

        submit: function(event) {
            var self = this,
                attributes = {};
            FormView.prototype.submit.apply(this, arguments);

            attributes = this.serializeForm(this.form);
            app.collections.ready.done(function() {
                app.tasks.create(attributes, {
                    wait: true,
                    success: $.proxy(self.success, self),
                    error: $.proxy(self.modelFailure, self)
                });
            });
        },
        success: function(model, resp, options) {
            this.done();
        }
    });

    var StatusView = TemplateView.extend({
        tagName: 'section',
        className: 'status',
        templateName: '#status-template',
        events: {
            'click button.addTask': 'renderAddForm'
        },
        initialize: function(options) {
            TemplateView.prototype.initialize.apply(this, arguments);
            this.sprint = options.sprint;
            this.status = options.status;
            this.title = options.title;
        },
        getContext: function() {
            return {sprint: this.sprint, title: this.title};
        },
        renderAddForm: function(event) {
            var view = new AddTaskView(),
                link = $(event.currentTarget);
                event.preventDefault();
                link.before(view.el);
                link.hide();
                view.render();
                view.on('done', function() {
                    link.show();
                });
        }
        
    });


    var HomepageView = Backbone.View.extend({
        templateName: '#home-template',
        events: {
            'click button.add': 'renderAddForm'
        },
        initialize: function () {
            var self = this;
            this.template = _.template($(this.templateName).html()); //this template je sedaj funkcija
            app.collections.ready.done(function() {
                app.sprints.fetch({
                    success: $.proxy(self.render, self)
                });
            });
        },
        render: function () {
            var context = this.getContext(),
            html = this.template(context); //funkciji podan kontekst, in vrne html
            this.$el.html(html);
        },
        getContext: function () {
            return {sprints: app.sprints || null};
        },
        renderAddForm: function(event) {
            var view = new NewSprintView(),
                link = $(event.currentTarget);

            event.preventDefault();
            link.before(view.el);
            link.hide();
            view.render();
            view.on('done', function() {
                link.show();
            });
        }
    });
    app.views.HomepageView = HomepageView;



    var LoginView = FormView.extend({
        id: 'login',
        templateName: '#login-template',

        submit: function(event) {
            var data = {};
            FormView.prototype.submit.apply(this, arguments);
            data = this.serializeForm(this.form);
            //todo: Submit the login data
            $.post(app.apiLogin, data)
                 .success($.proxy(this.loginSuccess, this))
                 .fail($.proxy(this.loginFailure, this));

        },

        loginSuccess: function(data) {
            app.session.save(data.token);
            this.done();
        }

    });
    app.views.LoginView = LoginView;
    

})(jQuery, Backbone, _, app);


//router
(function ($, Backbone,_ ,app) {
    var AppRouter = Backbone.Router.extend( {
        routes: {
            '' : 'home',  //routes uposteva od imena serverja naprej
            'sprint/:id' : 'sprint'  //prikaz posameznega sprinta
        },

        initialize: function(options) {
            this.contentElement = '#content';
            this.current = null;
            this.header = new app.views.HeaderView();
            $('body').prepend(this.header.el);
            this.header.render();
            Backbone.history.start();
        },
        home: function(i){
            var view = new app.views.HomepageView({
                el: this.contentElement
            });
            this.render(view);
        },

        sprint: function(id) {
            var view = new app.views.SprintView({
                el: this.contentElement,
                sprintId: id
            });
            this.render(view);
        },
        
        //override the default route to enforce login on every page
            
        route: function (route, name, callback) {
            // Override default route to enforce login on every page
            var login;
            callback = callback || this[name];
            callback = _.wrap(callback, function (original) {
                var args = _.without(arguments, original);
                if (app.session.authenticated()) {
                    original.apply(this, args);
                } else {
                    // Show the login screen before calling the view
                    $(this.contentElement).hide();
                    // Bind original callback once the login is successful
                    login = new app.views.LoginView();
                    $(this.contentElement).after(login.el);
                    login.on('done', function () {
                        this.header.render();
                        $(this.contentElement).show();
                        original.apply(this, args);
                    }, this);
                    // Render the login form
                    login.render();
                }
            });
            return Backbone.Router.prototype.route.apply(this, [route, name, callback]);
        },

        render: function(view) {
            if (this.current) {
                this.current.$el = $();
                this.current.remove();
            }
            this.current = view;
            this.current.render();
        }
    });
    app.router = AppRouter;
})(jQuery, Backbone, _, app);


