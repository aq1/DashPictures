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
                <label class="board-label">
                    <div class="col s12 m12">
                        <input type="checkbox" v-model="board.selected">
                        <span>{{ board.name }}</span>
                    </div>
                </label>
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
</style>
