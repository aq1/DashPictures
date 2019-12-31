<template>
    <div id="boards">
        <div v-if="boardsDownloading">
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
        <DashMenuBoardsList boards="boardsUser"/>
        <DashMenuBoardsList boards="boardsDefault"/>
    </div>
</template>

<script>
    import DashMenuBoardsList from './dash_menu_boards_list';

    export default {
        data() {
            return {
                boards: [],
                boardsDownloading: true,
            }
        },
        components: {
            DashMenuBoardsList
        },
        computed: {
            boardsSelected() {
                return this.boards.filter(board => board.selected);
            },
            boardsUser() {
                return this.boards.filter(board => !board.predefined);
            },
            boardsDefault() {
                return this.boards.filter(board => board.predefined);
            }
        },
        created() {
            axios.get('get_boards/', {timeout: 10000}).then(
                response => {
                    this.boards = response.data.data.map(function (board) {
                        board.selected = !board.predefined;
                        board.pins = [];
                        return board;
                    });
                    if (this.boards.length) {
                        this.noBoardsMessage = 'No boards found';
                    }
                },
                function () {
                    M.toast({html: 'Error getting boards'});
                }
            ).finally(() => {
                this.boardsDownloading = false;
            });
        },
        components: {}
    }
</script>

<style scoped>
    .board-label {
        cursor: pointer !important;
    }

    div.border-wrap {
        text-align: center;
        width: 100%;
    }

    div.border-wrap > div.border {
        width: 90%;
        display: inline-block;
        border-top: 1px solid #a9a9a9;
        /*padding-top: 10px;*/
    }

    .loading {
        text-align: center;
    }

    .collection-item {
        background-color: inherit;
        bordedr-color: #cdcdcd;
    }
</style>
