<template>
    <div class="home">
        <navbar-component />
        <div class="container">
            <div v-if="ActiveSessions.length === 0">
                <h2 class="text text-primary">You have no active exams!</h2>
            </div>
            <div v-else>
                <h2>Your current exam session(s)</h2>
                <base-card
                    v-for="(session, ind) in ActiveSessions"
                    :key="ind"
                    class="container"
                >
                    Exam name (click to start):
                    <button
                        @click="startSession(session)"
                        class="btn btn-outline-success"
                    >
                        {{ session.session_name }}
                    </button>
                    <p>Exam Description: {{ session.session_descriptions }}</p>
                </base-card>
            </div>
        </div>
    </div>
</template>

<script>
// @ is an alias to /src
import NavbarComponent from "../components/UI/Navbar.vue";
import { apiService, postAxios } from "../common/api.service";
import BaseCard from "../components/UI/BaseCard.vue";

export default {
    components: { BaseCard, NavbarComponent },
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
        startSession(session) {
            let endpoint = "api/results/";
            let data = {
                    "answers": null,
                    "is_finished": false,
                    "student": null,
                    "session_ref_number": session.session_ref_number
                };
            postAxios(endpoint, data).then( response => {
                console.log(response.data);
                this.$router.push({
                    name: "Exam",
                    params: { SessionId: session.session_ref_number },
                });
                }
            ).catch(e => {
                console.log(e);
            });
        },
    },

    mounted() {
        this.getActiveSessions();
    },
};
</script>
