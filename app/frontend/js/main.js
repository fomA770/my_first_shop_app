// app/frontend/js/main.js

import { authService } from './auth.js';
import { productsService } from './products.js';
import { cartService } from './cart.js';
import { ordersService } from './orders.js';
import { api } from './api.js';

// Делаем сервисы глобальными
window.authService = authService;
window.productsService = productsService;
window.cartService = cartService;
window.ordersService = ordersService;
window.api = api;

// Обновление навигации
export function updateNavigation() {
    const navAuth = document.getElementById('navAuth');
    if (!navAuth) return;

    const user = authService.getCurrentUser();

    if (authService.isAuthenticated && user) {
        navAuth.innerHTML = `
            <span class="user-name">👤 ${user.full_name}</span>
            <button onclick="window.authService.logout()" class="btn btn-danger btn-sm">Выйти</button>
        `;
    } else {
        navAuth.innerHTML = `
            <button onclick="window.location.href='/'">Войти</button>
            <button onclick="window.location.href='/'">Регистрация</button>
        `;
    }
}

// Toast уведомления
export function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.textContent = message;
    toast.className = `toast ${type}`;
    toast.classList.remove('hidden');
    
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

// Проверка авторизации для защищенных страниц
export function requireAuth() {
    if (!authService.checkAuth()) {
        window.location.href = '/';
        return false;
    }
    return true;
}

document.addEventListener('DOMContentLoaded', async () => {
    console.log('🚀 Приложение загружено');
    
    // Проверяем авторизацию
    const isAuth = authService.checkAuth();
    
    if (isAuth) {
        try {
            await authService.loadCurrentUser();
            console.log('👤 Пользователь авторизован');
        } catch (error) {
            console.error('Ошибка загрузки пользователя:', error);
        }
    }
    
    // Обновляем навигацию
    updateNavigation();
    
    // Глобальная функция для выхода
    window.logout = function() {
        authService.logout();
    };
    
    // Глобальная функция для тостов
    window.showToast = showToast;
});

// Экспортируем для использования в других модулях
export { authService, productsService, cartService, ordersService, api };