<template>
    <div style="height: 100%;">
        <n-layout style="height: 100%">
            <n-layout-header bordered class="n-layout-header-title">
                <div class="header-content">
                    <!-- 左侧标题 -->
                    <h2 class="header-title">稻麦倒伏检测平台</h2>

                    <!-- 右侧SVG图标 -->
                    <span class="header-right-button">
                        <n-button circle size="large" @click="goToPage('Home')">
                            <template #icon>
                                <svg t="1744429374794" class="icon" viewBox="0 0 1024 1024" version="1.1"
                                    xmlns="http://www.w3.org/2000/svg" p-id="5461" width="48" height="48">
                                    <path
                                        d="M1017.295381 515.625294c-8.918711 9.05797-23.377057 9.05797-32.295768 0L755.083237 303.3395c-1.513416-1.206227-2.807704-2.525091-3.989357-4.056938l-89.551638-90.944226c-1.513416-1.200084-2.807704-2.512803-3.989357-4.050794L512.000756 56.462215 38.999851 515.625294c-8.918711 9.05797-23.377057 9.05797-32.29372 0-8.918711-9.05797-8.918711-23.73954 0-32.797509L493.065647 10.095158c0.77002-1.130454 1.234898-2.394024 2.224046-3.405698 4.603734-4.677459 10.67583-6.829828 16.711063-6.682377 6.033185-0.147451 12.105281 2.004918 16.709015 6.682377 0.989147 1.011675 1.454026 2.275244 2.224046 3.405698l121.376383 123.262521L652.3102 71.16836c0 0-0.002048 0-0.002048-0.006144 0-13.114908 10.471037-23.751827 23.385249-23.751827l93.538947 0c6.459154 0 12.305978 2.660254 16.536989 6.952703 4.23306 4.298593 6.850307 10.24167 6.850307 16.799124l0 204.700282 224.675737 206.965287C1026.212043 491.885755 1026.212043 506.567325 1017.295381 515.625294zM745.851194 94.907899l-46.770497 0 0 85.959578 46.770497 47.491367L745.851194 94.907899zM163.72459 474.910509c12.916259 0 23.385249 10.630776 23.385249 23.745683l0 430.348784c0 26.235959 20.940027 47.49751 46.770497 47.49751l161.196225 0-0.002048 0L395.074513 688.656474c0-13.121052 10.471037-23.751827 23.385249-23.751827l187.079941 0c12.916259 0 23.385249 10.630776 23.385249 23.751827l0 287.846013-0.002048 0 161.196225 0c25.83047 0 46.768449-21.261551 46.768449-47.49751l-0.002048-430.348784c0-13.114908 10.468989-23.745683 23.385249-23.745683 12.914211 0 23.385249 10.630776 23.385249 23.745683l0 430.348784c0 52.469871-41.878006 94.995021-93.538947 94.995021L233.880336 1023.999997c-51.660941 0-93.538947-42.52515-93.538947-94.995021L140.34139 498.656193C140.34139 485.541285 150.810379 474.910509 163.72459 474.910509zM582.154454 976.502487l0-264.100329-140.309444 0 0 264.100329-0.002048 0L582.154454 976.502487 582.154454 976.502487z"
                                        p-id="5462" fill="#707070"></path>
                                </svg>
                            </template>
                        </n-button>
                    </span>
                </div>
            </n-layout-header>

            <n-layout position="absolute" style="height: 100%;top: 64px; bottom: 64px" has-sider>
                <n-layout-sider content-style="padding: 24px;" :native-scrollbar="false" bordered>
                    <n-menu v-model:value="activeKey" :options="menuOptions" responsive
                        @update:value="handleMenuSelect" />
                </n-layout-sider>

                <n-layout content-style="padding: 24px;" :native-scrollbar="false">
                    <router-view></router-view>
                </n-layout>

            </n-layout>
        </n-layout>
    </div>
</template>


<script setup>
import { AlbumsOutline as Albums, ImageOutline as Image, TimeOutline as TimeOut } from '@vicons/ionicons5';
import { NIcon } from 'naive-ui';
import { RouterLink, useRouter } from 'vue-router';
import { h, ref, onMounted } from 'vue';

const activeKey = ref(""); // 记录当前选中的菜单项
const router = useRouter();

// 菜单图标
function renderIcon(icon) {
    return () => h(NIcon, null, { default: () => h(icon) });
}

const menuOptions = [
    {
        label: () => h(
            RouterLink,
            {
                to: { name: 'Stitching' }
            },
            { default: () => '图片拼接' }
        ),
        key: 'ImageStitching',
        icon: renderIcon(Albums)
    },
    {
        label: () => h(
            RouterLink,
            {
                to: { name: 'Detect' }
            },
            { default: () => '倒伏检测' }
        ),
        key: 'DetectLodging',
        icon: renderIcon(Image)
    },
    {
        label: () => h(
            RouterLink,
            {
                to: { name: 'History' }
            },
            { default: () => '检测历史' }
        ),
        key: 'History',
        icon: renderIcon(TimeOut)
    }
];

// 处理菜单选择
const handleMenuSelect = (key) => {
    activeKey.value = key;
};

const goToPage = (routeName) => {
    router.push({ name: routeName });
};

</script>

<style lang="scss" scoped>
.header-title {
    width: 300px;
    height: 100%;
    display: flex;
    font-size: 26px;
    justify-content: center;
    align-items: center;
    color: #10705f;
}

.n-layout-header-title {
    height: 64px;
    display: flex;
    justify-content: space-between;
    /* 左右布局 */
    align-items: center;
    font-family: "Microsoft YaHei", "PingFang SC", "Inter", "Arial", sans-serif;
    background-color: #ecf4f1;
}

.header-content {
    width: 100%;
    display: flex;
    justify-content: space-between;
    /* 分开左右布局 */
    align-items: center;
}

.header-right-button {
    display: flex;
    align-items: center;
    margin-right: 20px;
}
</style>
