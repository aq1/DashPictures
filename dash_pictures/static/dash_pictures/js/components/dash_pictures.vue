<template>
    <div class="row">
        <DashMenu :boardsSelected="boardsSelected" :boardsUser="boardsUser" :boardsDefault="boardsDefault"/>
        <DashContent :boardsSelected="boardsSelected"/>
    </div>
</template>

<script>
    import DashMenu from './dash_menu';
    import DashContent from './dash_content';

    export default {
        data() {
            return {
                boards: [],
                pin: []
            }
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
        components: {
            DashMenu,
            DashContent
        }
    }
</script>

<style>

</style>
