<template>
    <div>
        <DashMenuTimerProgress/>
        <div class="ctrl-row">
            <div class="row">
                <div class="col s4">
                    <a class="waves-effect waves-teal btn-flat ctrl-btn"
                       :class="{disabled: isPaused}"
                       @click="addTimerMax(10)"
                    >+10s</a>
                </div>
                <div class="col s4">
                    <a class="btn-floating waves-effect waves-teal btn-flat ctrl-btn ctrl-btn-pause"
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
    import DashMenuTimerProgress from './dash_menu_timer_progress';

    export default {
        data() {
            return {
                pinsLoaded: false,
                max: 60,
                promise: null,
                value: 60,
                isPaused: true
            }
        },
        props: {
            boardsSelected: Array
        },
        components: {
            DashMenuTimerProgress
        },
        watch: {
            isPaused() {
                Event.$emit('timerPaused', this.isPaused);
            }
        },
        created() {
            Event.$on(['timerResumed', 'timerNextPressed'], () => {
                Event.$emit('menuButtonClicked', false);
            });
            Event.$on('resumeTimer', _ => {this.resume(true)});
        },
        methods: {
            pause() {
                clearInterval(this.promise);
                this.isPaused = true;
            },
            resume(event, reset=false) {
                Event.$emit('timerResumed');
                if (reset) {
                    this.value = this.max;
                }
                this.isPaused = false;
                clearInterval(this.promise);
                const timerStep = 0.1;
                this.promise = setInterval(() => {
                    if (this.isPaused) {
                        return;
                    }
                    this.value -= timerStep;
                    Event.$emit('progressValueChanged', 100 * (this.value / this.max));
                    if (this.value <= 0) {
                        clearInterval(this.promise);
                        Event.$emit('timerExpired');
                    }
                }, timerStep * 1000);
            },
            next() {
                Event.$emit('timerNextPressed');
                this.value = this.max;
            },
            setTimerMax(max) {
                this.max = max;
                this.value = max;
                Event.$emit('progressValueChanged', 100);
            },
            addTimerMax(value) {
                this.max += value;
                this.value += value;
            },
        }
    }
</script>

<style scoped>
    .ctrl-btn {
        /*width: 100%;*/
        padding: 0;
        margin: 0;
        text-align: center;
    }

    .active {
        color: #26a69a;
    }

    .ctrl-row .ctrl-btn {
        text-transform: none;
    }

    .ctrl-row {
        text-align: center;
    }

    .ctrl-btn-pause:hover {
        background-color: #ececec;
    }

    .ctrl-btn-pause > i {
        border: none;
        color: rgb(52, 52, 52);
    }

</style>
