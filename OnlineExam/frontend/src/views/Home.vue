<template>
    <div class="home">
        <div class="container">
            <div v-if="ActiveSessions.length === 0"><h2 class="text text-primary"> You have no active exams!</h2></div>
          <base-card v-else v-for="(session, ind) in ActiveSessions" :key="ind" class="container">
            <router-link :to="'/'+session.session_ref_number" class="btn btn-outline-success">{{ session.session_name }}</router-link>
          </base-card>
        </div>
    </div>
</template>

<script>
// @ is an alias to /src
import { apiService } from "../common/api.service";
import BaseCard from '../components/UI/BaseCard.vue';

export default {
    components: { BaseCard },
    name: "Home",

    data() {
        return {
            ActiveSessions: [],
        };
    },

    methods: {
        getActiveSessions() {
            let endpoint = "api/sessions/";
            apiService(endpoint).then((data) => {
                const midvar = [];
                midvar.push(...data);
                this.ActiveSessions = JSON.parse(JSON.stringify(midvar));
            });
        },
    },

    mounted() {
        this.getActiveSessions();
    },
};
</script>
