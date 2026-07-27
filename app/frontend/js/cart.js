// app/frontend/js/cart.js

import { api } from './api.js';

export class CartService {
    async getCart() {
        try {
            const cart = await api.get('/cart');
            return cart;
        } catch (error) {
            console.error('Ошибка загрузки корзины:', error);
            throw error;
        }
    }

    async getCartItems() {
        try {
            const items = await api.get('/cart/get_all');
            return items;
        } catch (error) {
            console.error('Ошибка загрузки товаров корзины:', error);
            throw error;
        }
    }

    async addToCart(productId, cartId, quantity = 1) {
        try {
            const result = await api.post('/cart/add', {
                product_id: productId,
                cart_id: cartId,
                quantity: quantity
            });
            return result;
        } catch (error) {
            console.error('Ошибка добавления в корзину:', error);
            throw error;
        }
    }

    async removeFromCart(productId) {
        try {
            await api.delete(`/cart/del/${productId}`);
        } catch (error) {
            console.error('Ошибка удаления из корзины:', error);
            throw error;
        }
    }

    async clearCart() {
        try {
            await api.delete('/cart/clear_cart');
        } catch (error) {
            console.error('Ошибка очистки корзины:', error);
            throw error;
        }
    }

    async checkout() {
        try {
            const order = await api.post('/orders/create_order');
            return order;
        } catch (error) {
            console.error('Ошибка оформления заказа:', error);
            throw error;
        }
    }

    getTotalPrice(items) {
        if (!items || items.length === 0) return 0;
        return items.reduce((total, item) => {
            // Цена товара не возвращается в CartItemReturn, нужно запросить отдельно
            return total + (item.price || 0) * item.quantity;
        }, 0);
    }

    getTotalItems(items) {
        if (!items || items.length === 0) return 0;
        return items.reduce((total, item) => total + item.quantity, 0);
    }
}

export const cartService = new CartService();