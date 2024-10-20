var mix = {
    methods: {
        getSales(page) {
            if(typeof page === "undefined") {
                page = 1
            }
            const PAGE_LIMIT = 20
            this.category = location.pathname.startsWith('/sale/')
            ? Number(location.pathname.replace('/sale/', ''))
            : null

            this.getData("/api/sales/", {
                page,
                limit: PAGE_LIMIT
            }).then(data => {
                this.salesCards = data.salesCards
                this.currentPage = data.currentPage
                this.lastPage = data.lastPage
            })
        },
    },
    mounted() {
        this.getSales();
    },
    data() {
        return {
            salesCards: [],
            pages: 1,
            currentPage: null,
            lastPage: 1,
            // TODO добавить пагинацию
        }
    },
}
