angular.module('tools', ['models'])
  .factory('session', ['$rootScope', '$http', 'models',
    function($s_root, $http, M) {
      $s_root.session = new M.Session();
      var session = {
        load: function() {
          return ($s_root.session.fetch()
            .then($s_root.session.fetchUser.bind($s_root.session)));
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
  ]);
