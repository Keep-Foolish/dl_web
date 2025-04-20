import { createApp, reactive } from 'vue'

import myLoad from '../components/loading.vue'

const msg = reactive({
    show: false,
    title: '加载中...'
})

const $loading = createApp(myLoad, { msg }).mount(document.createElement('div'))
const load = {
    show(title = msg.title) { // 控制显示loading的方法
        msg.show = true
        msg.title = title
        document.body.appendChild($loading.$el)
    },

    hide() { // 控制loading隐藏的方法
        msg.show = false
    }
}
export { load }

// 在需要使用时调用show方法
// 例如在指定api调用，或者其他耗时操作时打开loading
// 不传参默认为 加载中...
// load.show();
// load.show('登录中...');

//在加载完成时关闭
// load.hide();
