// app/frontend/js/auth.js

import { api } from './api.js';

export class AuthService {
    constructor() {
        this.currentUser = null;
        this.isAuthenticated = false;
        this.listeners = [];
    }

    addListener(callback) {
        this.listeners.push(callback);
    }

    notifyListeners() {
        this.listeners.forEach(callback => callback(this.isAuthenticated, this.currentUser));
    }

    async register(userData) {
        try {
            const response = await api.post('/auth/register', userData);
            this.currentUser = response;
            this.isAuthenticated = true;
            this.notifyListeners();
            return response;
        } catch (error) {
            throw error;
        }
    }

    async login(email, password) {
        try {
            const formData = new URLSearchParams();
            formData.append('username', email);
            formData.append('password', password);

            const response = await fetch('/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                },
                credentials: 'include',
                body: formData
            });

            if (!response.ok) {
                const error = await response.json();
                throw new Error(error.detail || 'Ошибка входа');
            }

            const userData = await response.json();
            this.currentUser = userData;
            this.isAuthenticated = true;
            this.notifyListeners();
            return userData;
        } catch (error) {
            throw error;
        }
    }

    logout() {
        this.currentUser = null;
        this.isAuthenticated = false;
        document.cookie = 'access_token=; Max-Age=0; path=/;';
        this.notifyListeners();
        window.location.href = '/';
    }

    checkAuth() {
        const cookies = document.cookie.split(';');
        const hasToken = cookies.some(cookie => cookie.trim().startsWith('access_token='));
        this.isAuthenticated = hasToken;
        return this.isAuthenticated;
    }

    getCurrentUser() {
        return this.currentUser;
    }

    async loadCurrentUser() {
        try {
            // Получаем пользователя из токена (если есть эндпоинт /auth/me)
            // Пока просто проверяем авторизацию
            this.checkAuth();
            return this.currentUser;
        } catch (error) {
            console.error('Ошибка загрузки пользователя:', error);
            return null;
        }
    }
}

export const authService = new AuthService();