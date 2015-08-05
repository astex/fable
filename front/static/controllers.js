angular.module('controllers', ['models'])
  .controller('LoginController', [
    '$rootScope', '$scope', '$routeParams',
    'session', 'error', 'models',
    function($s_root, $s, $p, session, error, M) {
      error.clear();
      session.load();

      $s_root.header_class = 'full';
      $s.form = 'login';
      $s.form_errors = {};
      $s.user = ((new M.User()).setFilters({verbosity: 'guest'}));

      $s.changeForm = function(form) { $s.form = form; };

      $s.validate = function(field) {
        var value = $s.user.data[field];
        var error = (function() {
          if (!value)
            return 'Please fill this out.';
          else if (
              field == 'email' &&
              !/^(([^<>()[\]\.,;:\s@\"]+(\.[^<>()[\]\.,;:\s@\"]+)*)|(\".+\"))@(([^<>()[\]\.,;:\s@\"]+\.)+[^<>()[\]\.,;:\s@\"]{2,})$/i.test(value)
            )
            return 'Please enter a valid email.';
          else if (
              field == 'confirm' &&
              $s.user.data.password !== value
            )
            return 'Passwords don\'t match.';
        })();

        if (error)
          $s.form_errors[field] = [error];
        else
          delete $s.form_errors[field];

        return !error;
      };

      $s.login = function() {
        var s = new M.Session();
        ['email', 'password'].some(function(f) {
          if (!$s.validate(f))
            return true;
        });
        return ((new M.Session()).set({
            email: $s.user.data.email,
            password: $s.user.data.password
          })
          .save()
          .then(function() {
            var next = $p.next;
            if (next)
              next = decodeURIComponent(next);
            if (!(next && next[0] == '#'))
              next = '#/calendar/' + moment().format('YYYY/MM');
            window.location.href = next;
          }))
          .catch(function(r) { $s.form_errors = r.data.data; });
      };
      $s.signup = function() {
        ['email', 'name', 'password', 'confirm'].some(function(f) {
          if (!$s.validate(f))
            return true;
        });
        return ($s.user.save()
          .then(function() { $s.login(); }))
          .catch(function(r) { $s.form_errors = r.data.data; });
      };
    }
  ])
  .controller('CalendarController', [
    '$filter',
    '$rootScope', '$scope', '$routeParams',
    'session', 'error', 'models',
    function($f, $s_root, $s, $p, session, error, M) {
      error.clear();
      session.load();

      $s.moment = moment;
      $s_root.header_class = 'under';
      var find = $s.find = $f('find');

      $s.month = moment($p.year + '-' + $p.month, 'YYYY-MM');
      var start = $s.month.clone().startOf('month');
      var end = start.clone().add(5, 'weeks');

      $s.deployments = ((new M.Deployments())
        .setFilters({start__gte: start.format(), end__lt: end.format()}));

      $s.weeks = [];
      for (var w = start.clone(); w <= end; w.add(1, 'week')) {
        var week = [];
        for (
            var d = w.clone().startOf('week');
            d <= w.clone().endOf('week');
            d.add(1, 'day')
          ) {
          week.push(d.clone());
          }
        $s.weeks.push(week);
      }

      var navigate = function(new_month) {
        setTimeout(function() {
          location.href = '#/calendar/' + new_month.format('YYYY/MM');
        }, 400);
      };
      $s.forward = function() {
        $s.next = 'right';
        navigate($s.month.clone().add(1, 'month'));
      };
      $s.backward = function() {
        $s.next = 'left';
        navigate($s.month.clone().subtract(1, 'month'));
      };

      $s.deployments.fetch()
        .then(function() {
          $s.clickDay = function(day) {
            var deployment = $s.deployments.getByDay(day) || new M.Deployment();
            var getUrl = function() { return '#/deployment/' + deployment.id + '/collection'; };

            if (deployment.id)
              return (location.href = getUrl());

            deployment
              .set({target: day.format()})
              .save()
              .then(function() { location.href = getUrl(); });
          };
        })
        .catch(error.raise);
    }
  ])
  .controller('DeploymentController', [
    '$q',
    '$rootScope', '$scope', '$routeParams',
    'session', 'error', 'models',
    function ($q, $s_root, $s, $p, session, error, M) {
      error.clear();
      session.load();
      $s_root.header_class = 'under';

      // Define DOM methods.
      $s.editCollection = function(collection) {
        collection.editing = true;
        collection.expanded = true;
      };
      $s.cancelEditingCollection = function(collection) {
        collection.editing = false;
      };
      $s.toggle = function(m) { m.expanded = !m.expanded; };

      // Define and fetch models.
      $s.deployment = (new M.Deployment()).set({id: $p.deployment_id});
      $s.deployment.fetchAll()
        .then(function() {
          // Define utility methods.
          $s.newCollection = function() {
            var collection = new M.Collection();
            collection.editing = collection.expanded = true;
            return (collection.save()
              .then(function() { $s.deployment.collections.models.push(collection); }));
          };

          $s.newStory = function(collection) {
            var story = ((new M.Story())
              .set({collection_id: collection.id}));
            return (story.save()
              .then(function() { $s.deployment.stories.models.push(story); })
              .then(function() { collection.stories.push(story); }));
          };

          $s.newTarget = function(story) {
            var target = ((new M.Target())
              .set({story_id: story.id}));
            return (target.save()
              .then(function() { $s.deployment.targets.models.push(target); })
              .then(function() { story.targets.push(target); }));
          };
        })
        .catch(error.raise);
    }
  ]);
