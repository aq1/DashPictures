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
        <DashMenuTimer :boardsSelected="boardsSelected"/>
        <div>
            <DashMenuBoards :boards="boardsUser"/>
            <DashMenuBoards :boards="boardsDefault"/>
        </div>
    </div>
</template>

<script>
    import DashMenuTimer from './dash_menu_timer';
    import DashMenuBoards from './dash_menu_boards';

    export default {
        data() {
            return {
                boards: [],
                boardsDownloading: true,
                showMenuMobile: false
            }
        },
        components: {
            DashMenuTimer,
            DashMenuBoards
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
