<template>
    <nav class="navbar navbar-expand-lg navbar-light custom-nav">
        <div class="container">
            <img src="/media/imgs/logo.png" class="logo img-logo" alt=""/>
            <span class="navbar-brand nav-text-large">Exam System</span>

            <ul class="navbar-nav ml-auto">
                <li v-if="page == 'Exam'" >
                    <p v-if="duration > 0">
                        <exam-timer :exam_dur="duration" />
                    </p>
                </li>

                <li class="nav-item active">
                    <p>
                        <span class="nav-text-small img-logo">{{ user["first_name"] }} {{ user['last_name'] }}</span>
                    </p>
                </li>
                <li>
                    <img :src="user['photo']" style = "width:60px; height:60px;" />
                </li>
                <li v-if="page == 'Home' || page == 'Finish'" class="nav-item">
                    <a class="btn btn-warning"
                        href="/accounts/logout/"
                        tabindex="-1"
                        >Logout</a>
                </li>
                <li v-else-if="page == 'Exam'">
                    <a class="btn btn-warning"
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
import ExamTimer from '../exam_components/ExamTimer.vue';

export default {
    components: { ExamTimer },
    name: "NavbarComponent",

    data() {
        return {
            user: {},
            time: null
            
        };
    },

    props: ['page', 'duration'],

    methods: {
        getUserData() {
            let endpoint = "api/users/";
            apiService(endpoint).then((data) => {
                this.user = JSON.parse(JSON.stringify(data))[0];
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
    background-color: #5bc1ac;
    border-bottom: 1px solid #ddd;
}

.nav-text-large {
    color: white;
    font-size: 25px;
}

.nav-text-small {
    color: white;
    font-size: 20px;
}

.img-logo {
    padding-right: 10px;
    height: 50px;
    max-width: 100%;
}
</style>
