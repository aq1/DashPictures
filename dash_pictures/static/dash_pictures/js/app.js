const _axios = axios.create({
    baseURL: '/dash_pictures/api/',
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
        showMenuMobile: true,
        noBoardsMessage: 'No boards found',
        boardsDownloading: true,
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
            return this.boards.filter(board => !board.predefined);
        },
        boardsDefault: function () {
            return this.boards.filter(board => board.predefined);
        },
    },
    methods: {
        pause: function () {
            this.timer.isPaused = true;
            clearInterval(this.timer.promise);
        },
        resume: function () {
            clearInterval(this.timer.promise);
            if (!this.src) {
                this.next();
                return;
            }
            this.timer.isPaused = false;
            this.showMenuMobile = false;
            const timerStep = 0.1;
            this.timer.promise = setInterval(() => {
                if (!this.src || this.timer.isPaused) {
                    return;
                }
                this.timer._value -= timerStep;
                this.timer.value = 100 * (this.timer._value / this.timer.max);
                if (this.timer._value <= 0) {
                    this.next();
                }
            }, timerStep * 1000);
        },
        next: function () {
            this.timer.value = 100;
            this.timer._value = this.timer.max;
            clearInterval(this.timer.promise);

            this.src = null;
            if (!this.boardsSelected) {
                return;
            }
            _axios.get(
                'get_pin/',
                {params: {boards: this.boardsSelected.map(board => board.id)}}).then(r => {
                    this.src = r.data.image_url;
                    this.resume();
                }, _ => M.toast({html: 'Failed to get a pin'})
            );
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
                    board.selected = !board.predefined;
                    board.pins = [];
                    return board;
                });
                if (view.boards.length) {
                    view.noBoardsMessage = 'No boards found';
                }
            },
            function () {
                M.toast({html: 'Error getting boards'});
            }
        ).finally(function () {
            view.boardsDownloading = false;
        });
    }
});
