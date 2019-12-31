<template>
    <div class="row">
        <!--        <dash-mobile-menu-button></dash-mobile-menu-button>-->
        <!--        <dash-mobile-progress></dash-mobile-progress>-->
        <DashMenu/>
        <DashContent/>
    </div>
</template>

<script>
    // import DashMobileMenuButton from './dash_mobile_menu_button';
    // import DashMobileProgress from './dash_mobile_menu_button';
    import DashMenu from './dash_menu';
    import DashContent from './dash_content';

    export default {
        data() {
            return {}
        },
        components: {
            DashMenu,
            DashContent
        }
    }
</script>

<style>

</style>
