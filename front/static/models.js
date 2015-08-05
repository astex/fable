angular.module('models', ['config'])
  .factory('classes', [function() {
    var C = {};

    C.Base = function() {};
    C.Base.extend = function(prototype, properties, static) {
      var parent = this;
      var child = (
        prototype.hasOwnProperty('constructor') ? prototype.constructor :
        function() { parent.apply(this, arguments); }
      );

      child.prototype = Object.create(parent.prototype, properties);
      angular.extend(child.prototype, prototype);
      angular.extend(child, parent, static || {});

      return child;
    };

    return C;
  }])
  .factory('relations', ['$filter', 'classes', function($f, C) {
    var R = {};

    R.Relation = C.Base.extend(
      {
        constructor: function(opts) {
          C.Base.apply(this, arguments);
          this.name = opts.name; this.model = opts.model;
          this.filters = opts.filters;
        }
      }, {
        fetcher_name: {get: function() {
          return $f('underscoreToCamelCase')('fetch_' + this.name);
        }}
      }
    );

    R.OneToOne = R.Relation.extend({
      constructor: function(opts) {
        R.Relation.apply(this, arguments);
        this.key = opts.key;
      },

      fetcher: function(m, filters) {
        m[this.name] = m[this.name] || new this.model();

        if (!m.data[this.key])
          return;

        return (m[this.name]
          .set({id: m.data[this.key]})
          .setFilters(angular.extend({}, this.filters, filters))
          .fetch());
      }
    });

    R.OneToMany = R.Relation.extend({
      constructor: function(opts) {
        R.Relation.apply(this, arguments);
        this.key = opts.key; this.reverse_name = opts.reverse_name;
      },

      fetcher: function(m, filters) {
        var r = this;

        m[r.name] = m[r.name] || new r.model();

        var f = {};
        f[r.key] = m.id;

        return (m[r.name]
          .setFilters(angular.extend({}, f, r.filters, filters))
          .fetch()
          .then(function() {
            if (r.reverse_name)
              m[r.name].models.forEach(function(submodel) {
                submodel[r.reverse_name] = m;
              });
          }));
      }
    });

    return R;
  }])
  .factory('models', [
    '$http', '$httpParamSerializer', '$filter', '$q',
    'apiURL', 'classes', 'relations',
    function($http, $param, $filter, $q, apiURL, C, R) {
      var M = {};

      M.Base = C.Base.extend({
        constructor: function() {
          var m = this;

          C.Base.apply(m, arguments);
          m.relations.forEach(function(r) {
            m[r.fetcher_name] = m.getRelatedFetcher(r);
          });
          m.filters = {};
        },

        setFilters: function(f) {
          angular.extend(this.filters, f);
          return this;
        },

        getRelatedFetcher: function(r) {
          var m = this;
          return function() {
            var arguments_ = Array.prototype.splice.call(arguments);
            arguments_.unshift(m);
            return r.fetcher.apply(r, arguments_);
          };
        }
      });

      M.Model = M.Base.extend(
        {
          constructor: function() {
            M.Base.apply(this, arguments);
            this.data = {};
          },

          id_field: 'id',
          relations: [],

          set: function(d) {
            angular.extend(this.data, d);
            return this;
          },

          fetch: function() {
            var m = this;
            return ($http.get(m.url)
              .then(function(r) { m.set(r.data.data); }));
          },

          save: function() {
            var m = this;
            return ($http[m.id ? 'put' : 'post'](m.url, m.data)
              .then(function(r) { m.set(r.data.data); }));
          },

          delete: function() {
            var m = this;
            return ($http.delete(m.url)
              .then(function(r) { delete m.data[m.id_field]; }));
          }
        }, {
          id: {get: function() { return this.data[this.id_field]; }},

          url: {get: function() {
            return (
              apiURL + this.uri + (this.id || '') +
              '?' + $param(this.filters)
            );
          }}
        }
      );

      M.List = M.Base.extend(
        {
          constructor: function() {
            M.Base.apply(this, arguments);
            this.models = [];
          },

          relations: [],

          filter: function() {
            var arguments_ = Array.prototype.slice.apply(arguments);
            arguments_.unshift(this.models);
            return $filter('filter').apply(this, arguments_);
          },

          find: function(test, ctx) {
            var arguments_ = Array.prototype.slice.apply(arguments);
            arguments_.unshift(this.models);
            return $filter('find').apply(this, arguments_);
          },

          fetch: function() {
            var c = this;
            return ($http.get(c.url)
              .then(function(r) {
                c.models = r.data.data.map(function(m) {
                  return (new c.model()).set(m);
                });
              }));
          }
        }, {
          url: {get: function() {
            return apiURL + this.model.prototype.uri + '?' + $param(this.filters);
          }}
        }
      );

      M.User = M.Model.extend({uri: '/user/'});
      M.Users = M.List.extend({model: M.User});

      M.Session = M.Model.extend({
        uri: '/session/',
        relations: [
          new R.OneToOne({
            model: M.User, name: 'user', key: 'user_id',
            filters: {verbosity: 'self'}
          })
        ]
      });

      M.Action = M.Model.extend({uri: '/action/'});
      M.Actions = M.List.extend({model: M.Action});

      M.Result = M.Model.extend({uri: '/result/'});
      M.Results = M.List.extend({model: M.Result});

      M.Step = M.Model.extend({uri: '/step/'});
      M.Steps = M.List.extend({model: M.Step});

      M.Run = M.Model.extend({uri: '/run/'});
      M.Runs = M.List.extend({model: M.Run});

      M.Target = M.Model.extend({uri: '/target/'});
      M.Targets = M.List.extend({model: M.Target});

      M.Story = M.Model.extend({uri: '/story/'});
      M.Stories = M.List.extend({model: M.Story});

      M.Collection = M.Model.extend({uri: '/collection/'});
      M.Collections = M.List.extend({model: M.Collection});

      M.Deployment = M.Model.extend({
        uri: '/deployment/',
        relations: [
          new R.OneToMany({
            model: M.Users, name: 'users', key: 'deployment_id',
            filters: {verbosity: 'guest'}
          }),
          new R.OneToMany({model: M.Collections, name: 'collections', key: 'deployment_id'}),
          new R.OneToMany({model: M.Stories, name: 'stories', key: 'deployment_id'}),
          new R.OneToMany({model: M.Targets, name: 'targets', key: 'deployment_id'}),
          new R.OneToMany({
            model: M.Runs, name: 'runs', key: 'deployment_id', reverse_name: 'deployment'
          }),
          new R.OneToMany({
            model: M.Steps, name: 'steps', key: 'deployment_id', reverse_name: 'deployment'
          }),
          new R.OneToMany({
            model: M.Results, name: 'results', key: 'deployment_id', reverse_name: 'deployment'
          }),
          new R.OneToMany({
            model: M.Actions, name: 'actions', key: 'deployment_id', reverse_name: 'deployment'
          })
        ],

        fetchAll: function() {
          var m = this;
          return ($q
            .all([
              m.fetch(), m.fetchCollections(), m.fetchStories(), m.fetchTargets(), m.fetchRuns(),
              m.fetchSteps(), m.fetchResults(), m.fetchActions(), m.fetchUsers()
            ])
            .then(function() {
              // Populate submodels.
              m.targets.models.forEach(function(target) {
                target.results = m.results.filter({data: {target_id: target.id}}, true);
              });
              m.stories.models.forEach(function(story) {
                story.targets = m.targets.filter({data: {story_id: story.id}}, true);
                story.steps = m.steps.filter({data: {story_id: story.id}}, true);
              });
              m.collections.models.forEach(function(collection) {
                collection.stories = m.stories.filter({data: {collection_id: collection.id}}, true);
                collection.runs = m.runs.filter({data: {collection_id: collection.id}}, true);
              });

              m.actions.models.forEach(function(action) {
                action.user = m.users.find({id: action.data.user_id});
              });
              m.results.models.forEach(function(result) {
                result.step = m.steps.find({id: result.data.step_id});
                result.actions = m.actions.filter({data: {result_id: result.id}}, true);
              });
              m.steps.models.forEach(function(step) {
                step.run = m.runs.find({id: step.data.run_id});
                step.results = m.results.filter({data: {step_id: step.id}}, true);
              });
              m.runs.models.forEach(function(run) {
                run.user = m.users.find({id: run.data.user_id});
                run.steps = m.steps.filter({data: {run_id: run.id}}, true);
              });
            }));
        }
      });
      M.Deployments = M.List.extend({
        model: M.Deployment,

        getByDay: function(day) {
          if (!this.models.length)
            return;
          return this.find(function(d) {
            return moment(d.data.target).format('L') == day.format('L');
          });
        }
      });

      return M;
    }
  ]);
