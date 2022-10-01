import { createRouter, createWebHashHistory, } from "vue-router";

const router = createRouter({
    history: createWebHashHistory(),
    routes: [
        {
            path: "/",
            component: () => import('@/views/'),
            // 检查是否存在登录token
            beforeEnter() { if (!sessionStorage["token"] && !localStorage["token"]) return "/verify"; },
            children: [
                { path: "", redirect() { return { name: "home" } } },
                { path: "home", name: "home", component: () => import('@/views/home/') },
                { path: "search/:keyword?", name: "search", component: () => import('@/views/home/search') },
                { path: "item/:id", name: "item", component: () => import('@/views/home/items'), },
                { path: "write/:id?", name: "write", component: () => import('@/views/home/write') },
                { path: "about", name: "about", component: () => import('@/views/home/about') },
                {
                    path: "user",
                    component: () => import('@/views/user/'),
                    children: [
                        { path: "", redirect() { return { name: "user" } } },
                        { path: "home", name: "user", component: () => import('@/views/user/home') },
                        { path: "security", name: "security", component: () => import('@/views/user/security') },
                    ],
                },
            ],
        },
        {
            path: "/verify",
            component: () => import('@/views/verify/'),
            // 检查是否存在登录token
            beforeEnter() { if (sessionStorage["token"] || localStorage["token"]) return "/"; },
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