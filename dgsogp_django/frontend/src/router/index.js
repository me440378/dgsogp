import Vue from 'vue';
import Router from 'vue-router';

Vue.use(Router);

export default new Router({
    routes: [
        {
            path: '/',
            redirect: '/dashboard'
        },
        {
            path: '/',
            component: () => import(/* webpackChunkName: "home" */ '../components/common/Home.vue'),
            meta: { title: '自述文件' },
            children: [
                {
                    path: '/dashboard',
                    component: () => import(/* webpackChunkName: "dashboard" */ '../components/pages/Dashboard.vue'),
                    meta: { title: '系统首页' }
                },
                {
                    path: '/users',
                    component: () => import(/* webpackChunkName: "users" */ '../components/pages/UsersManage.vue'),
                    meta: { title: '用户管理' }
                },
                {
                    path: '/datasources',
                    component: () => import(/* webpackChunkName: "datasources" */ '../components/pages/DatasourcesManage.vue'),
                    meta: { title: '数据源管理' }
                },
                {
                    path: '/hadoopsources',
                    component: () => import(/* webpackChunkName: "hadoopsources" */ '../components/pages/HadoopsourcesManage.vue'),
                    meta: { title: 'Hadoop源管理' }
                },
                {
                    path: '/metadata',
                    component: () => import(/* webpackChunkName: "metadata" */ '../components/pages/MetadataManage.vue'),
                    meta: { title: '元数据管理' }
                },
                {
                    path: '/datainterfaces',
                    component: () => import(/* webpackChunkName: "datainterfaces" */ '../components/pages/DatainterfacesManage.vue'),
                    meta: { title: '数据接口管理' }
                },
                {
                    path: '/databaseinterfaces',
                    component: () => import(/* webpackChunkName: "databaseinterfaces" */ '../components/pages/DatabaseinterfacesManage.vue'),
                    meta: { title: '数据库接口管理' }
                },
                {
                    path: '/databasecommandline',
                    component: () => import(/* webpackChunkName: "databasecommandline" */ '../components/pages/DatabaseCommandLine.vue'),
                    meta: { title: '数据库接口操作' }
                },
                {
                    path: '/messages',
                    component: () => import(/* webpackChunkName: "messages" */ '../components/pages/MessagesManage.vue'),
                    meta: { title: '通知管理' }
                },
                {
                    // 权限页面
                    path: '/permission',
                    component: () => import(/* webpackChunkName: "permission" */ '../components/page/Permission.vue'),
                    meta: { title: '权限测试', permission: true }
                },
                {
                    path: '/404',
                    component: () => import(/* webpackChunkName: "404" */ '../components/page/404.vue'),
                    meta: { title: '404' }
                },
                {
                    path: '/403',
                    component: () => import(/* webpackChunkName: "403" */ '../components/page/403.vue'),
                    meta: { title: '403' }
                },
            ]
        },
        {
            path: '/login',
            component: () => import(/* webpackChunkName: "login" */ '../components/pages/Login.vue'),
            meta: { title: '登录' }
        },
        {
            path: '*',
            redirect: '/404'
        }
    ]
});
