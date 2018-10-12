var app = angular.module('pinterestApp', []);


app.config(['$httpProvider', function($httpProvider) {
    $httpProvider.defaults.useXDomain = true;
    $httpProvider.defaults.xsrfCookieName = "csrftoken";
    $httpProvider.defaults.xsrfHeaderName = "X-CSRFToken";
    $httpProvider.defaults.withCredentials = true;
}]);



app.controller('BodyCtrl', ['$scope', '$http', '$interval', function($scope, $http, $interval) {

    window.pinterestScope = $scope;
    $scope.boards = [];
    $scope.drawingStarted = false;
    $scope.pictureSrc = null;
    $scope.noBoardsMessage = 'Loading boards...';
    $scope.timer = {
        promise: null,
        max: 60,
        _value: 0,
        value: 1,
    };

    $scope.toggleBoard = function(board) {
        board.selected = !board.selected;
    };

    $scope.startButtonDisabled = function() {
        return !Boolean($scope.boards.filter(board => board.selected).length);
    };

    var resetTimer = function() {
        $scope.timer._value = 0;
        $scope.timer.value = 1;
    };

    setTimer = function(seconds) {
        $scope.timer._value = seconds;
        $scope.timer.value = Math.min(
            1 - ($scope.timer._value / $scope.timer.max),
            $scope.timer.max
        );
        console.log(seconds);
    };

    $scope.setTimerMax = function(seconds) {
        $scope.timer.max = seconds;
        setTimer(0);
    };

    $scope.startTimer = function() {
        $scope.timer.promise = $interval(function() {
            if ($scope.timer._value == $scope.timer.max) {
                $scope.nextPicture();
                return;
            }
            setTimer($scope.timer._value + 1);
        }, 1000);
        $scope.timer.isPaused = false;
    };

    $scope.pauseTimer = function() {
        $interval.cancel($scope.timer.promise);
        $scope.timer.isPaused = true;
    };

    $scope.toggleTimer = function() {
        $scope.drawingStarted = !$scope.drawingStarted;
        if ($scope.drawingStarted) {
            $scope.nextPicture();
        } else {
            $interval.cancel($scope.timer.promise);
        }
    };

    $scope.nextPicture = function() {
        $interval.cancel($scope.timer.promise);
        resetTimer();
        var boardIds = [];
        for (var i = 0; i < $scope.boards.length; i++) {
            if (!$scope.boards[i].selected) {
                continue;
            }
            boardIds.push($scope.boards[i].id);
        }
        $http.get('/api/get_pin/', {params: {boards_ids: boardIds}}).then(function(r) {
            $scope.pictureSrc = r.data.image_url;
            $scope.startTimer();
        });
    };

    $scope.addToTimer = function(seconds) {
        var _value = Math.max(0, $scope.timer.value -= seconds);
        setTimer(_value);
    };

    $http.get('/api/get_boards/').then(function(r) {
        $scope.boards = r.data.data.map(function(board) {
            board.selected = true;
            board.pins = [];
            return board;
        });
        if (!$scope.boards.length) {
            $scope.noBoardsMessage = 'No boards found';
        }
    });
}]);
