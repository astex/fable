angular.module('app', ['ngRoute', 'config', 'controllers'])
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
        .otherwise({redirectTo: '/login'});
    }
  ]);
