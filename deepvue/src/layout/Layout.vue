<template>
    <div>
        <Header />
        <!--主体-->
        <div style="display: flex">
            <!--      侧边栏-->
            <Aside />
            <!--内容区域-->
            <div class="note" :style ="note">
                <router-view />
            </div>
        </div>
    </div>
</template>

<script>
    import Header from "@/components/Header";
    import Aside from "@/components/Aside";
    export default {
        name: "Layout",
        components: {
            Aside,
            Header
        },
        data() {
            return {
                note: {
                    backgroundImage: "url(" + require("../assets/geometric-leaves.png") + ")",
                    backgroundRepeat: "no-repeat",
                    backgroundSize: "100% 100%",
                    flex:1
                },
            }
        }
    }
</script>

<style scoped>

</style>