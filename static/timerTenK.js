/*global angular:false, $scope:false, console:false */
var app = angular.module('timerTenK', []);
 
app.config(['$interpolateProvider', function ($interpolateProvider) {
    $interpolateProvider.startSymbol('{[');
    $interpolateProvider.endSymbol(']}');
}]);

app.controller('firstController', ['$scope', '$http', function ($scope, $http) {
    $scope.visible = false;

    $scope.getKeys = function (jsonData) {

        var keys = [];
        for (var i=0; i < jsonData.length; i++){
            keys.push(Object.keys(jsonData[i])[0]);
        };
        return keys;
    };
    
  $scope.getSkill = function(skillName, jsonData){
      for (var i=0; i < jsonData.length; i++){
          if (Object.keys(jsonData[i])[0] == skillName)
          {
              $scope.skill_todo = jsonData[i][skillName]
              $scope.skill_in_use = skillName;
              $scope.visible = true;
          }
      }
  };
    
    
    $scope.addSkill = function () {
        var newSkill = $scope.newSkill.trim();
        var obj = JSON.parse('{ "' + newSkill + '": []}');

        if (!newSkill) {
            return;
        }

        for (var i=0; i < $scope.existingUser.skills.length; i++){
            if (Object.keys($scope.existingUser.skills[i])[0] == newSkill){
                return;
                }
            }
        
        $scope.existingUser.skills.push(obj);
        
        $http({
            method: "post",
            url: "/test_user/add_skill",
            headers: {'Content-Type': "application/json"},
            data: obj
        }).success(function () {
            console.log("success!");
        });

        $scope.newSkill = '';
    };

  $scope.addTodo = function () {
      var newTodo = $scope.newTodo.trim();
      var obj = JSON.parse('{"newTodo": "' + newTodo + '", "skill_in_use": "' + $scope.skill_in_use + '"}')
      
        if (!newTodo) {
            return;
        }
        $scope.skill_todo.push(newTodo)
        
        $http({
            method: "post",
            url: "/test_user/add_todo",
            headers: {'Content-Type': "application/json"},
            data: obj
        }).success(function () {
            console.log("success!");
        });
        
        $scope.newTodo = '';
    };
    
//    TODO: pop up check for removal yes/no
    $scope.removeSkill = function (skill) {
        for (var i=0; i < $scope.existingUser.skills.length; i++){
            if (Object.keys($scope.existingUser.skills[i])[0] == skill){
                $scope.existingUser.skills.splice(i, 1)
            $http({
                method: "post",
                url: "/test_user/remove_skill",
                headers: {'Content-Type': "application/json"},
                data: skill
            }).success(function () {
                console.log("success!");
            });
            if ($scope.skill_in_use == skill){
                $scope.skill_in_use = ''
                $scope.skill_todo = ''

            }
                  }
        }
    };
    
    $scope.removeTodo = function (todo) {
        var obj = JSON.parse('{"Todo": "' + todo + '", "skill_in_use": "' + $scope.skill_in_use + '"}')
        $scope.skill_todo.splice($scope.skill_todo.indexOf(todo), 1)
        $http({
            method: "post",
            url: "/test_user/remove_todo",
            headers: {'Content-Type': "application/json"},
            data: obj
        }).success(function () {
            console.log("success!");
        });
    };
}]);
