<template>
    <div class="col s12 m12 l2" id="menu">
<!--    <div class="col s12 m12 l2" id="menu" :class="{'hide': !showMenuMobile}">-->
        <div class="row">
            <div class="col s12 m12 hide-on-large-only">
                <a class="waves-effect waves-teal btn-flat" @click="showMenuMobile = false">
                    <i class="material-icons">menu</i>
                </a>
            </div>
        </div>
        <dash-menu-timer></dash-menu-timer>
        <dash-menu-boards></dash-menu-boards>
    </div>
</template>

<script>
    import DashMenuTimer from './dash_menu_timer';
    import DashMenuBoards from './dash_menu_boards';

    export default {
        data() {
            return {
                showMenuMobile: false
            }
        },
        components: {
            DashMenuTimer,
            DashMenuBoards
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
</style>
