<template>
    <div id="boards">
        <div v-if="boards.length">
            <div class="row boards-header" @click="hideBoards = !hideBoards">
                <div class="col s12 m12">
                    <i class="material-icons" v-if="!hideBoards">arrow_drop_up</i>
                    <i class="material-icons" v-if="hideBoards">arrow_drop_down</i>
                    <span v-if="isDefault">Predefined boards</span>
                    <span v-if="!isDefault">My boards</span>
                </div>
            </div>
            <div class="row board-row" v-for="board in boards" v-if="!hideBoards">
                <div class="col s12 m12">
                    <label class="truncate">
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
        data() {
            return {
                hideBoards: false
            }
        },
        props: {
            boards: Array
        },
        computed: {
            isDefault() {
                for (const board of this.boards) {
                    if (!board.predefined) {
                        return false;
                    }
                }
                return true;
            }
        }
    }
</script>

<style scoped>
    div#boards,
    div.board-row *,
    i.material-icons {
        font-size: 16px;
    }

    label {
        cursor: pointer !important;
        width: 100%;
    }

    .board-row label {
        display: inline-block;
    }

    .boards-header,
    .board-row {
        padding: 5px 0;
        cursor: pointer;
        margin-bottom: 0;
    }

    .boards-header:hover,
    .board-row:hover {
        background-color: #f2f2f2;
    }
</style>
