<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light custom-nav">
        <div class="container">
            <span class="navbar-brand">Online Exam System</span>

            <ul class="navbar-nav ml-auto">
                <li class="nav-item active">
                    <p>
                        <span class="badge badge-light">{{ user["first_name"] }} {{ user['last_name'] }}</span>
                    </p>
                </li>
                <li v-if="page == 'Home'" class="nav-item">
                    <a class="btn btn-sm btn-danger"
                        href="/accounts/logout/"
                        tabindex="-1"
                        >Logout</a>
                </li>
                <li v-else-if="page == 'Exam'">
                    <a class="btn btn-sm btn-danger"
                        tabindex="-1"
                        @click="$emit('click-quit')"
                        >Quit the Exam</a>
                </li>
            </ul>
        </div>
    </nav>
</template>

<script>
import { apiService } from "../../common/api.service";

export default {
    name: "NavbarComponent",

    data() {
        return {
            user: {},
        };
    },

    props: ['page'],

    methods: {
        getUserData() {
            let endpoint = "api/rest-auth/user/";
            apiService(endpoint).then((data) => {
                this.user = JSON.parse(JSON.stringify(data));
            });
        },
    },

    mounted() {
        this.getUserData();
    },
};
</script>

<style scoped>
.custom-nav {
    border-bottom: 1px solid #ddd;
}
</style>
