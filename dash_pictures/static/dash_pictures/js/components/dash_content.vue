<template>
    <div>
        <div class="col s12 m12 l10" id="content" :class="{'hide-on-med-and-down': hideComponentSwitch === true}">
            <div class="menu-button">
                <DashMobileMenuButton :hideComponentSwitch="true"/>
            </div>
                <DashMenuTimerProgress class="hide-on-large-only" />

            <img v-if="pin.image_url"
                 src=""
                 :src="pin.image_url"
                 :style="{'box-shadow': '0 0 30px ' + pin.color}"
                 id="drawing"
                 alt="drawing">
            <div class="row">
                <div class="col s12" v-if="pin.image_url && pin.link">
                    <span>
                        <a :href="pin.link" target="_blank" class="truncate">Source<i
                                class="material-icons">open_in_new</i></a>
                    </span>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    import DashMobileMenuButton from './dash_mobile_menu_button';
    import DashMenuTimerProgress from './dash_menu_timer_progress';

    export default {
        props: {
            boardsSelected: Array
        },
        data() {
            return {
                pin: {},
                hideComponentSwitch: true
            };
        },
        components: {
            DashMobileMenuButton,
            DashMenuTimerProgress
        },
        created() {
            Event.$on('timerResumed', () => {
                if (!this.pin.image_url) {
                    this.getPin();
                }
            });
            Event.$on(['timerNextPressed', 'timerExpired'], this.getPin);
            Event.$on('menuButtonClicked', (hideComponentSwitch) => {
                this.hideComponentSwitch = hideComponentSwitch
            });
        },
        methods: {
            getPin() {
                axios.get(
                    'get_pin/',
                    {params: {boards: this.boardsSelected.map(board => board.id)}}).then(r => {
                        this.pin = r.data;
                        Event.$emit('resumeTimer');
                    }, _ => M.toast({html: 'Failed to get a pin'})
                );
            }
        }
    }
</script>

<style scoped>
    #content {
        text-align: center;
        align-items: center;
        height: 90vh;
        /*line-height: ;*/
        justify-content: center;
    }

    #content #drawing {
        box-shadow: 0 10px 10px 0 rgba(0, 0, 0, 0.2);
        max-width: 90%;
        max-height: 90%;
        vertical-align: middle;
    }

    .menu-button {
        float: left;
    }
</style>
