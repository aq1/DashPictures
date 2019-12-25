const _axios = axios.create({
    baseURL: '/api/',
    timeout: 1000,
    withCredentials: true,
    headers: {
        'xsrfCookieName': 'csrftoken',
        'xsrfHeaderName': 'X-CSRFToken',
    }
});


let app = new Vue({
    el: '#app',
    data: {
        noBoardsMessage: 'No boards found',
        boards: [],
        src: null,
        timer: {
            max: 60,
            promise: null,
            _value: 60,
            value: 100,
            isPaused: true,
        }
    },
    computed: {
        boardsSelected: function () {
            return this.boards.filter(board => board.selected);
        },
        boardsUser: function () {
            return this.boards.filter(board => !board.default);
        },
        boardsDefault: function () {
            return this.boards.filter(board => board.default);
        },
    },
    methods: {
        pause: function () {
            this.timer.isPaused = true;
            clearInterval(this.timer.promise);
        },
        resume: function () {
            this.timer.isPaused = false;
            let view = this;
            clearInterval(this.timer.promise);
            if (!view.src) {
                this.next();
                return;
            }
            this.timer.promise = setInterval(function () {
                if (!view.src || view.timer.isPaused) {
                    return;
                }
                view.timer._value -= 1;
                view.timer.value = 100 * (view.timer._value / view.timer.max);
                if (view.timer._value <= 0) {
                    view.next();
                }
            }, 1000);
        },
        next: function () {
            let view = this;
            this.timer.value = 100;
            this.timer._value = this.timer.max;
            clearInterval(this.timer.promise);

            this.src = null;
            if (!this.boardsSelected) {
                return;
            }
            _axios.get(
                'get_pin/',
                {params: {boards: this.boardsSelected.map(board => board.id)}}).then(
                function (r) {
                    view.src = r.data.image_url;
                    view.resume();
                });

        },
        setTimerMax: function (value) {
            this.timer.max = value;
            this.timer._value = value;
            this.timer.value = 100;
        },
        addTimerMax: function (value) {
            this.timer.max += value;
            this.timer._value += value;
        },
    },
    created: function () {
        let view = this;
        _axios.get('get_boards/').then(
            function (response) {
                view.boards = response.data.data.map(function (board) {
                    board.selected = true;
                    board.pins = [];
                    return board;
                });
                if (view.boards.length) {
                    view.noBoardsMessage = 'No boards found';
                }
            },
            function () {
                console.log('Error getting boards');
            }
        );
    }
});
