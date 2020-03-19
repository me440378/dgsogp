import Vue from 'vue';
import App from './App.vue';
import router from './router';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css'; // 默认主题
// import './assets/css/theme-green/index.css'; // 浅绿色主题
import './assets/css/icon.css';
import './components/common/directives';
import 'babel-polyfill';
import axios from 'axios'
import VueWebsocket from 'vue-websocket'
import VueClipboard from 'vue-clipboard2'

Vue.config.productionTip = false;

/* Vue Clipboard 粘贴板*/
Vue.use(VueClipboard)

/* Vue WebSocket */
Vue.use(VueWebsocket, {
    reconnection: false
});

Vue.use(ElementUI, {
    size: 'small'
});

/* adminMongo */
Vue.prototype.adminMongoUrl = "http://192.168.191.10:8025/app/connection_list"

/* 数据接口 */
Vue.prototype.DataInterfacesBaseUrl = "http://127.0.0.1:8000/api/1.0/datainterfaces/data"

/* HTTP请求 */
var Axios = axios;

Vue.prototype.baseUrl = "http://127.0.0.1:8000/api/1.0"
// Vue.prototype.toParams = function (obj) {
//     var param = ""
//     for(const name in obj) {
//         if(typeof obj[name] != 'function') {
//             param += "&" + name + "=" + encodeURI(obj[name])
//         }
//     }
//     return param.substring(1)
// }

//POST
Vue.prototype.$post=function(api, data){
    var url = this.baseUrl + api
    if (data === undefined){
        data = {}
    }
    return Axios.post(url,data)
}

//GET
Vue.prototype.$get=function(api, data){
    var url = this.baseUrl + api
    if (data === undefined){
        data = {}
    }
    return Axios.get(url, data)
} 

//PUT
Vue.prototype.$put=function(api, data){
    var url = this.baseUrl + api
    if (data === undefined){
        data = {}
    }
    return Axios.put(url, data)
} 

//DELETE
Vue.prototype.$delete=function(api, data){
    var url = this.baseUrl + api
    if (data === undefined){
        data = {}
    }
    return Axios.delete(url,data)
} 



//使用钩子函数对路由进行权限跳转
router.beforeEach((to, from, next) => {
    document.title = `${to.meta.title} | 数据治理系统`;
    const role = localStorage.getItem('userid');
    if (!role && to.path !== '/login') {
        next('/login');
    } else if (to.meta.permission) {
        // 如果是管理员权限则可进入，这里只是简单的模拟管理员权限而已
        role === 'admin' ? next() : next('/403');
    } else {
        // 简单的判断IE10及以下不进入富文本编辑器，该组件不兼容
        if (navigator.userAgent.indexOf('MSIE') > -1 && to.path === '/editor') {
            Vue.prototype.$alert('vue-quill-editor组件不兼容IE10及以下浏览器，请使用更高版本的浏览器查看', '浏览器不兼容通知', {
                confirmButtonText: '确定'
            });
        } else {
            next();
        }
    }
});

new Vue({
    router,
    render: h => h(App)
}).$mount('#app');
