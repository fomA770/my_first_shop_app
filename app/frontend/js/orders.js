// app/frontend/js/orders.js

import { api } from './api.js';

export class OrdersService {
    async getOrders() {
        try {
            const orders = await api.get('/orders/user_orders');
            return orders;
        } catch (error) {
            console.error('Ошибка загрузки заказов:', error);
            throw error;
        }
    }

    async updateOrderStatus(orderId, status) {
        try {
            const result = await api.put('/orders/update_status', {
                order_id: orderId,
                status: status
            });
            return result;
        } catch (error) {
            console.error('Ошибка обновления статуса заказа:', error);
            throw error;
        }
    }

    getStatusText(status) {
        const statusMap = {
            'pending': '⏳ Ожидает',
            'processing': '🔄 В обработке',
            'shipped': '🚚 Отправлен',
            'delivered': '✅ Доставлен',
            'cancelled': '❌ Отменен'
        };
        return statusMap[status] || status;
    }

    getStatusColor(status) {
        const colorMap = {
            'pending': '#f39c12',
            'processing': '#3498db',
            'shipped': '#9b59b6',
            'delivered': '#27ae60',
            'cancelled': '#e74c3c'
        };
        return colorMap[status] || '#95a5a6';
    }
}

export const ordersService = new OrdersService();