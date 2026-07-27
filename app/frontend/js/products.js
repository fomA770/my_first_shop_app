// app/frontend/js/products.js

import { api } from './api.js';

export class ProductsService {
    async getProducts(filters = {}, skip = 0, limit = 100) {
        try {
            let endpoint = `/products/get_all?skip=${skip}&limit=${limit}`;
            
            if (filters.category) endpoint += `&category=${encodeURIComponent(filters.category)}`;
            if (filters.min_price) endpoint += `&min_price=${filters.min_price}`;
            if (filters.max_price) endpoint += `&max_price=${filters.max_price}`;
            if (filters.in_stock) endpoint += `&in_stock=true`;
            
            const products = await api.get(endpoint);
            return products;
        } catch (error) {
            console.error('Ошибка загрузки товаров:', error);
            throw error;
        }
    }

    async createProduct(productData) {
        try {
            const product = await api.post('/products/create', productData);
            return product;
        } catch (error) {
            console.error('Ошибка создания товара:', error);
            throw error;
        }
    }

    async updateProduct(productId, productData) {
        try {
            const product = await api.put(`/products/update/${productId}`, productData);
            return product;
        } catch (error) {
            console.error('Ошибка обновления товара:', error);
            throw error;
        }
    }

    async deleteProduct(productId) {
        try {
            await api.delete(`/products/del/${productId}`);
        } catch (error) {
            console.error('Ошибка удаления товара:', error);
            throw error;
        }
    }

    async bulkCreate(products) {
        try {
            const result = await api.post('/products/create_many', { products });
            return result;
        } catch (error) {
            console.error('Ошибка массового создания:', error);
            throw error;
        }
    }
}

export const productsService = new ProductsService();