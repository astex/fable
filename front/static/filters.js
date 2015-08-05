angular.module('filters', [])
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
