<template>
    <div class="loading" v-show="msg.show" >
        <div class="load-box">
            <img src="../assets/loading.gif">
            <span>{{ msg.title }}</span>
        </div>
    </div>
</template>

<script>
export default {
    name: 'loading',
    props: {
        msg: Object,
    }
}
</script>

<style scoped lang="scss">
.loading {
    width: 100vw;
    height: 100vh;
    position: absolute;
    top: 0;
    left: 0;
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 9999;

    .load-box {
        width: 100vw;
        height: 100vh;
        background-color: rgba(0, 0, 0, .5);
        border-radius: 5px;
        box-shadow: 0px 1px 15px rgba(0, 0, 0, .5);
        color: #fff;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        letter-spacing: .8px;
        font-size: 13px;

        img {
            width: 100px;
            margin-bottom: 8px;
            -webkit-animation: spin 1s linear infinite; /* 兼容旧版 WebKit 内核浏览器 */
            animation: spin 1s linear infinite; /* 标准写法，兼容现代浏览器 */
        }
    }
}

@keyframes spin {
    to {
        transform: rotate(360deg);
        -webkit-transform: rotate(360deg);
    }
}
</style>