<template>
    <div class="col s12 m12 l10" id="content">
        <img :class="{'hide-on-med-and-down': showMenuMobile}"
             v-if="pin.image_url"
             src=""
             :src="pin.image_url"
             id="drawing"
             alt="drawing">
        <div class="row">
            <div class="col s12" v-if="pin.image_url && pin.link">
                    <span>
                        <a :href="pin.link" class="truncate">Source: <i class="material-icons">open_in_new</i></a>
                    </span>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        data() {
            return {
                pin: {}
            }
        },
        components: {}
    }
</script>

<style scoped>
</style>
