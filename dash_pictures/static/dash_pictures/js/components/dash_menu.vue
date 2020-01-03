<template>
    <div class="col s12 m12 l2" id="menu" :class="{'hide-on-med-and-down': hideComponentSwitch === false}">

        <DashMobileMenuButton :hideComponentSwitch="false"/>
        <DashMenuTimer :boardsSelected="boardsSelected"/>

        <div :class="{hide: boardsUser.length + boardsDefault.length !== 0}">
            <div class="loading">
                <div class="row">
                    <div class="col s12 m12">
                        <span>Getting your boards...</span>
                    </div>
                </div>
                <div class="row">
                    <div class="col s12 m12">
                        <div class="preloader-wrapper small active">
                            <div class="spinner-layer spinner-green-only">
                                <div class="circle-clipper left">
                                    <div class="circle"></div>
                                </div>
                                <div class="gap-patch">
                                    <div class="circle"></div>
                                </div>
                                <div class="circle-clipper right">
                                    <div class="circle"></div>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div>
            <DashMenuBoards :boards="boardsUser"/>
            <DashMenuBoards :boards="boardsDefault"/>
        </div>
    </div>
</template>

<script>
    import DashMenuTimer from './dash_menu_timer';
    import DashMenuBoards from './dash_menu_boards';
    import DashMobileMenuButton from './dash_mobile_menu_button';

    export default {
        props: {
            boardsDefault: Array,
            boardsSelected: Array,
            boardsUser: Array
        },
        data() {
            return {
                hideComponentSwitch: true
            }
        },
        created() {
            Event.$on('menuButtonClicked', (hideComponentSwitch) => {
                this.hideComponentSwitch = hideComponentSwitch;
            });
        },
        components: {
            DashMenuTimer,
            DashMenuBoards,
            DashMobileMenuButton
        }
    }
</script>

<style scoped>
    div#menu {
        border-right: 1px solid #cdcdcd;
        height: 100%;
    }

    @media screen and (max-width: 991px) {
        div#menu {
            border-right: none;
        }
    }

    .loading {
        text-align: center;
    }

</style>
