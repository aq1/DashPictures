<template>
    <div class="row">
        <div class="col s12 m12">
            <div class="progress" :class="{disabled: isPaused}">
                <div class="determinate" style="width: 100%" :style="{width: valuePercent + '%'}"></div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                isPaused: true,
                valuePercent: 100
            }
        },
        created() {
            Event.$on('timerValueChanged', valuePercent => {
                this.valuePercent = valuePercent;
            });
            Event.$on('timerPaused', isPaused => {
                this.isPaused = isPaused;
            })
        }
    }
</script>

<style scoped>
    .progress.disabled > div.determinate {
        background-color: #787878;
    }
</style>