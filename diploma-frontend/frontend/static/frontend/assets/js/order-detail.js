var mix = {
    methods: {
        getOrder(orderId) {
            this.getData(`/api/orders/active/`).then(data => {
                this.orderId = data.id
                this.createdAt = data.createdAt
                this.fullName = data.fullName
                this.phone = data.phone
                this.email = data.email
                this.deliveryType = data.deliveryType
                this.city = data.city
                this.address = data.address
                this.paymentType = data.paymentType
                this.status = data.status
                this.totalCost = data.totalCost
                this.products = data.products
                if (typeof data.paymentError !== 'undefined'){
                    this.paymentError = data.paymentError
                }
            })
        },
        confirmOrder() {
            if (this.order) {
                this.postData('/api/orders/' + this.order.id + '/', {
                   ...this.order
                })
                    .then(() => {
                        alert('Заказ подтвержден')
                        if (this.order.paymentType === 'Онлайн картой')
                        {location.replace('/payment/')}
                        else (location.replace('/payment-someone/'))
                    })
                    .catch(() => {
                        console.warn('Ошибка при подтверждения заказа')
                    })
            }
        },
        getOrderDetails() {
            const orderId = location.pathname.startsWith('/order-detail/')
            ? Number(location.pathname.replace('/order-detail/', ''))
            : null
            this.getData(`/api/orders/${orderId}/`).then(data => {
                this.orderId = data.id
                this.createdAt = data.createdAt
                this.fullName = data.fullName
                this.phone = data.phone
                this.email = data.email
                this.deliveryType = data.deliveryType
                this.city = data.city
                this.address = data.address
                this.paymentType = data.paymentType
                this.status = data.status
                this.totalCost = data.totalCost
                this.products = data.products
                if (typeof data.paymentError !== 'undefined'){
                    this.paymentError = data.paymentError
                }
            })
        },
    },
    mounted() {
        // this.getOrder(pk);
        this.getOrderDetails()


    },
    data() {
        return {
            orderId: null,
            createdAt: null,
            fullName: null,
            phone: null,
            email: null,
            deliveryType: null,
            city: null,
            address: null,
            paymentType: null,
            status: null,
            totalCost: null,
            products: [],
            paymentError: null,
        }
    },
}
