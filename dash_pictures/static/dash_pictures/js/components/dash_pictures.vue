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
                localStorage.boards = JSON.stringify(this.boards);
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
            if (localStorage.boards) {
                this.boards = JSON.parse(localStorage.boards);
                return;
            }

            axios.get('get_boards/', {timeout: 10000}).then(
                response => {
                    this.boards = response.data.data;
                    if (this.boards.length) {
                        this.boards[0].selected = true;
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
