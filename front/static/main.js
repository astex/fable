angular.module('app', ['ngRoute', 'config', 'controllers', 'models'])
  .config(['$routeProvider', '$httpProvider',
    function($routeProvider, $httpProvider) {
      $httpProvider.defaults.withCredentials = true;

      $routeProvider
        .when('/login', {
          templateUrl: 'templates/login.html',
          controller: 'LoginController'
        })
        .when('/deployment/:deployment_id/collection', {
          templateUrl: 'templates/deployment.html',
          controller: 'DeploymentController'
        })
        .when('/calendar/:year/:month', {
          templateUrl: 'templates/calendar.html',
          controller: 'CalendarController'
        })
        .otherwise({redirectTo: '/deployment'});
    }
  ])
  .factory('session', ['$rootScope', '$http', 'models',
    function($s_root, $http, M) {
      $s_root.session = new M.Session();
      var session = {
        load: function() {
          $s_root.session.fetch()
            .then($s_root.session.fetchUser.bind($s_root.session));
        },
        logout: function() {
          return ($s_root.session.delete()
            .then(function() {
              $s_root.session = new M.Session();
              location.href = '#/login';
            }));
        }
      };

      $s_root.logout = session.logout;
      return session;
    }
  ])
  .factory('error', ['$rootScope',
    function($s_root) {
      return {
        clear: function() { $s_root.error = undefined; },
        raise: function(r) {
          $s_root.header_class = 'full';
          $s_root.error = r;
        }
      };
    }
  ])
  .filter('find', [function() {
    // Like filter, but only returns the first instance.
    return function(arr, test, ctx) {
      var r = null;
      var f = (
        typeof test == "object" ?
          function(el) {
            for (var k in test)
              if (test.hasOwnProperty(k) && test[k] !== el[k])
                return false;
            return true;
          } :
        test
      );
      arr.some(function(el, i) {
        return f.call(ctx, el, i, arr) ? ((r = el), true) : false;
      });
      return r;
    };
  }])
  .filter('dtFormat', [function() {
    return function(dt, format) {
      return moment(dt).format(format);
    };
  }])
  .filter('underscoreToCamelCase', [function() {
    return function(s) {
      return s.toLowerCase().replace(/_(.)/g, function(match, group1) {
        return group1.toUpperCase();
      });
    };
  }]);
