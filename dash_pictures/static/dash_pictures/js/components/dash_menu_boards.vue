<template>
    <div id="boards">
        <div v-if="boards.length">
            <div class="row">
                <div class="col s12 m12">
                    <div class="border-wrap">
                        <div class="border"></div>
                    </div>
                </div>
            </div>
            <div class="row" v-for="board in boards">
                <div class="col s12 m12 board-label-div">
                    <label>
                        <input type="checkbox" v-model="board.selected">
                        <span>{{ board.name }}</span>
                    </label>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
    export default {
        props: {
            boards: Array
        }
    }
</script>

<style scoped>
    label {
        cursor: pointer !important;
        width: 100%;
    }

    div.border-wrap > div.border {
        width: 90%;
        display: inline-block;
        border-top: 1px solid #a9a9a9;
    }

    div.border-wrap {
        text-align: center;
        width: 100%;
    }

    .board-label-div label {
        display: inline-block;
    }

    @media screen and (max-width: 991px) {
        .board-label-div {
            text-align: center;
        }
    }
</style>
