<template>
    <div class="col s12 m12 left hide-on-large-only">
        <a class="waves-effect waves-teal btn-flat" @click="click">
            <i class="material-icons">menu</i>
        </a>
    </div>
</template>

<script>
    export default {
        created() {
            Event.$on(['timerResumed', 'timerNextPressed'], () => {
                Event.$emit('menuButtonClicked', false);
            });

        },
        props: {
            hideComponentSwitch: Boolean
        },
        methods: {
            click() {
                Event.$emit('menuButtonClicked', this.hideComponentSwitch);
            }
        }
    }
</script>

<style scoped>
</style>
