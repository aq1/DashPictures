<template>
    <div>
        <div class="row">
            <div class="col s12 m12">
                <div class="progress" :class="{disabled: isPaused}">
                    <div class="determinate" style="width: 100%" :style="{width: value + '%'}"></div>
                </div>
            </div>
        </div>
        <div class="ctrl-row">
            <div class="row">
                <div class="col s4">
                    <a class="waves-effect waves-teal btn-flat ctrl-btn"
                       :class="{disabled: isPaused}"
                       @click="addTimerMax(10)"
                    >+10s</a>
                </div>
                <div class="col s4">
                    <a class="waves-effect waves-teal btn-flat ctrl-btn"
                       v-if="!isPaused"
                       @click="pause">
                        <i class="material-icons">pause</i>
                    </a>
                    <a class="btn-floating ctrl-btn"
                       v-if="isPaused"
                       :class="{disabled: !boardsSelected.length, pulse: boardsSelected.length}"
                       @click="resume">
                        <i class="material-icons">play_arrow</i>
                    </a>
                </div>
                <div class="col s4">
                    <a class="waves-effect waves-teal btn-flat ctrl-btn"
                       @click="next"
                       :class="{disabled: isPaused || !boardsSelected.length, pulse: boardsSelected.length}">
                        <i class="material-icons">fast_forward</i>
                    </a>
                </div>
            </div>
            <div class="row">
                <div class="col s4">
                    <a class="waves-effect waves-teal btn-flat ctrl-btn"
                       :class="{active: max === 30}"
                       @click="setTimerMax(30)">
                        30s
                    </a>
                </div>
                <div class="col s4">
                    <a class="waves-effect waves-teal btn-flat ctrl-btn"
                       :class="{active: max === 60}"
                       @click="setTimerMax(60)">
                        1m
                    </a>
                </div>
                <div class="col s4">
                    <a class="waves-effect waves-teal btn-flat ctrl-btn"
                       :class="{active: max === 120}"
                       @click="setTimerMax(120)">
                        2m
                    </a>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                max: 60,
                promise: null,
                _value: 60,
                value: 100,
                isPaused: true,
            }
        },
        props: {
            boardsSelected: Array
        },
        methods: {
            pause() {
                this.isPaused = true;
                this.$emit('timerPaused');
            },
            resume() {
                this.isPaused = false;
                this.$emit('timerResumed');
                const timerStep = 0.1;
                this.promise = setInterval(() => {
                    if (this.isPaused) {
                        return;
                    }
                    this._value -= timerStep;
                    this.value = 100 * (this._value / this.max);
                    if (this._value <= 0) {
                        clearInterval(this.promise);
                        this.$emit('timerExpired');
                    }
                }, timerStep * 1000);
            },
            next() {
                this.$emit('timerNextPressed');
            },
            setTimerMax(value) {
                this.max = value;
                this._value = value;
                this.value = 100;
            },
            addTimerMax(value) {
                this.max += value;
                this._value += value;
            },
        },
        components: {}
    }
</script>

<style scoped>
    .progress.disabled > div.determinate {
        background-color: #787878;
    }

    .ctrl-btn {
        /*width: 100%;*/
        padding: 0;
        margin: 0;
        text-align: center;
    }

    .ctrl-btn.active {
        color: #26a69a;
    }

    .ctrl-row .ctrl-btn {
        text-transform: none;
    }

    .ctrl-row {
        text-align: center;
    }
</style>
