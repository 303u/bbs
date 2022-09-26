import { createRouter, createWebHashHistory, } from "vue-router";

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: "/",
            component: () => import('@/views/'),
            // 检查是否存在登录token
            beforeEnter() { if (!sessionStorage.getItem("token")) return "/verify"; },
            children: [
                { path: "", redirect() { return { name: "home" } } },
                { path: "home", name: "home", component: () => import('@/views/home/') },
                { path: "about", name: "about", component: () => import('@/views/home/about') },
                { path: "create", name: "create", component: () => import('@/views/home/create') },
                // { path: "search", name: "search", component: () => import('@/views/home/search') },
                { path: "item/:id", name: "item", component: () => import('@/views/home/items'), },
                { path: "rewrite/:id", name: "rewrite", component: () => import('@/views/home/rewrite') },
                {
                    path: "user",
                    component: () => import('@/views/user/'),
                    children: [
                        { path: "", redirect() { return { name: "user" } } },
                        { path: "home", name: "user", component: () => import('@/views/user/home') },
                        { path: "history", name: "history", component: () => import('@/views/user/history') },
                        { path: "security", name: "security", component: () => import('@/views/user/security') },
                    ],
                },
            ],
        },
        {
            path: "/verify",
            component: () => import('@/views/verify/'),
            // 检查是否已登录
            beforeEnter() { if (sessionStorage.getItem("token")) return "/"; },
            children: [
                { path: "", redirect() { return { name: "login" } } },
                { path: "login", name: "login", component: () => import('@/views/verify/login') },
                { path: "regest", name: "regest", component: () => import('@/views/verify/regest') },
                { path: "retrieve", name: "retrieve", component: () => import('@/views/verify/retrieve') },
            ]
        },
        // 无法匹配的路由重定向到首页
        { path: "/:any*", redirect() { return "/" }, },
    ],
})

// 导出路由
export default router;